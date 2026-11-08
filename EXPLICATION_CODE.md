# Explication du code du datathon

Ce document explique ce que fait le code de `src/`, à partir de sa lecture et d'un contrôle des données de `data/raw/`.

**État actuel :** la pipeline a tourné sur les 5 départements, et ses résultats sont dans `data/processed/`. Le journal du dernier calcul est dans `pipeline.log`. `duckdb` n'est pas installé dans le Python système : il faut un environnement virtuel.

## 1. L'objectif en bref

Le code mesure, pour chaque EPCI normand, **les surfaces de prairies permanentes perdues**, et distingue deux causes :

- **la charrue :** une prairie permanente devient une culture ;
- **le béton :** une prairie permanente est artificialisée.

Il répond à la question : « Dans ce territoire, combien d'hectares de prairies disparaissent par an, et quelle part est due au béton ? »

## 2. Les trois bases de données

| Base | Dossier | Rôle |
|---|---|---|
| **RPG Explorer** (INRAE) | `data/raw/rpg_explorer/` | ce qui est cultivé sur chaque LCP, de 2015 à 2024 |
| **OCS GE Artificialisation** (IGN) | `data/raw/ocsge_artif/` | les zones artificialisées ou désartificialisées |
| **Communes et EPCI** (geo.api.gouv.fr) | `data/raw/geo/` | les contours des communes et leur EPCI |

### RPG Explorer

- **LCP :** plus petite parcelle commune. C'est l'unité de surface suivie d'une année à l'autre.
- **Colonnes utiles :** `id_lcp`, `area_lcp` (surface en ha), `crop15` à `crop24` (culture de chaque année).
- **`ref_fr_en.csv` :** relie chaque code de culture à un groupe (`grp`).

### OCS GE

Chaque ligne est un polygone qui a changé d'état entre deux années :

- `artificialisation = 1` : zone artificialisée, le « béton » ;
- `artificialisation = -1` : zone désartificialisée ;
- `cs_AAAA` : couverture du sol, ce qu'on voit sur le terrain ;
- `us_AAAA` : usage du sol, ce à quoi il sert.

La période n'est pas la même partout :

| Départements | Fenêtre OCS GE |
|---|---|
| 14, 61 | 2020-2023 |
| 27, 50, 76 | 2019-2022 |

### Communes et EPCI

- **`communes_XX.geojson` :** 2 644 communes au total, avec `nom`, `code` (INSEE), `codeEpci`, `epci`, `surface` et leur contour.
- **`epci_departements.csv` :** 71 EPCI, avec `departements` et `hors_normandie`.

Hiérarchie : **commune → EPCI → département → région**. Les types d'EPCI sont CC (communauté de communes), CA (d'agglomération), CU (urbaine) et Métropole.

La carte `communes_epci.html` permet d'explorer cette base.

## 3. Les scripts

```
telecharger_donnees.py     télécharge les 3 bases dans data/raw/
        │
pipeline.py                pour chaque département :
        ├── retournements_epci.py    charrue par EPCI et par an
        ├── beton_charrue_epci.py    béton + charrue sur la fenêtre OCS GE
        │        (les deux utilisent geo_utils.py)
        └── tableau_regional.py      une fois à la fin : tableau des 71 EPCI
```

Pour tout lancer :

```bash
pip install duckdb py7zr
python src/telecharger_donnees.py
python src/pipeline.py
```

`duckdb` télécharge aussi son extension `spatial` au premier lancement, il faut donc une connexion internet.

### `telecharger_donnees.py`

Télécharge les données brutes (environ 650 Mo) sans refaire ce qui est déjà présent et valide. Pour OCS GE, il prend la fenêtre la plus récente de chaque département et l'écrit dans `fenetres.csv`.

### `geo_utils.py`

Contient `rattacher_plus_proche`, qui traite les objets dont le point ne tombe dans aucune commune. Ils sont rattachés à la commune la plus proche.

Ces cas existent pour trois raisons :

