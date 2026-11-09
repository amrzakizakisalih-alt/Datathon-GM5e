# Explication du code du datathon

Ce document explique **tout le code de `src/`**, script par script et fonction par fonction. Pour chaque élément, il répond à quatre questions :

- **Ce qu'il fait :** les opérations, étape par étape.
- **À quoi il sert :** le problème qu'il règle.
- **Ce qu'il intègre :** les données et les fichiers qu'il lit.
- **Ce qu'il apporte au projet :** ce qu'il produit, et l'écran du site qui l'utilise.

**État au 8 novembre 2026 :** la pipeline complète a tourné sans erreur sur les 5 départements. Les résultats sont dans `data/processed/`, et le journal du calcul est dans `pipeline.log`. Le site, lui, n'existe pas encore.

---

## Sommaire

1. [Le projet en une page](#1-le-projet-en-une-page)
2. [Installer et lancer](#2-installer-et-lancer)
3. [Les notions à connaître](#3-les-notions-à-connaître)
4. [Les données brutes](#4-les-données-brutes)
5. [Vue d'ensemble : qui fait quoi](#5-vue-densemble--qui-fait-quoi)
6. [Les scripts un par un](#6-les-scripts-un-par-un)
7. [Des fichiers aux écrans du site](#7-des-fichiers-aux-écrans-du-site)
8. [Pièges de lecture](#8-pièges-de-lecture)
9. [Limites de la solution et difficultés des données](#9-limites-de-la-solution-et-difficultés-des-données)
10. [Ce qui reste à faire](#10-ce-qui-reste-à-faire)

---

## 1. Le projet en une page

**Titre :** « Rendre à la nature ce que le béton et la charrue ont pris ».

**La question :** dans chaque EPCI normand, combien d'hectares de prairies permanentes disparaissent chaque année, et pourquoi ?

- **Le béton :** la prairie est artificialisée (logements, zones d'activité, routes…).
- **La charrue :** la prairie est retournée et devient une culture (blé, maïs…).

Aucun outil existant ne répond à cette question chaque année et par EPCI. Le suivi du ZAN mesure l'espace consommé, pas ce qu'il remplace. Les statistiques agricoles mesurent le stock de prairies restant, tous les dix ans.

**Le récit du projet, en trois temps,** chacun correspondant à un ou plusieurs scripts :

| Temps | Message | Scripts |
|---|---|---|
| 1. Ce qui a été pris | « Voici, EPCI par EPCI, ce que le béton et la charrue ont pris en prairies, zones humides et ZNIEFF… » | `retournements_epci.py`, `beton_charrue_epci.py`, `qualite_epci.py` |
| 2. Pour quoi faire | « … au regard des logements et des emplois créés, et de la trajectoire ZAN. » | `sobriete_epci.py` |
| 3. Où rendre | « Voici les friches où renaturer en priorité. » | `friches.py` |

`tableau_regional.py` rassemble le tout en un seul tableau de 71 lignes, une par EPCI.

**Chiffres clés de la Normandie** (tableau régional, en hectares par an) :

| Indicateur | Valeur |
|---|---|
| Prairies permanentes déclarées en 2015 | 603 765 ha |
| Charrue, moyenne 2015-2024 | 8 150 ha/an (dont 4 920 de prairies anciennes) |
| Béton total, toutes surfaces confondues | 1 374 ha/an |
| Béton sur des prairies permanentes déclarées | 210 ha/an |
| Prairies perdues sur la fenêtre OCS GE (borne basse) | 9 905 ha/an |
| **Part du béton dans les prairies perdues** | **2,1 % (borne basse) à 6,4 % (borne haute)** |

**Ce que ça veut dire :** en Normandie, **la charrue fait disparaître bien plus de prairies que le béton.** C'est le message central du projet.

---

## 2. Installer et lancer

```bash
python3 -m venv .venv
.venv/bin/pip install duckdb rasterio numpy py7zr pytest
.venv/bin/python src/telecharger_donnees.py   # environ 950 Mo, une seule fois
.venv/bin/python src/pipeline.py              # tout le calcul
.venv/bin/python -m pytest tests              # les tests (environ 4 secondes)
```

- **Pourquoi un environnement virtuel (`.venv/`) :** `rasterio` n'est pas installé dans le Python du système. `.venv/` est ignoré par git.
- **Connexion internet :** au premier lancement, `duckdb` télécharge son extension `spatial`, qui fait les calculs géographiques.
- **Un seul département :** `.venv/bin/python src/pipeline.py --deps 14`. Attention, `tableau_regional.py` lit les sorties de tous les départements présents dans `data/processed/`.

---

## 3. Les notions à connaître

| Notion | Explication |
|---|---|
| **EPCI** | Intercommunalité : communauté de communes (CC), d'agglomération (CA), urbaine (CU) ou métropole. La Normandie en touche 71. C'est l'échelle de tous nos résultats. |
| **LCP** | « Plus petite parcelle commune ». RPG Explorer découpe le territoire en morceaux dont les contours ne changent pas de 2015 à 2024. C'est ce qui permet de suivre la culture d'un même morceau de terre année après année. |
| **PP** | Prairie permanente : groupe 18 du RPG (prairies permanentes et prairies rares en herbe). C'est ce qu'on cherche à protéger. |
| **PT** | Prairie temporaire : groupe 19. Une prairie semée, intégrée à une rotation de cultures. |
| **PP ancienne** | Pour un passage de l'année N à N+1 : parcelle déclarée en PP **chaque année de 2015 jusqu'à N**. On la met en avant parce qu'elle échappe aux artefacts administratifs, notamment le reclassement de 2018 (voir la section 9). |
| **Retournement strict** | Une PP l'année N, puis une culture l'année N+1. C'est « la charrue ». Une PP mise en jachère n'en est pas un. |
| **Béton** | Un polygone que l'IGN classe comme nouvellement artificialisé (`artificialisation = 1`) dans OCS GE. |
| **Fenêtre OCS GE** | Les deux dates entre lesquelles l'IGN compare l'occupation du sol : 2019-2022 pour l'Eure, la Manche et la Seine-Maritime, 2020-2023 pour le Calvados et l'Orne. |
| **CS / US** | Dans OCS GE, la couverture du sol (CS : ce qu'on voit) et l'usage du sol (US : à quoi ça sert). Exemple : `CS2.2.1` = herbe, `US1.1` = agriculture, `CS1.1…` = sol bâti, revêtu ou stabilisé, `CS2.1…` = végétation ligneuse (bois, haies). |
| **Point intérieur** | Un point garanti d'être à l'intérieur d'un polygone (`ST_PointOnSurface`). On s'en sert pour dire dans quelle commune tombe un objet. L'objet entier est attribué à cette commune. |
| **Lambert 93** | Le système de coordonnées officiel français, en mètres (EPSG:2154). Les communes arrivent en degrés (WGS84, EPSG:4326) et sont converties, pour que les surfaces et les distances soient justes. |
| **Borne basse / borne haute** | Le béton n'est sûr que sur les parcelles déclarées à la PAC. La borne basse ne compte que celles-là. La borne haute ajoute l'herbe agricole bétonnée hors des parcelles déclarées. La vérité est entre les deux. |
| **ha/an** | Tout est ramené en hectares par an. C'est indispensable, parce que les fenêtres n'ont pas toutes la même durée. |
| **ZAN** | Zéro artificialisation nette. Sa première étape : consommer, de 2021 à 2031, deux fois moins d'espace que de 2011 à 2021. |
| **ENAF** | Espaces naturels, agricoles et forestiers. Leur consommation est mesurée par le Cerema. |

---

## 4. Les données brutes

Toutes sont ouvertes, et toutes sont téléchargées par `telecharger_donnees.py` dans `data/raw/`, qui n'est pas versionné.

| Base | Producteur | Fichier | Utilisée par | Ce qu'on en tire |
|---|---|---|---|---|
| **RPG Explorer 2015-2024** | INRAE, AgroParisTech | `rpg_explorer/seq1524_dXX.gpkg`, `ref_fr_en.csv` | charrue, béton, qualité, friches | La culture de chaque LCP pour chaque année de 2015 à 2024 (`crop15` à `crop24`). `ref_fr_en.csv` relie chaque code de culture à un groupe (`grp`). |
| **OCS GE Artificialisation, différentiel** | IGN | `ocsge_artif/dXX/…/zan_evol_A0_A1_XX.gpkg` | béton, qualité | Les polygones artificialisés (`1`) ou désartificialisés (`-1`) entre les deux dates, avec leur CS et leur US à chaque date. |
| **Communes et EPCI** | geo.api.gouv.fr | `geo/communes_XX.geojson`, `geo/epci_departements.csv` | tous | Le contour et l'EPCI de chacune des 2 644 communes. La liste des 71 EPCI, avec la part de leur surface et de leur population hors des 5 départements. |
| **ZNIEFF de type 1 et 2** | MNHN, via le WFS de l'IGN | `zonages/znieff1.geojson`, `znieff2.geojson` | qualité, friches | Les zones naturelles remarquables. |
| **Natura 2000** (SIC et ZPS) | MNHN, via le WFS de l'IGN | `zonages/natura2000.geojson` | qualité, friches | Les sites protégés au niveau européen. |
| **Inventaire des zones humides** | DREAL Normandie | `zones_humides/dataset/drealnorm_zh_s_r28.shp` | qualité, friches | Les zones humides vérifiées sur le terrain. |
| **Milieux potentiellement humides (MPH)** | INRAE, GéoSAS | `mph/mph_normandie.tif` | qualité, friches | Une image de pixels de 50 m. Les classes 1 à 3 indiquent une probabilité d'être humide. |
| **Observatoire des friches** | EPF Normandie (DataNormandie) | `friches/friches_epfn.geojson`, `dictionnaire.csv` | friches | 5 068 friches, avec leur surface, la pollution, le zonage, l'avancement du projet, la zone inondable et le potentiel de renaturation (méthode ADEME). |
| **CONSOENAF 2011-2025** | Cerema | `consoenaf/conso_com.csv` | sobriété | La consommation d'espace de chaque commune, chaque année, par destination (habitat, activité, routes…). Le fichier contient aussi la population, les ménages et les emplois en 2016 et 2022 (source INSEE). |
| **Séries historiques du recensement** | INSEE | `insee/base-cc-serie-historique-2022.CSV` | sobriété | Le nombre de logements de chaque commune en 2016 et 2022. |

**Prévus au cahier des charges mais non intégrés :** la carte des haies de l'IGN (voir la section 9), CASIAS et SIS de Géorisques (la pollution vient uniquement du champ de l'EPF), Cartofriches (facultatif). Les emplois Urssaf sont remplacés par les emplois INSEE du fichier Cerema.

---

## 5. Vue d'ensemble : qui fait quoi

```
telecharger_donnees.py ──► data/raw/  (toutes les données brutes, une seule fois)

pipeline.py  (chef d'orchestre)
  │
  ├─ pour chaque département (14, 27, 50, 61, 76) :
  │    ├─ retournements_epci.py  ──► retournements_epci_XX.csv   la charrue, année par année
  │    ├─ beton_charrue_epci.py  ──► beton_charrue_epci_XX.csv   béton et charrue sur la fenêtre OCS GE
  │    └─ qualite_epci.py        ──► qualite_epci_XX.csv         bloc D : milieux remarquables
  │
  ├─ sobriete_epci.py            ──► sobriete_epci.csv            bloc E : ZAN, logements, emplois
  ├─ friches.py                  ──► friches.csv, friches_epci.csv   écran 2 : où rendre
  │
  ├─ tableau_regional.py         ──► tableau_regional_epci.csv    tout, par EPCI, avec le bloc F (profils)
  ├─ sensibilite_anomalies.py    ──► sensibilite_anomalies_epci.csv   la charrue avec et sans les anomalies de la PAC
  ├─ sensibilite.py              ──► sensibilite.csv              l'effet des seuils, des poids et des rayons
  ├─ sensibilite_prl.py          ──► sensibilite_prl.csv, sensibilite_prl_epci.csv   le poids des prairies en rotation longue
  └─ export_web.py               ──► web/data/                    les fichiers légers du site (JSON, GeoJSON)

Validation sur photos aériennes (lancée à part, données sensibles dans data/validation/, non versionné) :
  echantillon_validation.py ──► preparer_lecture.py ──► lecture à l'aveugle (lecture.html) ──► resultat_validation.py

definitions.py         définitions partagées : années, classes RPG, retournement strict, prairies anciennes
geo_utils.py           fonctions partagées : charger les communes, rattacher un objet à sa commune
tests/                 21 tests automatiques sur un territoire fictif (lancés avec pytest)
test_rattachement.py   contrôle, lancé à part : mesure l'effet de l'ancien rattachement
```

**Les outils techniques communs à tous les scripts :**
- **DuckDB** et son extension **spatial** : une base de données qui tourne en mémoire, sans serveur. On y écrit du SQL qui lit directement les fichiers géographiques (`ST_Read`), calcule des intersections (`ST_Intersection`), des surfaces (`ST_Area`), des distances (`ST_Distance`)…
- **rasterio** : lit l'image des milieux potentiellement humides, la seule donnée en pixels.
- **numpy** : calcule les scores des friches.
- Tous les fichiers CSV de sortie utilisent le séparateur `;`.

---

## 6. Les scripts un par un

### 6.1 `telecharger_donnees.py` : télécharger les données brutes

**Ce qu'il fait :** il télécharge les 10 bases de la section 4 dans `data/raw/`, les décompresse, et écrit deux fichiers de référence (`fenetres.csv` et `epci_departements.csv`).

**À quoi il sert :** à rendre le projet **reproductible**. N'importe qui peut reconstruire `data/raw/` depuis zéro, sans manipulation à la main. Le script est **idempotent** : un fichier déjà présent et valide n'est pas retéléchargé, donc on peut le relancer sans risque.

**Ce qu'il intègre :** des sources en ligne : l'entrepôt Recherche Data Gouv (RPG Explorer), le Géoplateforme de l'IGN (OCS GE et WFS), geo.api.gouv.fr, GéoSAS (MPH), la DREAL, DataNormandie, data.gouv.fr (Cerema) et l'INSEE.

**Ce qu'il apporte :** toutes les entrées de la pipeline, plus `fenetres.csv`, qui indique à chaque script la fenêtre OCS GE et le fichier à lire pour chaque département.

**Usage :** `python src/telecharger_donnees.py [--deps 14 27 50 61 76]`

#### Ses fonctions

| Fonction | Ce qu'elle fait | Pourquoi |
|---|---|---|
| `ouvrir(url, timeout)` | Ouvre une adresse web avec un en-tête `User-Agent` explicite. | data.geopf.fr (IGN) refuse les requêtes de Python sans cet en-tête (erreur 403). |
| `lire(url)` | Télécharge une petite réponse (page, JSON) en mémoire. | Pour lire des métadonnées et des listes. |
| `md5(chemin)` | Calcule l'empreinte MD5 d'un fichier, par blocs de 1 Mo. | Pour vérifier qu'un gros fichier est complet et intact. |
| `telecharger(url, dest, taille, empreinte)` | Télécharge un fichier, sauf s'il existe déjà avec la bonne taille ou la bonne empreinte. Il écrit d'abord dans un fichier `.part`, puis le renomme à la fin. | Une coupure ne laisse jamais un fichier à moitié écrit qui passerait pour complet. |
| `rpg_explorer(deps)` | Interroge l'API de l'entrepôt pour connaître la liste des fichiers, puis télécharge `ref_fr_en.csv` et le `seq1524_dXX.gpkg` de chaque département, avec contrôle de la taille et du MD5. | RPG Explorer est le plus gros jeu (630 Mo) : le contrôle évite de le retélécharger. |
| `ocsge_artificialisation(deps)` | Lit la page de téléchargement de l'IGN pour chaque département, y repère les couches différentielles, garde **la fenêtre la plus récente** (puis la dernière publication), télécharge l'archive `.7z` en vérifiant son MD5 et la décompresse. Il écrit `fenetres.csv` (département, début, fin, chemin de la couche). | Les fenêtres diffèrent selon le département, et l'IGN publie de nouvelles versions. Le script choisit tout seul la bonne, et les autres scripts n'ont qu'à lire `fenetres.csv`. |
| `communes_et_epci(deps)` | Télécharge les communes de chaque département (contour, code INSEE, EPCI, surface). Il récupère ensuite la liste nationale des EPCI, garde ceux qui touchent la Normandie et, pour ceux qui débordent sur une autre région, calcule la part de leur surface et de leur population hors des 5 départements. | Pour rattacher chaque objet à une commune puis à un EPCI, et pour signaler les 6 EPCI à cheval sur une autre région. |
| `wfs_geojson(typenames, dest, pas)` | Télécharge une couche du service WFS de l'IGN sur l'emprise de la Normandie, **par pages de 1 000 objets**, et assemble le tout en un GeoJSON en Lambert 93. | Le WFS ne renvoie qu'un nombre limité d'objets par requête. |
| `zonages_et_milieux()` | Appelle `wfs_geojson` pour les ZNIEFF 1, les ZNIEFF 2 et Natura 2000 (SIC et ZPS réunis), puis télécharge les zones humides DREAL, l'image MPH découpée sur la Normandie (service WCS), les friches et leur dictionnaire, CONSOENAF et les séries de l'INSEE. | Toutes les données des blocs D, E et de l'écran 2. |

---

### 6.2 `geo_utils.py` : les outils géographiques partagés

**Ce qu'il fait :** il regroupe les deux opérations dont presque tous les scripts ont besoin : charger les communes, et rattacher à une commune les objets qui ne tombent dans aucune.

**À quoi il sert :** à ce que tous les scripts rattachent les objets **de la même façon**. Sinon, deux scripts pourraient attribuer la même parcelle à deux EPCI différents.

**Ce qu'il intègre :** `data/raw/geo/communes_XX.geojson`.

**Ce qu'il apporte :** la table `communes` (code INSEE, nom, EPCI, contour en Lambert 93) dans la base DuckDB du script qui l'appelle.

#### `charger_communes(con, dossier)`

- **Ce qu'elle fait :** elle lit **tous** les fichiers `communes_*.geojson` du dossier, les convertit en Lambert 93 et les réunit dans une seule table `communes`.
- **Pourquoi les 5 départements, et pas seulement celui de l'objet :** le fichier RPG d'un département contient des parcelles situées dans une commune d'un autre département : limites départementales, communes ayant changé de département. Si on ne chargeait que les communes du département, ces parcelles seraient rattachées à tort à la commune la plus proche du mauvais département. `test_rattachement.py` a mesuré cet effet, et c'est ce qui a motivé la correction.
- **Utilisée par :** `retournements_epci.py`, `beton_charrue_epci.py`, `qualite_epci.py`.

#### `rattacher_plus_proche(con, table, cle, point)`

- **Ce qu'elle fait :** pour chaque ligne de `table` qui n'a pas de commune (`insee` vide), elle cherche la commune dont le contour est le plus proche du point de l'objet, et lui donne son code INSEE et son EPCI. Elle affiche le nombre d'objets rattachés et leur distance médiane et maximale.
- **Pourquoi :** certains objets tombent hors de tout contour communal :
  - les contours de geo.api.gouv.fr sont simplifiés, et un objet en bordure peut donc tomber « entre » deux communes ;
  - le littoral et l'estran (la zone entre la marée haute et la marée basse) dépassent souvent les contours ;
  - certains objets sont au-delà des limites de la Normandie.
- **Ce que ça donne :** sur le dernier calcul, 899 parcelles sont concernées (environ 4 700 ha), surtout dans la Manche, à une distance médiane de quelques dizaines de mètres, mais jusqu'à 2,1 km.
- **Utilisée par :** tous les scripts qui rattachent des objets, sauf `sobriete_epci.py`, qui travaille directement par commune.

---

### 6.3 `retournements_epci.py` : la charrue, année par année

**Ce qu'il fait :** pour chaque EPCI et chaque paire d'années (2015→2016, …, 2023→2024), il mesure la surface de prairies permanentes et ce qu'elles sont devenues l'année suivante.

**À quoi il sert :** à mesurer **la charrue sur toute la période 2015-2024**, et pas seulement sur la fenêtre OCS GE. C'est la série chronologique de l'écran 1.

**Ce qu'il intègre :** RPG Explorer (`seq1524_dXX.gpkg`), `ref_fr_en.csv` et les communes.

**Ce qu'il apporte :** `retournements_epci_XX.csv`, une ligne par EPCI et par année.

**Usage :** `python src/retournements_epci.py <seq1524_dXX.gpkg> <ref_fr_en.csv> <dossier_communes> <sortie.csv>`

#### Étape par étape

1. **Chargement :** il charge la table de correspondance culture → groupe, puis les communes avec `charger_communes`.
2. **Classement de chaque LCP, pour chaque année :** selon le groupe RPG de sa culture, avec les règles de `definitions.py`.

   | Classe | Groupes RPG | Exemples |
   |---|---|---|
   | `PP` | 18 | prairies permanentes |
   | `PT` | 19 | prairies temporaires |
   | `fourrage` | 16 | fourrages annuels |
   | `gel` | 11 | jachères : une PP mise en jachère n'est **pas** un retournement |
   | `culture` | 1 à 9, 14, 15, 24, 25 | céréales, oléagineux, maïs, légumes… |
   | `autre` | les autres groupes | vergers, vignes, surfaces non agricoles… |
   | vide | — | parcelle non déclarée cette année-là |

3. **Rattachement :** chaque LCP est attribuée à la commune où tombe son point intérieur, puis à l'EPCI de cette commune. Les LCP orphelines passent par `rattacher_plus_proche`.
4. **Calcul :** pour chaque paire d'années N → N+1 (9 paires), et chaque EPCI, il calcule les colonnes ci-dessous.

#### Colonnes de sortie

| Colonne | Signification |
|---|---|
| `annee` | l'année d'arrivée N+1 (par exemple 2016 pour la paire 2015→2016) |
| `stock_pp` | surface en PP l'année N |
| `strict_toutes` | PP l'année N, culture en N+1 : **la charrue** |
| `strict_anciennes` | idem, mais seulement pour les PP déclarées en PP chaque année depuis 2015 jusqu'à N |
| `vers_pt` | PP devenue prairie temporaire |
| `vers_fourrage` | PP devenue fourrage |
| `vers_gel` | PP mise en jachère |
| `devenir_inconnu` | PP qui n'est plus déclarée en N+1 (sortie de la PAC). **Elle n'est jamais comptée comme retournée** |
| `borne_haute` | `strict_toutes` + `vers_pt` + `vers_fourrage` + `vers_gel` + `devenir_inconnu` : tout ce qui a cessé d'être une PP déclarée |

**Ce qu'il apporte au projet :** la courbe annuelle de la charrue sur l'écran 1, le stock de PP en 2015 (pour calculer le pourcentage de perte), et la moyenne 2015-2024 de la charrue dans le tableau régional.

---

### 6.4 `beton_charrue_epci.py` : le béton et la charrue sur la même période

**Ce qu'il fait :** sur la fenêtre OCS GE du département, il mesure le béton (total, et ce qu'il a pris aux prairies), les sols rendus à la nature, et la charrue **sans compter deux fois** une surface à la fois bétonnée et retournée.

**À quoi il sert :** à **comparer le béton et la charrue sur exactement la même période**. C'est le cœur du projet : il donne la part du béton dans les prairies perdues.

**Ce qu'il intègre :** la couche OCS GE Artificialisation du département, RPG Explorer, `ref_fr_en.csv` et les communes.

**Ce qu'il apporte :** `beton_charrue_epci_XX.csv`, une ligne par EPCI pour la fenêtre du département.

**Usage :** `python src/beton_charrue_epci.py <couche OCS GE> <année début> <année fin> <seq1524_dXX.gpkg> <ref_fr_en.csv> <dossier_communes> <sortie.csv>`

#### Étape par étape

1. **Le béton :** il garde les polygones `artificialisation = 1` de la couche IGN, avec leur couverture et leur usage avant (`cs0`, `us0`) et après (`cs1`, `us1`). Il affiche ce qu'il y avait avant le béton : la plupart du temps, `CS2.2.1` / `US1.1`, c'est-à-dire de l'herbe agricole.
   - **Pourquoi la couche officielle de l'IGN, plutôt qu'une règle maison sur CS × US :** l'IGN applique le décret 2023-1096 avec des critères en plus du couple CS/US, et une règle maison ne reproduit pas ses résultats.
2. **Les LCP :** il classe chaque LCP pour chaque année, avec les mêmes classes que la charrue (`definitions.py`).
3. **Croisement béton × LCP :** il calcule l'**intersection géométrique** de chaque polygone de béton avec chaque LCP qu'il touche. On obtient ainsi la surface exacte bétonnée sur chaque parcelle, et ce qui y était cultivé l'année de début (PP, PT, culture…).
4. **Rattachement aux EPCI :** il rattache les LCP, les polygones de béton et ceux de désartificialisation par leur point intérieur, puis avec `rattacher_plus_proche` pour les orphelins.
   - **Le béton est ventilé selon l'EPCI du polygone de béton**, et non selon celui de chaque parcelle touchée. Le béton total et sa répartition (sur PP, sur PT, sur cultures, hors RPG) s'additionnent donc toujours, même pour un polygone à cheval sur deux EPCI.
5. **Prairies probables hors PAC :** un polygone de béton posé sur de l'herbe agricole (`CS2.2.1` et `US1.1`), mais **hors** des parcelles déclarées, est sans doute une prairie que l'exploitant ne déclarait pas. Cette surface est comptée à part et sert à la **borne haute**.
6. **La désartificialisation** (`artificialisation = -1`) est séparée en deux :
   - **sols rendus :** le sol était bâti, revêtu ou stabilisé (`CS1.1…`) au début. C'est une vraie renaturation ;
   - **changement d'usage :** la surface était déjà végétalisée, et seul son usage a changé (par exemple, la fin d'un chantier sur une prairie). Ce n'est pas un vrai gain.
7. **Contrôle :** il affiche ce que deviennent dans le RPG, en fin de fenêtre, les PP touchées par le béton. Ça permet de vérifier le risque de double comptage.
8. **La charrue nette du béton :** une PP devenue culture compte pour sa surface **moins la part bétonnée de la même LCP**. **Le béton l'emporte**, donc une surface n'est jamais comptée deux fois. Un retournement compte comme « PP ancienne » si la parcelle était en PP chaque année de 2015 jusqu'à l'année du retournement, comme dans `retournements_epci.py`.

#### Colonnes de sortie

| Colonne | Signification |
|---|---|
| `debut`, `fin` | les années de la fenêtre OCS GE |
| `beton_total` | toute l'artificialisation, quelle que soit la surface d'avant |
| `beton_sur_pp`, `beton_sur_pt`, `beton_sur_cultures` | la part posée sur des PP, des PT ou des cultures déclarées l'année de début (`beton_sur_cultures` inclut les fourrages et les jachères) |
| `beton_hors_rpg` | le béton hors des parcelles déclarées (`beton_total` moins les trois précédents) |
| `beton_herbe_hors_pac` | les prairies probables hors PAC bétonnées |
| `desartif_sols`, `desartif_usage` | les sols rendus et les simples changements d'usage |
| `charrue_pp`, `charrue_pp_anciennes` | la charrue sur la fenêtre, nette du béton (toutes les PP, et les PP anciennes) |
| `prairies_perdues` | `beton_sur_pp` + `charrue_pp` (borne basse) |
| `part_beton_pct` | la part du béton dans les prairies perdues (borne basse) |
| `prairies_perdues_haute`, `part_beton_haute_pct` | idem, avec les prairies probables hors PAC (borne haute) |

Les surfaces sont **cumulées sur la fenêtre** (3 ans). C'est `tableau_regional.py` qui les ramène en hectares par an.

**Ce qu'il apporte au projet :** la barre « béton contre charrue » avec sa fourchette, les sols rendus, et le message central (le béton ne représente que 2 à 6 % des prairies perdues).

---

### 6.5 `qualite_epci.py` : le bloc D, ce qui a été pris en milieux remarquables

**Ce qu'il fait :** il mesure combien de béton et de charrue sont tombés **dans des milieux de grande valeur écologique** : ZNIEFF, Natura 2000, zones humides, milieux potentiellement humides, surfaces boisées.

**À quoi il sert :** à passer de « combien d'hectares » à « **quels** hectares ». Un hectare de zone humide bétonné ne vaut pas un hectare de champ de maïs. C'est l'enrichissement « 1 bis » du cahier des charges.

**Ce qu'il intègre :** la couche OCS GE du département (via `fenetres.csv`), RPG Explorer, les communes, les ZNIEFF 1 et 2, Natura 2000, les zones humides DREAL et les MPH.

**Ce qu'il apporte :** `qualite_epci_XX.csv`, une ligne par EPCI.

**Usage :** `python src/qualite_epci.py <département> <sortie.csv>`

#### Étape par étape

1. **Communes :** il charge les communes des 5 départements avec `charger_communes`, pour bien rattacher les objets en bordure. Il garde à part celles du département (`communes_dep`) pour deux usages :
   - calculer l'**emprise** du département, plus 5 km de marge, et ne charger que les zonages qui la touchent. Le calcul est ainsi beaucoup plus rapide ;
   - fixer la liste des EPCI en sortie.
2. **Béton dans chaque zonage :** pour chaque polygone de béton, il **fusionne** les zonages qui le touchent, puis calcule l'intersection. La fusion compte une seule fois une surface couverte par deux ZNIEFF qui se chevauchent.
3. **Béton dans les milieux potentiellement humides :** comme le MPH est une image, il découpe l'image selon le polygone et calcule la part des pixels de classe 1 à 3. Il multiplie ensuite la surface du polygone par cette part. Pour un polygone plus petit qu'un pixel de 50 m, il prend la valeur du pixel sous son point intérieur.
4. **Béton sur des surfaces boisées (`beton_ligneux`) :** les polygones dont la couverture était `CS2.1…` (bois, bosquets, haies larges) l'année de début.
5. **Charrue :** il compte, pour chaque LCP, le nombre de retournements stricts sur les 9 paires d'années 2015-2024 (toutes PP, et PP anciennes). Une LCP compte comme « dans une zone » si son point intérieur y tombe. Pour le MPH, on lit le pixel sous ce point.
   - Une année non déclarée vaut `'non déclaré'` et non `NULL` : sinon, un seul terme vide effaçait tous les retournements de la parcelle (défaut corrigé le 9 novembre, voir `HISTORIQUE.md`).
6. **Agrégation par EPCI.** La liste des EPCI est celle du département, plus ceux des communes voisines où tombent des objets du département.

#### Colonnes de sortie

| Colonne | Signification |
|---|---|
| `beton_ligneux` | béton sur une couverture boisée (ha, sur la fenêtre) |
| `beton_znieff1`, `beton_znieff2`, `beton_natura2000`, `beton_zh` | béton dans chaque zonage (ha, sur la fenêtre) |
| `beton_mph` | béton dans les milieux potentiellement humides (ha, sur la fenêtre) |
| `charrue_zh`, `charrue_mph`, `charrue_natura2000`, `charrue_znieff1` | surface retournée dans chaque zonage, cumulée sur 2015-2024 (ha) |
| `…_anc` | idem, pour les PP anciennes |

#### Précautions

- **Natura 2000 :** un retournement dans un site Natura 2000 **n'est pas une infraction**. La PAC n'y interdit que le retournement des « prairies sensibles », et la plupart des sites ne sont pas désignés pour leurs prairies. Il ne faut jamais présenter cet indicateur comme une infraction.
- **Pourquoi pas de « km de haies » :** voir la section 9.

**Ce qu'il apporte au projet :** les indicateurs écologiques de la fiche EPCI. Par exemple : « dans la Manche, 5 716 ha retournés sur 2015-2024 étaient en milieux potentiellement humides ».

---

### 6.6 `sobriete_epci.py` : le bloc E, la trajectoire ZAN et ce qu'on a gagné

**Ce qu'il fait :** pour chaque EPCI, il mesure la consommation d'espace face à l'objectif ZAN, et ce qu'elle a permis de créer en logements et en emplois.

**À quoi il sert :** à répondre à la question « **pour quoi faire ?** ». On met en regard ce qui a été pris et ce qu'on a gagné. C'est la problématique P2 du datathon (les interactions entre l'humain et la nature), et c'est ce qui intéresse les élus qui révisent leurs PLUi et leurs SCoT.

**Ce qu'il intègre :** CONSOENAF (Cerema), qui contient aussi la population, les ménages et les emplois en 2016 et 2022 ; les séries historiques de l'INSEE (logements) ; les communes (pour l'EPCI). C'est le seul script qui ne fait **aucun calcul géométrique** : tout se fait par code de commune.

**Ce qu'il apporte :** `sobriete_epci.csv`, une ligne par EPCI.

**Usage :** `python src/sobriete_epci.py <sortie.csv>`

#### Étape par étape

1. **Chargement :** il charge la correspondance commune → EPCI de geo.api. Si une commune en est absente, il prend l'EPCI que lui donne le Cerema.
2. **Consommation :** pour chaque commune, il lit la consommation 2011-2021 (`naf11art21`), la consommation 2021-2025 (`naf21art25`), la consommation pour l'habitat 2016-2022 et la consommation pour l'activité 2016-2022 (somme des années).
3. **Logements :** il lit le nombre de logements en 2016 et 2022 (INSEE).
4. **Repérage des gros projets :** pour chaque commune et chaque année de 2021 à 2025, il repère le plus gros flux de consommation et sa destination principale. Si un seul flux représente au moins 20 ha **et** la moitié de la consommation 2021-2025 de l'EPCI, une alerte est levée. La projection repose alors sur un seul projet, ou sur une anomalie du cadastre, et elle doit être vérifiée.
5. **Agrégation par EPCI** et calcul des indicateurs.

#### Colonnes de sortie

| Colonne | Signification |
|---|---|
| `conso_ref_ha` | consommation du 1/1/2011 au 1/1/2021 : la période de référence du ZAN |
| `conso_2021_2025_ha` | consommation du 1/1/2021 au 1/1/2025 |
| `rythme_ref_ha_an`, `rythme_actuel_ha_an` | les mêmes, en ha par an |
| `enveloppe_2021_2031_ha` | la moitié de `conso_ref_ha` : ce que l'EPCI peut consommer de 2021 à 2031 |
| `enveloppe_consommee_pct` | la part de cette enveloppe déjà consommée au 1/1/2025 |
| `projection_2031_pct` | la consommation de 2021 à 2031 si le rythme actuel continue, en % de l'enveloppe. **Au-dessus de 100 %, l'EPCI dépasse sa trajectoire** |
| `principal_flux_2021_2025`, `part_principal_flux_pct` | le plus gros flux d'une commune (commune, année, ha, destination) et son poids |
| `alerte_flux_unique` | vrai si la projection repose sur un seul gros flux |
| `projection_2031_pct_hors_principal` | la projection sans ce flux |
| `conso_habitat_2016_2022_ha`, `conso_activite_2016_2022_ha` | la consommation pour l'habitat et pour l'activité |
| `delta_logements`, `delta_menages`, `delta_population`, `delta_emplois` | les variations entre 2016 et 2022 |
| `logements_par_ha_habitat` | logements créés par hectare consommé pour l'habitat. **Vide si moins de 1 ha a été consommé. Négatif si le nombre de logements a baissé malgré la consommation** |
| `emplois_par_ha_activite` | emplois créés par hectare consommé pour l'activité, avec les mêmes règles |
| `population_2022`, `surface_km2`, `densite_2022` | pour classer l'EPCI dans un profil (bloc F) |

**Remarque :** la référence est la règle nationale (réduction de moitié). La territorialisation du SRADDET peut fixer d'autres taux selon le territoire.

**Chiffres régionaux :**
- 16 857 ha consommés de 2011 à 2021, puis 5 787 ha de 2021 à 2025 ;
- **68,7 % de l'enveloppe 2021-2031 était déjà consommée au 1er janvier 2025**, alors que 40 % de la période seulement s'était écoulée ;
- 11,5 logements créés par hectare consommé pour l'habitat.

**Ce qu'il apporte au projet :** la trajectoire ZAN et l'efficacité de chaque EPCI sur l'écran 1. Ce sont aussi les bases du futur simulateur (écran 3).

---

### 6.7 `friches.py` : l'écran 2, où rendre à la nature

**Ce qu'il fait :** pour chacune des 5 068 friches de l'EPF Normandie, il calcule un **score de potentiel écologique**, en teste la robustesse, classe la friche (« gain rapide », etc.), explique son rang en clair et liste les points de vigilance.

**À quoi il sert :** à répondre à la problématique P1 (« où agir en priorité ») et au « rendre à la nature » du titre. L'EPF fournit déjà un « potentiel de renaturation » selon la méthode ADEME, mais il mesure la **faisabilité** (propriétaire, bâti, pollution…), pas l'**intérêt écologique**. Le script ajoute ce qui manquait : est-ce que renaturer cette friche reconnecte la nature existante ?

**Ce qu'il intègre :** l'observatoire des friches, les ZNIEFF 1, Natura 2000, les zones humides DREAL, les MPH, RPG Explorer 2024 (les prairies autour de la friche) et les communes.

**Ce qu'il apporte :**
- `friches.csv` : une ligne par friche, avec ses critères, ses scores, sa classe, ses raisons, ses points de vigilance et ses coordonnées pour la carte ;
- `friches_epci.csv` : une synthèse par EPCI.

**Usage :** `python src/friches.py <friches.csv> <friches_epci.csv>`

#### Étape par étape

1. **Chargement** des communes des 5 départements, puis des friches (surface, pollution, zonage, avancement du projet, potentiel EPF, position, zone inondable, zone humide).
2. **Calcul des 5 critères :**

   | Critère | Calcul | Idée |
   |---|---|---|
   | `dist_reservoir_m` | distance à la ZNIEFF 1 ou au site Natura 2000 le plus proche (0 si la friche est dedans, plafonnée à 5 km) | renaturer là où ça reconnecte un réservoir de biodiversité |
   | `part_humide_pct` | la plus forte de trois valeurs : la part de la friche en zone humide DREAL, la part de ses pixels MPH en classe 1 à 3, et 100 % si l'EPF signale une zone humide avérée | une zone humide restaurée a beaucoup de valeur (biodiversité, eau) |
   | `part_prairies_500m_pct` | surface de PP déclarées en 2024 dans une couronne de 500 m, rapportée à la surface de la couronne | une friche entourée de prairies peut les relier |
   | `surface_ha` | surface de la friche | plus c'est grand, plus l'effet est fort |
   | `contexte_urbain` | friche en centre-bourg ou en quartier d'habitation | pour le préréglage « nature en ville » |

3. **Passage en rangs centiles (`centile`) :** chaque critère est converti en rang de 0 à 100 (0 = la moins bonne friche, 100 = la meilleure). Ça rend comparables des mètres, des pourcentages et des hectares. Les ex æquo reçoivent la moyenne de leurs rangs. La surface passe par un logarithme, pour que quelques très grandes friches n'écrasent pas tout.
4. **Trois scores, selon trois jeux de poids** (réservoir, humide, prairies, surface, ville) :

   | Préréglage | Poids | Pour qui |
   |---|---|---|
   | `score_biodiversite` (défaut) | 35 / 20 / 30 / 15 / 0 | reconnecter la nature |
   | `score_eau` | 15 / 60 / 10 / 15 / 0 | restaurer les zones humides |
   | `score_ville` | 15 / 15 / 5 / 15 / 50 | nature en ville |

5. **Test de robustesse (`robustesse_pct`) :** les poids sont un choix discutable. Le script tire donc **1 000 jeux de poids au hasard** (loi de Dirichlet sur les 4 critères écologiques) et compte, pour chaque friche, la part des tirages où elle reste dans les 10 % meilleures. Une friche robuste à 90 % est bien classée **quels que soient les poids**. C'est un argument solide devant le jury.
6. **Classes :**
   - « projet engagé » : un projet de reconversion est en démarches ou finalisé ;
   - « petite friche (< 0,1 ha) » : renaturer quelques centaines de m² ne pèse pas à l'échelle d'un EPCI ;
   - parmi les autres friches, dites « éligibles » (2 268) :
     - « **gain rapide** » : un potentiel écologique au moins égal au 75e centile **et** une faisabilité EPF au moins égale à la médiane ;
     - « **fort potentiel, contraintes** » : un fort potentiel, mais une faisabilité faible ;
     - « potentiel modéré » : le reste.
7. **Raisons (`raison`) :** les trois critères qui contribuent le plus au score de la friche, écrits en clair. Par exemple : « dans une ZNIEFF ou un site Natura 2000 ; 45 % en zone humide inventoriée ou potentielle ; 2,3 ha ».
8. **Vigilance :** les points à vérifier avant toute décision :
   - la pollution : avérée, potentielle, inconnue ou **non renseignée**. « Non renseignée » ne veut pas dire « saine » ;
   - un terrain constructible (zone U ou AU), donc une pression foncière ;
   - une zone inondable (PPRI). C'est un atout écologique, mais une contrainte d'usage.

#### Les fonctions internes

| Fonction | Rôle |
|---|---|
| `centile(v)` | convertit une liste de valeurs en rangs centiles de 0 à 100, en gérant les ex æquo |
| `raison(k, r)` | écrit en français la phrase qui correspond au critère `k` d'une friche |

#### Résultats

| Classe | Nombre | Surface |
|---|---|---|
| potentiel modéré | 1 701 | 1 493 ha |
| projet engagé | 596 | 1 007 ha |
| **gain rapide** | **413** | **635 ha** |
| fort potentiel, contraintes | 154 | 106 ha |
| petite friche | 2 204 | 85 ha |

**`friches_epci.csv`** contient, par EPCI : le nombre et la surface des friches, la surface et le nombre de friches « gain rapide », la surface « fort potentiel, contraintes » et la surface « projet engagé ».

**Données personnelles :** aucune. Les friches sont des sites publiés par l'EPF, et les prairies ne servent qu'à calculer un taux autour de la friche. Aucune parcelle agricole n'est affichée.

**Ce qu'il apporte au projet :** toute la carte « Où rendre » (écran 2) et le top 10 des friches par EPCI avec la raison de leur rang, comme le demande le cahier des charges.

---

### 6.8 `tableau_regional.py` : le tableau final par EPCI

**Ce qu'il fait :** il rassemble les sorties de tous les scripts en **un seul tableau de 71 lignes** (une par EPCI) et 75 colonnes, ramène tout en hectares par an, et ajoute le **profil** de chaque EPCI (bloc F) pour comparer des territoires semblables.

**À quoi il sert :** c'est **la source de données de la fiche EPCI** sur le site. Tout ce qu'un élu verra pour son territoire est dans ce fichier.

**Ce qu'il intègre :** `retournements_epci_*.csv`, `beton_charrue_epci_*.csv`, `qualite_epci_*.csv`, `sobriete_epci.csv`, `friches_epci.csv` et `epci_departements.csv`.

**Ce qu'il apporte :** `tableau_regional_epci.csv`.

**Usage :** `python src/tableau_regional.py <dossier data/processed> <epci_departements.csv> <sortie.csv>`

#### Étape par étape

1. **Base béton et charrue :**
   - la charrue 2015-2024 est la somme des 9 paires divisée par 9, donc une moyenne annuelle ;
   - chaque partie départementale est annualisée sur sa propre fenêtre (béton ÷ (fin − début)) ;
   - un EPCI présent dans plusieurs fichiers départementaux est la somme de ses parties. Si ces parties ont des fenêtres différentes, sa fenêtre est notée `mixte` (18 EPCI).
2. **Bloc D :** le béton en milieux remarquables, annualisé sur la fenêtre, et la charrue en milieux remarquables, divisée par 9.
3. **Bloc E :** il reprend `sobriete_epci.csv` tel quel.
4. **Friches :** il reprend `friches_epci.csv`, et calcule `annees_beton_friches` = surface des friches ÷ béton annuel. Exemple de lecture : « les friches de l'EPCI représentent 4 années de béton ». C'est un message fort pour le pitch.
5. **Bloc F, le profil de l'EPCI :**

   | Profil | Règle | Nombre |
   |---|---|---|
   | urbain | densité ≥ 300 hab/km² | 5 |
   | périurbain | densité ≥ 100 hab/km² | 21 |
   | rural herbager | PP ≥ 20 % du territoire | 25 |
   | rural de grandes cultures | les autres | 20 |

   Pour chaque profil : le nombre d'EPCI, le **rang** de l'EPCI pour la perte de prairies (en % du stock), et les médianes du profil. On compare ainsi le Cotentin aux EPCI périurbains plutôt qu'à la Métropole de Rouen.
6. **Les EPCI à cheval sur une autre région :**
   - `perimetre` indique « EPCI entier » ou « partie normande (X % de la surface) ». Tous les chiffres ne portent que sur la partie normande ;
   - `exclu_comparaisons` vaut vrai si au moins la moitié de la surface est hors Normandie. C'est le cas du Pays de Dreux et du Maine Saosnois (5 % en Normandie chacun) : leur rang et leurs médianes restent vides.

#### Colonnes principales

| Groupe | Colonnes |
|---|---|
| Identité | `epci_code`, `epci_nom`, `departements`, `hors_normandie`, `fenetre_ocsge`, `perimetre`, `exclu_comparaisons` |
| Charrue | `stock_pp_2015`, `charrue_toutes_ha_an`, `charrue_anciennes_ha_an`, `charrue_fenetre_ha_an`, `charrue_anciennes_fenetre_ha_an` |
| Béton | `beton_total_ha_an`, `beton_sur_pp_ha_an`, `beton_hors_rpg_ha_an`, `beton_herbe_hors_pac_ha_an` |
| Sols rendus | `desartif_sols_ha_an`, `desartif_usage_ha_an` |
| **Le bilan** | `prairies_perdues_ha_an`, `part_beton_pct`, `prairies_perdues_haute_ha_an`, `part_beton_haute_pct`, `perte_pct_stock_an` |
| Bloc D | `beton_ligneux_ha_an`, `beton_znieff1_ha_an`, …, `charrue_mph_ha_an`, … |
| Bloc E | toutes les colonnes de `sobriete_epci.csv` |
| Friches | `n_friches`, `friches_ha`, `friches_gain_rapide_ha`, `n_gain_rapide`, …, `annees_beton_friches`, `annees_beton_gain_rapide` |
| Bloc F | `part_pp_territoire_pct`, `profil`, `n_profil`, `rang_perte_profil`, `perte_pct_stock_an_mediane_profil`, `part_beton_pct_mediane_profil` |

**Cases vides normales :** les EPCI sans friche n'ont pas de chiffres friches. Les ratios logements ou emplois par hectare sont vides quand moins de 1 ha a été consommé. Les deux EPCI exclus n'ont ni rang ni médiane de profil.

---

### 6.9 `pipeline.py` : le chef d'orchestre

**Ce qu'il fait :** il lance tous les scripts dans le bon ordre, avec les bons arguments.

**À quoi il sert :** à tout recalculer **en une seule commande**, sans se tromper de fichier ni d'argument. C'est l'exigence de reproductibilité du cahier des charges.

**Ce qu'il intègre :** `fenetres.csv`, pour connaître la fenêtre et la couche de chaque département.

**Ce qu'il apporte :** tous les fichiers de `data/processed/`.

**Usage :** `python src/pipeline.py [--deps 14 27 50 61 76]`

| Fonction ou partie | Rôle |
|---|---|
| `lancer(script, *args)` | lance un script de `src/` avec le même Python, et **s'arrête à la première erreur** (`check=True`) |
| la boucle sur les départements | pour chaque département : `retournements_epci.py`, `beton_charrue_epci.py`, puis `qualite_epci.py` |
| après la boucle | `sobriete_epci.py` et `friches.py`, qui traitent toute la région d'un coup, puis `tableau_regional.py` |
| à la fin | les trois analyses de sensibilité (`sensibilite_anomalies.py`, `sensibilite.py`, `sensibilite_prl.py`), puis `export_web.py`. Une seule commande produit donc des données cohérentes jusqu'au site |

---

### 6.10 `definitions.py` : les définitions partagées

**Ce qu'il fait :** il contient, à un seul endroit, la liste des années, les groupes RPG de chaque classe et les expressions SQL qui classent une parcelle, repèrent un retournement strict et une prairie ancienne.

**À quoi il sert :** à ce que tous les scripts comptent de la même façon. Avant sa création, les copies avaient divergé : la jachère comptait comme une culture dans deux scripts sur trois, et les prairies anciennes avaient deux définitions.

**Ce qu'il intègre :** rien : il ne lit aucune donnée.

**Ce qu'il apporte :** il est importé par `retournements_epci.py`, `beton_charrue_epci.py`, `qualite_epci.py`, `friches.py`, `sensibilite.py`, `sensibilite_prl.py`, `echantillon_validation.py` et `test_rattachement.py`.

| Fonction ou constante | Rôle |
|---|---|
| `ANNEES` | les suffixes des colonnes `crop15` à `crop24` |
| `GRP_PP`, `GRP_PT`, `GRP_FOURRAGE`, `GRP_GEL`, `GRP_CULTURE` | les groupes RPG de chaque classe |
| `annees_entre(debut, fin)` | les années d'une fenêtre, par exemple 2019-2022 → `['19', '20', '21', '22']` |
| `jointures_ref()` | les jointures SQL qui relient la culture de chaque année à son groupe |
| `classe_sql(y)`, `classes_sql()` | l'expression SQL de la classe d'une année (`k19`…), ou de toutes les années |
| `retournement_sql(a, b)` | la condition « PP l'année a, culture l'année b » |
| `pp_ancienne_sql(n)` | la condition « PP chaque année de 2015 jusqu'à n » |
| `CODE_PPH`, `CODE_PRL` | les deux codes du groupe 18 : prairie permanente au sens strict, prairie en rotation longue (supprimé du RPG en 2023) |

### 6.11 `sensibilite_anomalies.py` : la charrue face aux anomalies de la PAC

**Ce qu'il fait :** il recalcule la charrue moyenne de chaque EPCI selon cinq scénarios (référence, sans le passage 2017→2018, sans le passage 2018→2019, sans les passages 2022→2024, prairies anciennes seulement) et compare chaque classement des EPCI à celui de référence.

**À quoi il sert :** à vérifier que nos conclusions ne dépendent pas des anomalies connues de la PAC : le reclassement de 2018, le pic de labours de 2019 qui en découle, et le trou de 2023.

**Ce qu'il intègre :** `retournements_epci_*.csv` et `tableau_regional_epci.csv` (pour écarter les EPCI exclus des comparaisons).

**Ce qu'il apporte :** `sensibilite_anomalies_epci.csv`, avec la charrue et le rang de chaque EPCI dans chaque scénario. Le résumé affiché donne, pour chaque scénario, la corrélation de rang de Spearman, le plus grand déplacement, le nombre d'EPCI déplacés de plus de 5 rangs et le nombre d'EPCI communs aux deux top 10. Voir `HISTORIQUE.md` pour les résultats.

### 6.11 bis `sensibilite.py` : l'effet des seuils, des poids et des rayons

**Ce qu'il fait :** il fait varier un choix à la fois et mesure l'effet sur ce que l'outil affiche :
- **le classement des EPCI** selon la définition des pertes (bornes basse et haute, toutes PP ou anciennes, fenêtre OCS GE ou moyenne 2015-2024), mesuré par la corrélation de Spearman ;
- **les profils d'EPCI** selon les seuils de densité et de part de prairies : combien d'EPCI changent de profil ;
- **les friches « gain rapide »** selon le seuil de potentiel, la surface minimale, les poids et le rayon des prairies (300, 500 ou 1 000 m), mesurés par l'indice de Jaccard (la part de friches communes aux deux ensembles) ;
- **le « noyau stable »** : les friches qui restent « gain rapide » dans toutes les variantes (281 sur 413, soit 481 ha sur 635) ;
- **le béton en milieux potentiellement humides**, réparti par classe de probabilité.

**À quoi il sert :** à montrer quels choix de méthode pèsent sur les résultats, et lesquels ne changent presque rien. Il commence par un contrôle : son recalcul des friches doit redonner exactement `friches.csv` (Jaccard = 1).

**Ce qu'il intègre :** `tableau_regional_epci.csv`, `friches.csv`, les friches brutes, RPG Explorer 2024, les couches OCS GE et l'image des milieux potentiellement humides.

**Ce qu'il apporte :** `sensibilite.csv`, une ligne par test. `export_web.py` en reprend le noyau stable des friches.

### 6.11 ter `sensibilite_prl.py` : le poids des prairies en rotation longue

**Ce qu'il fait :** il recalcule les retournements par EPCI et par année en séparant les deux codes du groupe 18, `PPH` (prairie permanente) et `PRL` (prairie en rotation longue), puis compare plusieurs définitions : toutes les PP, sans les `PRL`, sans les `PRL` de 2023 seulement, et `PPH` chaque année depuis 2015. Il analyse aussi ce que deviennent les `PRL` en 2023, l'année où le code disparaît (94 % sont déclarées `PPH`).

**À quoi il sert :** à mesurer la part de la charrue qui vient de prairies en rotation, et donc probablement pas de vraies prairies permanentes (15 % de la charrue en Normandie, jusqu'à 32 % dans certains EPCI).

**Ce qu'il intègre :** RPG Explorer, les communes et `tableau_regional_epci.csv`. Il vérifie d'abord que ses totaux redonnent ceux de la pipeline.

**Ce qu'il apporte :** `sensibilite_prl.csv` (les mesures) et `sensibilite_prl_epci.csv` (la charrue sans `PRL` de chaque EPCI, reprise par `export_web.py` dans les fiches du site).

### 6.12 `tests/` : les tests automatiques

**Ce qu'il fait :** 21 tests, lancés avec `.venv/bin/python -m pytest tests`, sur un territoire fictif de deux communes dont on connaît le résultat à l'avance.

**À quoi il sert :** à vérifier en quelques secondes qu'une modification ne casse aucun calcul, et à documenter la méthode par des exemples.

| Fichier | Ce qu'il vérifie |
|---|---|
| `conftest.py` | il fabrique le territoire fictif, aux formats exacts de RPG Explorer, d'OCS GE et de geo.api |
| `test_definitions.py` | les classes RPG (y compris `PRL`), le retournement strict, la jachère, les prairies anciennes |
| `test_geo_utils.py` | le chargement des communes, le passage en Lambert 93, le rattachement à la commune la plus proche |
| `test_pipeline_scripts.py` | les vrais scripts `retournements_epci.py` et `beton_charrue_epci.py`, cas par cas : le béton l'emporte sur la charrue, le reclassement de 2018, le trou de 2023, le hors PAC, les sols rendus, un béton à cheval sur deux EPCI |

### 6.13 `test_rattachement.py` : un contrôle, lancé à part

**Ce qu'il fait :** il compare l'**ancienne** méthode de rattachement (un objet cherché seulement dans les communes de son département) à la nouvelle (les 5 départements). Pour chaque objet mal placé avec l'ancienne méthode, il indique s'il tombe dans un autre département normand (`autre_dep`) ou hors de tout contour normand (`hors_contours`).

**À quoi il sert :** à **prouver** que la correction de `charger_communes` était nécessaire, et à mesurer son effet par EPCI.

**Ce qu'il intègre :** RPG Explorer, OCS GE et les communes.

**Ce qu'il apporte :** `data/processed/test_rattachement_epci.csv`. Il ne fait pas partie de la pipeline : on le lance à la main avec `python src/test_rattachement.py`.

### 6.14 `export_web.py` : les fichiers du site

**Ce qu'il fait :** il transforme les résultats de `data/processed/` en fichiers légers pour le site, dans `web/data/` :

| Fichier | Contenu |
|---|---|
| `regional.json` | les totaux normands, la série 2015-2024, les sources et les avertissements de lecture |
| `epci_index.json` | une ligne légère par EPCI, pour la carte et la recherche |
| `epci_contours.geojson` | les contours des 71 EPCI, simplifiés sans créer de trous entre voisins |
| `epci/<code>.json` | la fiche complète d'un EPCI (71 fichiers de 3 Ko au plus) |
| `friches.geojson` | un point par friche d'au moins 0,1 ha |
| `friches/<code>.json` | le détail des friches d'un EPCI, chargé à la demande |

**À quoi il sert :** à alimenter un site statique, sans serveur, léger (environ 145 Ko compressés au premier chargement, hors bibliothèques), comme l'exige le critère de sobriété.

**Ce qu'il protège :** aucune parcelle agricole n'est exportée. Les noms de friches ne sont pas repris, parce que certains contiennent un nom de personne ou une mention de succession : le libellé est reconstruit (« ancienne activité à commune »). Des contrôles automatiques vérifient qu'aucun identifiant de parcelle ne figure dans les fichiers.

### 6.15 La validation sur photos aériennes

Trois scripts mesurent si les retournements détectés dans le RPG sont réels, en les vérifiant sur les photos aériennes de l'IGN. **Ils manipulent des localisations de parcelles agricoles : leurs fichiers restent dans `data/validation/`, qui n'est pas versionné.**

| Script | Ce qu'il fait |
|---|---|
| `echantillon_validation.py` | tire au hasard, de façon reproductible, des parcelles d'au moins 1 ha retournées entre 2021 et 2023, par département et par ancienneté (prairie ancienne ou récente), plus des parcelles témoins restées en prairie. Il ne garde que les points dont la photo d'après est de l'année même du retournement |
| `preparer_lecture.py` | télécharge les photos avant et après de chaque point, et prépare une lecture **à l'aveugle** : le lecteur ne voit ni le type de point, ni le département, ni la culture déclarée |
| `resultat_validation.py` | calcule le taux de confirmation (« culture » visible sur la photo d'après), pondéré par la surface des strates, avec un intervalle de confiance à 95 %, l'accord entre lecteurs (kappa de Cohen) et le taux de fausses alertes sur les témoins |

**Les fichiers de la lecture :** la page `data/validation/lecture.html` et le protocole `data/validation/LISEZ-MOI.md` (avec la règle de calcul fixée avant lecture). Ce sont les deux seuls fichiers de `data/validation/` que git conserve.

**Le registre des choix :** `docs/registre_choix_methodologiques.md` liste chaque choix qui influe sur les chiffres, avec l'alternative écartée, la justification et la preuve. C'est la base de la page méthode et des réponses au jury.

**Sa limite :** elle mesure la **précision** (les retournements détectés sont-ils vrais ?), pas les **oublis** (combien de vrais retournements le RPG ne voit pas).

---

## 7. Des fichiers aux écrans du site

| Écran (cahier des charges) | Fichier source | Colonnes clés |
|---|---|---|
| **1. Ce que le béton et la charrue ont pris** | `tableau_regional_epci.csv` | `prairies_perdues_ha_an`, `part_beton_pct` / `part_beton_haute_pct`, `desartif_sols_ha_an`, `profil`, `rang_perte_profil` |
| 1. La courbe 2015-2024 | `retournements_epci_XX.csv` | `annee`, `strict_toutes`, `strict_anciennes` |
| **1 bis. Enrichissements** | `tableau_regional_epci.csv` | blocs D (`beton_zh_ha_an`, `charrue_mph_ha_an`…) et E (`projection_2031_pct`, `logements_par_ha_habitat`…) |
| **2. Où rendre** | `friches.csv`, `friches_epci.csv` | `lon`, `lat`, `score_biodiversite`, `classe`, `raisons`, `vigilance`, `robustesse_pct` |
| **3. Et si…** (simulateur) | `tableau_regional_epci.csv` | `enveloppe_2021_2031_ha`, `rythme_actuel_ha_an`, `friches_gain_rapide_ha`, `prairies_perdues_ha_an` |
| **4. Méthode et sobriété** | ce document | sections 3, 4, 8 et 9 |

**Fait :** l'export en JSON et le fond de carte des 71 EPCI (`export_web.py`, dans `web/data/`). **Reste à faire :** le site lui-même.

---

## 8. Pièges de lecture

- **Comparer le béton et la charrue :** prendre `charrue_fenetre_ha_an`, mesurée sur la même période que le béton, et non `charrue_toutes_ha_an`.
- **Les prairies perdues sous le béton :** prendre `beton_sur_pp_ha_an`, et non `beton_total_ha_an`, qui compte tout le béton, y compris sur des champs ou des jardins.
- **Toujours afficher la fourchette :** `part_beton_pct` (basse) et `part_beton_haute_pct` (haute).
- **Face aux chiffres de l'Agreste :** l'Agreste annonce 18 % de béton, mais c'est un bilan net 2008-2019, toutes prairies confondues. Notre chiffre (2 à 6 %) est un flux annuel, sur les seules prairies permanentes. Il faut toujours citer les deux, chacun avec sa définition.
- **« Impact » :** le code mesure des **surfaces** perdues, pas leurs effets sur la biodiversité ou l'eau.
- **Natura 2000 :** un retournement dans un site Natura 2000 n'est pas une infraction.
- **Vocabulaire neutre :** la plupart des retournements sont légaux.
- **Fenêtres différentes :** les départements ne couvrent pas la même période. Il faut le signaler dans les comparaisons.
- **EPCI à cheval :** lire la colonne `perimetre`, et préférer les ratios aux hectares.

---

## 9. Limites de la solution et difficultés des données

Cette section sert de base à la partie « limites » du rapport et de la page méthode.

### Les haies ne sont pas mesurées : la surface boisée les remplace

- **Ce que prévoyait le cahier des charges :** les km de haies disparus sous le béton.
- **Le problème :** pour mesurer des haies bétonnées entre 2019 et 2022, il faut savoir où étaient les haies **avant** le béton. Or la couche nationale des haies de l'IGN disponible est l'édition 2026 : elle montre les haies **actuelles**. Une haie arrachée pour construire n'y figure plus. Le croisement donnerait presque zéro, ce qui serait faux.
- **Ce qu'on fait à la place :** `beton_ligneux`, le béton posé sur une couverture boisée (`CS2.1…`) **l'année de début** de la fenêtre. La date est donc la bonne.
- **Les limites de ce remplacement :**
  - ce sont des hectares, pas des km ;
  - la haie bocagère typique (quelques mètres de large) est trop étroite pour l'OCS GE, et seules les haies larges sont vues. Le chiffre est donc une **borne basse** ;
  - les haies sont mélangées avec les bois et les bosquets.
- **Une piste :** une édition plus ancienne de la BD TOPO de l'IGN (thème « haie ») permettrait de mesurer les haies d'avant le béton. Ce n'est pas vérifié.

### Les artefacts de la PAC

- **La rupture de 2018 :** 83 824 ha de prairies temporaires passent en permanentes. C'est probablement un reclassement administratif (dans la PAC, une PT déclarée depuis plus de 5 ans devient une PP), pas un vrai changement sur le terrain. La cause reste à confirmer. Ça gonfle le stock de PP et peut faire croire à des retournements ensuite. **Parade :** les PP anciennes en chiffre principal.
- **L'anomalie de 2023 :** 30 462 ha de prairies déclarées en 2022 ne le sont plus en 2023, probablement à cause de la refonte du RPG. Ils vont dans `devenir_inconnu`, et ne sont jamais comptés comme retournés.
- **Le RPG ne voit que les surfaces déclarées à la PAC :** les prairies non déclarées (chevaux, particuliers, retraités) sont invisibles. D'où les « prairies probables hors PAC » de la borne haute.

### Le béton

- **Les fenêtres OCS GE diffèrent** selon le département (2019-2022 ou 2020-2023), et elles sont courtes (3 ans) : une année exceptionnelle pèse beaucoup.
- **Une fausse désartificialisation dans l'Orne :** environ 212 ha, ce qui gonfle les « sols rendus ». À vérifier sur photo aérienne. Seuls les « sols rendus » sont affichés, pas les changements d'usage.
- **Les prairies probables hors PAC** sont une estimation : de l'herbe agricole hors parcelle déclarée n'est pas forcément une prairie permanente.

### Le rattachement géographique

- **Une LCP comptée en entier :** si elle chevauche deux EPCI, toute sa surface va à celui de son point intérieur. L'effet n'est pas mesuré, mais il est faible à l'échelle de l'EPCI.
- **899 LCP (environ 4 700 ha) tombent hors de tout contour normand,** et sont rattachées à la commune la plus proche (jusqu'à 2,1 km). Une mesure du 8 novembre (voir `HISTORIQUE.md`, étape 4) a montré que ce n'est pas un défaut des contours : ADMIN EXPRESS donne le même résultat.
  - Environ 276 LCP (3 850 ha) sont des **prés salés** de la côte ouest de la Manche, au-delà du trait de côte. Leur rattachement à la commune littorale est correct, et elles ne sont presque jamais retournées.
  - 622 LCP (environ 820 ha, dont 350 ha de PP) sont **dans des départements voisins, hors de Normandie**, et sont attribuées à tort à un EPCI normand. L'effet est faible (0,06 % du stock), et la correction est connue : les exclure.
- **6 EPCI sont à cheval sur une autre région :** seule leur partie normande est calculée.

### Les définitions entre scripts

- **Réglé le 8 novembre :** les définitions de la jachère et des prairies anciennes sont maintenant communes à tous les scripts (`definitions.py`), et un dossier `tests/` existe. Les tests anciens cités dans les commentaires (`tests/T5b`, `T8`, `T9`) restent introuvables.
- **Toutes les PP ou PP anciennes ?** Le cahier des charges veut les PP anciennes en chiffre principal, mais le tableau régional calcule le bilan et les rangs avec toutes les PP. L'analyse de sensibilité montre que ce choix change beaucoup le classement des EPCI. Il reste à trancher.

### Les autres données

- **Les emplois** viennent de l'INSEE (emplois au lieu de travail, via le fichier Cerema), pas de l'Urssaf comme prévu.
- **La pollution des friches** vient uniquement du champ de l'EPF. CASIAS et SIS (Géorisques) ne sont pas intégrés, et beaucoup de friches ont une pollution « non renseignée ».
- **Les poids du score des friches** sont un choix. Le test de robustesse le compense en partie.
- **La trajectoire ZAN** suit la règle nationale (réduction de moitié). Le SRADDET peut fixer d'autres taux selon le territoire.
- **Les ratios logements ou emplois par hectare** comparent deux sources différentes (Cerema et INSEE) sur des dates proches mais pas identiques.

### Points vérifiés

| Point | Résultat |
|---|---|
| Totaux recalculés depuis les données brutes | charrue, stock et béton identiques, à 1 ha près |
| Rattachement en bordure de département | corrigé avec `charger_communes`, et mesuré par `test_rattachement.py` |
| Retournements répétés (une LCP comptée à chaque passage) | négligeable : environ 0,7 % de la charrue |
| Jachère (gel) | n'est plus comptée comme une culture : −96 ha/an de charrue (−1,2 %) |
| Anomalies de 2018 et 2023 | voir `sensibilite_anomalies.py` et `HISTORIQUE.md` |
| `beton_hors_rpg` négatif | aucun cas |
| Pipeline complète du 8 novembre | elle tourne sans erreur, 71 EPCI, aucun doublon |

---

## 10. Ce qui reste à faire

D'après le cahier des charges (remise le 12 novembre à midi, gel du code les 9 et 10 novembre) :

1. **L'export pour le site :** un JSON par EPCI et un fond de carte léger des contours.
2. **Le site statique :** l'écran 1 et l'écran 4 sont indispensables, puis l'écran 2. Le simulateur (écran 3) est un bonus.
3. **La page méthode :** à partir des sections 3, 4, 8 et 9 de ce document, avec la déclaration RGESN et la mesure EcoIndex.
4. **La fiche projet** (les 7 points de la consigne) et le dictionnaire des colonnes livrable.
5. **Les vérifications terrain** sur photo aérienne : la désartificialisation de l'Orne et quelques cas d'herbe hors PAC.
6. **Le pitch** (13-23 novembre), avec une vidéo de démonstration de secours.
