# Test T2b : retournements de prairies par EPCI et par an (Manche)

Date : 18/10/2026. Résultat : **GO**. Le rattachement aux communes et aux EPCI fonctionne et prend environ 4 secondes pour tout le département.

## Ce qui a été fait

- **Script :** `src/retournements_epci.py` (DuckDB 1.5.6 et son extension spatiale, environnement `.venv`).
  ```
  .venv\Scripts\python.exe src\retournements_epci.py data\raw\rpg_explorer\seq1524_d50.gpkg data\raw\rpg_explorer\ref_fr_en.csv data\raw\geo\communes_50.geojson data\processed\retournements_epci_50.csv
  ```
- **Communes :** geo.api.gouv.fr (contours et code EPCI). La Manche compte 445 communes réparties dans 8 EPCI.
- **Méthode :** chaque LCP est rattachée à la commune qui contient un point intérieur de sa géométrie (`ST_PointOnSurface`), puis à l'EPCI de cette commune.
- **Sortie :** `data/processed/retournements_epci_50.csv`, avec une ligne par EPCI et par année. Colonnes : `stock_pp`, `strict_anciennes`, `strict_toutes`, `vers_pt`, `vers_fourrage`, `devenir_inconnu`, `borne_haute`.
- **Convention :** `annee` = l'année N+1 où la culture est observée. « 2016 » désigne donc un retournement entre la déclaration 2015 et la déclaration 2016.

## Contrôles

- **Parcelles non rattachées :** 610 LCP (4 191 ha, environ 1 % de la surface). Ce sont probablement des parcelles du littoral ou de la frontière départementale, que les contours simplifiés de geo.api ne couvrent pas. À corriger plus tard en les affectant à la commune la plus proche, ou en utilisant les contours ADMIN EXPRESS.
- **Cohérence avec le test T2 :** la somme des EPCI donne 27 040 ha de retournements stricts, toutes prairies permanentes, sur 2015-2024. T2 trouvait 27 059 ha ; l'écart correspond aux parcelles non rattachées.
- **Définition des « prairies anciennes »**, plus stricte qu'en T2 : en prairie permanente **chaque année** depuis 2015, une année non déclarée étant éliminatoire. On obtient 12 350 ha, contre 13 048 ha en T2.

## Retournements stricts de prairies anciennes (ha) par EPCI et par an

| EPCI | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| CA du Cotentin | 275 | 229 | 182 | 471 | 324 | 306 | 486 | 390 | 160 | **2 824** |
| CA Mont-Saint-Michel-Normandie | 314 | 261 | 130 | 370 | 283 | 340 | 260 | 262 | 102 | **2 322** |
| CA Saint-Lô Agglo | 273 | 189 | 87 | 398 | 180 | 216 | 307 | 277 | 126 | **2 053** |
| CC Coutances Mer et Bocage | 238 | 220 | 102 | 333 | 186 | 192 | 244 | 287 | 112 | **1 913** |
| CC de la Baie du Cotentin | 193 | 40 | 62 | 108 | 81 | 106 | 176 | 190 | 72 | **1 029** |
| CC Côte Ouest Centre Manche | 74 | 94 | 48 | 118 | 68 | 103 | 145 | 147 | 30 | **827** |
| CC de Villedieu Intercom | 100 | 91 | 68 | 110 | 80 | 75 | 68 | 58 | 41 | **692** |
| CC de Granville, Terre et Mer | 96 | 98 | 53 | 97 | 83 | 41 | 80 | 112 | 31 | **691** |
| **Manche** | 1 562 | 1 222 | 732 | 2 005 | 1 285 | 1 379 | 1 768 | 1 723 | 674 | **12 350** |

## Synthèse 2015-2024 par EPCI

| EPCI | Stock PP 2015 (ha) | Strict, prairies anciennes | Strict, toutes PP | Devenir inconnu | Borne haute | Strict toutes PP, % du stock par an | Prairies anciennes retournées, % du stock 2015 |
|---|---|---|---|---|---|---|---|
| CA du Cotentin | 41 469 | 2 824 | 5 832 | 7 849 | 14 754 | 1,41 | 6,8 |
| CA Mont-Saint-Michel-Normandie | 28 678 | 2 322 | 7 674 | 8 015 | 17 084 | **2,40** | 8,1 |
| CA Saint-Lô Agglo | 26 321 | 2 053 | 3 849 | 4 869 | 9 452 | 1,48 | 7,8 |
| CC Coutances Mer et Bocage | 21 392 | 1 913 | 3 166 | 3 699 | 7 382 | 1,51 | 8,9 |
| CC de la Baie du Cotentin | 23 031 | 1 029 | 1 639 | 2 289 | 4 134 | **0,76** | 4,5 |
| CC Côte Ouest Centre Manche | 13 107 | 827 | 2 070 | 2 319 | 4 653 | 1,55 | 6,3 |
| CC de Villedieu Intercom | 9 325 | 692 | 1 594 | 1 799 | 3 713 | 1,68 | 7,4 |
| CC de Granville, Terre et Mer | 7 239 | 691 | 1 218 | 2 034 | 3 461 | 1,76 | **9,5** |

## Premières lectures (à confirmer)

- **Entre 4,5 % et 9,5 % des prairies permanentes anciennes de 2015 ont été retournées en culture en neuf ans**, selon l'EPCI.
- **CA Mont-Saint-Michel-Normandie :** l'écart entre « toutes PP » (7 674 ha) et « anciennes » (2 322 ha) y est le plus fort. La plupart de ses retournements portent sur des prairies récentes, reclassées permanentes en 2018. C'est cohérent avec les rotations longues du sud Manche, à vérifier.
- **CC de la Baie du Cotentin**, le cœur des marais du Cotentin et du Bessin : c'est le taux le plus faible (0,76 % par an). C'est cohérent avec les protections des prairies humides et Natura 2000.
- **Les années 2019 et 2023 restent marquées par les artefacts** décrits en T2 : le reclassement de 2018, et les sorties de 2023 (« devenir inconnu » ≈ 10 000 ha en 2023). Le graphique devra les signaler.

## Limites et suites

- **Ces chiffres ne sont pas encore nets du béton.** Une prairie retournée puis artificialisée peut être comptée deux fois avec la partie béton. Il faut croiser avec l'OCS GE (test T5).
- **Les EPCI à cheval sur deux départements** (aucun dans la Manche, mais il y en aura ailleurs) ne seront complets qu'une fois les cinq départements traités.
- **Reste à faire :**
  - affecter les 610 LCP non rattachées ;
  - traiter les quatre autres départements, environ 450 Mo à télécharger ;
  - ajouter 2025, qui n'est pas dans RPG Explorer.
- **Diffusion :** seul le CSV agrégé peut être livré. Les fichiers de `data/raw/` ne sont pas versionnés.