- les contours communaux sont simplifiés ;
- le littoral et l'estran dépassent parfois les contours ;
- l'objet peut se trouver au-delà de la limite de la Normandie.

Le fichier contient aussi `charger_communes`, qui charge les communes des 5 départements : un LCP d'un fichier départemental peut en effet se trouver dans une commune d'un autre département.

### `retournements_epci.py` : la charrue, année par année

1. **Reprojection :** les communes passent de WGS84 (degrés) à Lambert 93 (mètres).
2. **Classement :** chaque LCP reçoit une classe pour chaque année, selon son groupe RPG :

   | Classe | Groupes RPG |
   |---|---|
   | `PP` (prairie permanente) | 18 |
   | `PT` (prairie temporaire) | 19 |
   | `fourrage` | 16 |
   | `culture` | 1 à 9, 11, 14, 15, 24, 25 |
   | `autre` | les autres groupes |
   | vide | non déclaré cette année-là |

3. **Rattachement :** un point à l'intérieur du LCP donne sa commune, donc son EPCI. Le LCP compte en entier pour cet EPCI.
4. **Calcul :** pour chaque paire d'années N → N+1 et chaque EPCI :

   | Colonne | Signification |
   |---|---|
   | `stock_pp` | surface en PP l'année N |
   | `strict_toutes` | PP devenue culture |
   | `strict_anciennes` | idem, mais PP chaque année depuis 2015 |
   | `vers_pt`, `vers_fourrage` | PP devenue PT ou fourrage |
   | `devenir_inconnu` | PP non déclarée en N+1 |
   | `borne_haute` | somme de `strict_toutes`, `vers_pt`, `vers_fourrage` et `devenir_inconnu` |

**Sortie :** `retournements_epci_XX.csv`, une ligne par EPCI et par an.

### `beton_charrue_epci.py` : béton et charrue sur la même période

1. **Béton :** garde les polygones `artificialisation = 1`.
2. **Croisement avec le RPG :** calcule l'intersection entre chaque polygone et chaque LCP, ce qui donne la surface bétonnée sur chaque LCP. La culture de l'année de début indique ce qui a été bétonné.
3. **Rattachement à l'EPCI :** les LCP et les polygones sont rattachés par un point intérieur.
4. **Prairies probables hors PAC :** de l'herbe agricole (`CS2.2.1` et `US1.1`) bétonnée hors parcelle déclarée est comptée à part. Elle sert à la borne haute.
5. **Désartificialisation :** elle est seulement affichée, et séparée en deux :
   - sols rendus : le sol était bâti, revêtu ou stabilisé (`CS1.1...`) ;
   - simple changement d'usage d'une surface déjà végétalisée.
6. **Charrue sans double comptage :** PP devenue culture, moins la surface bétonnée sur ce LCP. **Le béton l'emporte.**

**Sortie :** `beton_charrue_epci_XX.csv`, une ligne par EPCI et par fenêtre.

### `tableau_regional.py` : le tableau final

Rassemble tous les départements et ramène tout en **hectares par an**. Un EPCI qui a des objets dans plusieurs fichiers départementaux est la somme de ses parties, chacune étant annualisée sur sa propre fenêtre. Si ces fenêtres diffèrent, sa fenêtre est marquée `mixte`, même si l'autre partie ne représente que quelques parcelles (18 EPCI sont dans ce cas).

| Colonne | Signification |
|---|---|
| `stock_pp_2015` | prairies permanentes déclarées en 2015 (ha) |
| `charrue_toutes_ha_an` | charrue, moyenne 2015 → 2024 |
| `charrue_fenetre_ha_an` | charrue sur la fenêtre OCS GE, sans le béton |
| `beton_total_ha_an` | toute l'artificialisation, prairies ou non |
| `beton_sur_pp_ha_an` | béton sur des prairies permanentes déclarées |
| `beton_herbe_hors_pac_ha_an` | béton sur des prairies probables hors PAC |
| `prairies_perdues_ha_an` | `beton_sur_pp` + `charrue_fenetre` (borne basse) |
| `part_beton_pct` | part du béton dans ces pertes (borne basse) |
| `prairies_perdues_haute_ha_an`, `part_beton_haute_pct` | idem, avec les prairies probables hors PAC |
| `perte_pct_stock_an` | `prairies_perdues` / `stock_pp_2015` |
| `hors_normandie` | l'EPCI a des communes hors des 5 départements |

