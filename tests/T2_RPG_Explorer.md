# Test T2 : RPG Explorer (INRAE), successions de cultures dans la Manche

Date : 18/10/2026. Résultat : **GO**. On lit directement les passages prairie permanente → culture, sans faire nous-mêmes la superposition des RPG. Deux artefacts administratifs sont à neutraliser.

## Le jeu de données

- **Nom :** « Crop successions 2015-2024 (France mainland) », version 1.4 publiée le 15/04/2026. Auteurs : B. Girault (INRAE) et P. Martin (AgroParisTech).
- **DOI :** 10.57745/6G0JTJ (Recherche Data Gouv).
- **Licence : Etalab 2.0**, réutilisation libre avec mention de la source. Aucun compte n'est nécessaire.
- **Fichiers :** un GeoPackage par département et un Parquet national.
  - Normandie : d14 = 114 Mo, d27 = 83 Mo, d50 = 177 Mo, d61 = 135 Mo, d76 = 120 Mo, soit environ 630 Mo au total.
  - Table des codes : `ref_fr_en.csv`, qui donne le code, son libellé et son groupe de culture (28 groupes).
- **Fichiers téléchargés :** `data/raw/rpg_explorer/seq1524_d50.gpkg` et `ref_fr_en.csv`.
- **Principe :** les parcelles RPG de 2015 à 2024 sont superposées pour obtenir les « plus petites parcelles communes » (LCP). Chaque LCP porte son code culture pour chaque année. Le nettoyage fait perdre environ 1 % de la surface du RPG.

## Colonnes (table `seq1524_d50`)

`fid`, `wkb_geometry` (polygone en Lambert-93), `id_lcp`, `area_lcp` (ha), `id15`…`id24` (identifiant IGN de la parcelle chaque année), `crop15`…`crop24` (code culture, vide si rien n'est déclaré cette année-là), `code_dept`, `code_reg`.

**Manche :** 252 282 LCP pour 436 637 ha. Les codes sont lisibles avec SQLite seul, sans bibliothèque SIG.

## Codes utiles

| Classe | Codes | Remarque |
|---|---|---|
| Prairie permanente (groupe 18) | PPH (herbe prédominante), PRL (prairie en rotation longue, 6 ans ou plus) | **PRL disparaît en 2023** et se fond dans PPH |
| Prairie temporaire (groupe 19) | PTR, RGA | Prairies de 5 ans ou moins |
| Culture | Groupes 1-9, 11, 14, 15, 24, 25 | Le groupe 16 « fourrage » est compté à part |

## Résultat : devenir des prairies permanentes d'une année à l'autre (Manche)

| Paire | Stock PP (ha) | → culture (strict) | → prairie temporaire | → non déclarée | Strict % | Borne haute % |
|---|---|---|---|---|---|---|
| 2015→16 | 174 507 | 1 566 | 2 629 | 2 714 | 0,90 | 4,02 |
| 2016→17 | 172 699 | 1 356 | 411 | 3 185 | 0,79 | 2,92 |
| 2017→18 | 172 873 | 871 | 31 | 3 173 | 0,50 | 2,39 |
| 2018→19 | 214 822 | 6 105 | 123 | 2 522 | 2,84 | 4,23 |
| 2019→20 | 209 750 | 3 418 | 18 | 3 506 | 1,63 | 3,41 |
| 2020→21 | 206 954 | 3 404 | 13 | 2 419 | 1,64 | 2,90 |
| 2021→22 | 205 173 | 4 258 | 16 | 3 351 | 2,08 | 3,84 |
| 2022→23 | 202 145 | 4 433 | 7 | **10 227** | 2,19 | 7,35 |
| 2023→24 | 192 215 | 1 648 | 6 | 3 544 | 0,86 | 2,74 |

- **Retournements stricts cumulés de 2015 à 2024 : environ 27 000 ha.** Presque tous sont durables : la parcelle ne redevient pas prairie permanente l'année suivante.
- **Ce qui remplace les prairies :** surtout du maïs ensilage (≈ 17 100 ha) et du maïs (≈ 6 900 ha). C'est cohérent avec Agreste, pour qui les retournements viennent surtout des élevages laitiers.
- **Retour culture → prairie permanente :** faible, de 24 à 436 ha par an.
- **Plausibilité :** en moyenne environ 1,5 % du stock par an, du même ordre que la DRAAF Grand Est (1 à 1,2 %).

## Deux artefacts à neutraliser

1. **Le reclassement de 2018.** Le stock de prairies permanentes bondit de 172 873 à 214 822 ha, tandis que les prairies temporaires passent de 65 881 à 21 494 ha : c'est la règle des 5 ans de la PAC. Depuis 2018, plus de la moitié des retournements stricts portent sur des prairies « récentes », qui étaient prairie temporaire ou culture avant de devenir permanentes.
   - Il faut donc distinguer les **prairies anciennes**, restées en prairie permanente depuis 2015, et les **prairies récentes**.
   - Retournements de prairies **anciennes** de 2015 à 2024 : **≈ 13 000 ha**, de 725 à 2 108 ha par an. C'est le chiffre le plus solide écologiquement.
2. **Les « sorties » de 2023.** 10 227 ha de prairies permanentes de 2022 ne sont plus déclarés en 2023, et seulement 1 964 ha le sont de nouveau en 2024. La surface non déclarée totale passe d'environ 21 600 à 31 000 ha. Cela coïncide avec la disparition du code PRL et la refonte du RPG en 2023.
   - À afficher comme « devenir inconnu », jamais comme retournement.
   - À vérifier : comparer avec le RPG brut de l'IGN pour 2023.

## Conséquences pour le projet

- **Raccourci validé :** la comparaison année par année se fait en SQL simple sur ce fichier. Le test T3 (superposition maison) devient secondaire. Il ne servira que pour 2025, qui n'est pas dans RPG Explorer (arrêt en 2024).
- **Indicateur proposé, par EPCI et par an :**
  - **retournement strict des prairies anciennes**, le chiffre principal ;
  - **retournement strict toutes prairies permanentes** ;
  - **borne haute**, avec les passages en prairie temporaire et les sorties de la PAC ;
  - **surfaces au devenir inconnu**, affichées à part.
- **Distinguer PPH et PRL avant 2023** : une prairie en rotation longue retournée n'a pas la même valeur écologique qu'une prairie naturelle.
- **Prochaine étape technique :** rattacher chaque LCP à sa commune puis à son EPCI (centroïde dans le contour communal), avec DuckDB spatial ou GeoPandas. C'est le nouveau test le plus utile.
- **Articulation avec le béton :** il faudra croiser les LCP avec les polygones artificialisés de l'OCS GE (test T5) pour appliquer la règle « le béton l'emporte sur la charrue ».
- **Mention obligatoire :** « Données : RPG Explorer, INRAE / AgroParisTech (Girault & Martin), d'après le RPG IGN-ASP, Licence Etalab 2.0. »