**Sortie :** `tableau_regional_epci.csv`.

## 4. Pièges de lecture

- **Comparer charrue et béton :** prendre `charrue_fenetre_ha_an`, sur la même période que le béton, et non `charrue_toutes_ha_an`.
- **Prairies perdues :** prendre `beton_sur_pp_ha_an`, et non `beton_total_ha_an`, qui inclut tout le béton.
- **« Impact » :** le code mesure des surfaces perdues, pas leurs effets sur la biodiversité ou l'eau.
- **Fenêtres différentes :** les départements ne couvrent pas la même période, ce qu'il faut signaler dans les comparaisons.

## 5. Les 6 EPCI à cheval sur la Normandie

Seules leurs communes normandes sont dans la base. Le calcul est juste pour cette partie, mais ne représente pas forcément tout l'EPCI.

| EPCI | Communes en Normandie | Surface en Normandie |
|---|---|---|
| CC Interco Normandie Sud Eure | 40 / 41 | 99 % |
| CC Aumale - Blangy-sur-Bresle | 34 / 44 | 81 % |
| CU d'Alençon | 26 / 31 | 73 % |
| CC des Villes Sœurs | 15 / 28 | 61 % |
| CA du Pays de Dreux | 6 / 81 | 5 % |
| CC Maine Saosnois | 2 / 51 | 5 % |

**Règle proposée, encore à valider :**

- garder les 6 dans les totaux régionaux ;
- traiter Sud Eure comme un EPCI normal ;
- signaler Aumale-Blangy, Alençon et Villes Sœurs comme « partie normande uniquement » ;
- retirer Dreux et Maine Saosnois des classements.

Pour ces EPCI, comparer de préférence les ratios plutôt que les hectares. Le code actuel ne contient pas de colonne `part_normande_pct`.

## 6. Points vérifiés et points ouverts

### Vérifiés

| Point | Résultat |
|---|---|
| Totaux recalculés depuis les données brutes | charrue, stock et béton identiques, à 1 ha près |
| Rattachement en bordure de département | corrigé : les communes des 5 départements sont chargées (voir `src/test_rattachement.py`) |
| Retournements répétés (un LCP compté à chaque passage) | négligeable : environ 0,7 % de la charrue |
| Gel compté comme culture (groupe 11) | négligeable : 1,2 % de la charrue |
| `beton_hors_rpg` négatif | aucun cas |

### Ouverts

1. **Rupture de 2018 :** 83 824 ha de prairies temporaires passent en permanentes. La cause reste à confirmer, et ça gonfle `perte_pct_stock_an`, calculé sur le stock de 2015.
2. **Anomalie de 2023 :** 30 462 ha de prairies déclarées en 2022 ne le sont plus en 2023. Ils ne comptent pas comme retournés.
3. **Un LCP compté en entier :** s'il chevauche deux EPCI, toute sa surface va à celui de son point intérieur. L'effet n'est pas mesuré.
4. **LCP hors de tout contour normand :** 899 LCP (4 667 ha), surtout dans la Manche, sont rattachés à la commune la plus proche. Leur vrai rattachement n'est pas prouvé.
5. **« PP anciennes » pas tout à fait identiques :** dans `retournements_epci.py`, la prairie doit être PP chaque année jusqu'à l'année N. Dans `beton_charrue_epci.py`, seulement jusqu'au début de la fenêtre.
6. **Référence à un test absent :** `beton_charrue_epci.py:14` cite `tests/T5b`, mais il n'y a pas de dossier `tests/` ici.
