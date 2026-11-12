# Test T5 : couche des changements OCS GE et croisement « béton × charrue » (Manche)

Date : 18/10/2026. Résultat : **GO**, avec deux réserves de méthode. La couche des changements est légère et exploitable. Le croisement avec les parcelles RPG tourne en 6 secondes. Le double compte avec la charrue est négligeable.

## La donnée

- **Ressource IGN :** `OCS-GE_2-0_DIFF-2019-2022_GPKG_LAMB93_D050_2025-03-10`, téléchargée via data.geopf.fr. L'archive 7z fait **2,4 Mo**. Elle a été vérifiée par MD5 et décompressée avec le `tar` de Windows.
- **Contenu :** `DIFF_D050_2022_2019.gpkg` (9,8 Mo), une seule couche, **15 416 polygones de changement, soit 2 464 ha**.
- **Années pour la Manche : 2019 et 2022**, ce qui confirme l'hypothèse. Les années de départ (2019) existent aussi en GeoPackage complet, à télécharger seulement si besoin.
- **Attributs :** `ID_`, `CS_` (couverture), `US_` (usage) et `OSS_` pour chaque année (2019 et 2022). La géométrie est en EPSG:2154.
- **Pas d'attribut « artificialisé ».** Le statut est reconstitué avec une **approximation du décret 2023-1096**, codée dans `src/beton_charrue_epci.py` :
  - CS1.1.1.x (imperméabilisé) ou CS1.1.2.x (stabilisé ou composite) ;
  - ou CS2.2.1 (herbacé) avec un usage résidentiel, de production secondaire ou tertiaire, de transport ou de logistique, ou en chantier ou abandonné (US2, US3, US5, US235, US4.x, US6.1, US6.2).
  - **À valider** contre le produit officiel « OCS GE Artificialisation » de l'IGN (sur data.gouv).

## Résultats pour la Manche, 2019 → 2022

**Béton :** 5 840 polygones nouvellement artificialisés, soit **822 ha en 3 ans (≈ 274 ha/an)**.
- Couverture et usage en 2019 :
  - herbacé agricole (CS2.2.1 / US1.1) : **657 ha, soit 80 %** ;
  - herbacé sans usage : 94 ha ;
  - ligneux sans usage : 21 ha.

**Ce que le béton a pris, d'après le RPG de 2019 :**

| RPG 2019 | ha bétonnés |
|---|---|
| Prairie permanente | **198** |
| Prairie temporaire | 28 |
| Cultures et fourrage | 101 |
| Hors des parcelles RPG déclarées | **496**, dont **334 ha d'herbacé agricole non déclaré** |

Les 334 ha d'herbe agricole hors PAC sont très probablement des **prairies non déclarées** : petits éleveurs, chevaux de loisir, pâtures communales. Ils sont invisibles côté charrue, mais bien réels côté béton. Il faut les afficher comme « prairies probables hors PAC ».

**Double compte béton / charrue :** parmi les prairies permanentes de 2019 touchées par le béton, voici leur classe RPG en 2022 :
- non déclarées : 123 ha ;
- toujours déclarées en prairie permanente : 60 ha (polygone en bordure de parcelle) ;
- **culture : 1 ha seulement**.

Le recouvrement avec le retournement strict est donc **négligeable**. Il porte surtout sur le « devenir inconnu ». Règle retenue : le béton est retiré de la charrue et du devenir inconnu. Le script retire déjà la surface bétonnée de chaque LCP.

**Charrue sur la même fenêtre** (paires 2019→20, 2020→21, 2021→22), nette du béton : **11 069 ha** de prairies permanentes passées en culture, dont **4 442 ha de prairies anciennes**. C'est cohérent avec le test T2b.

## Bilan par EPCI, 2019 → 2022

| EPCI | Béton total (ha) | Béton sur PP | Béton hors RPG | Charrue, toutes PP | Charrue, PP anciennes | Prairies perdues (PP) | Part du béton |
|---|---|---|---|---|---|---|---|
| CA Mont-Saint-Michel-Normandie | 207 | 35 | 120 | 3 303 | 886 | 3 338 | 1,1 % |
| CA du Cotentin | 210 | 55 | 129 | 2 418 | 1 117 | 2 473 | 2,2 % |
| CA Saint-Lô Agglo | 99 | 30 | 60 | 1 517 | 704 | 1 547 | 1,9 % |
| CC Coutances Mer et Bocage | 90 | 19 | 56 | 1 171 | 624 | 1 190 | 1,6 % |
| CC Côte Ouest Centre Manche | 65 | 10 | 46 | 886 | 317 | 896 | 1,1 % |
| CC de la Baie du Cotentin | 37 | 17 | 16 | 681 | 363 | 698 | 2,4 % |
| CC de Villedieu Intercom | 35 | 15 | 13 | 670 | 226 | 685 | 2,3 % |
| CC de Granville, Terre et Mer | 80 | 17 | 56 | 424 | 206 | 441 | 3,8 % |
| **Manche** | **822** | **198** | **496** | **11 069** | **4 442** | **11 267** | **1,8 %** |

Fichier : `data/processed/beton_charrue_epci_50.csv`.

## Ce qu'il faut retenir pour le produit

- **Sur 2019-2022 dans la Manche, la charrue a pris 8 à 56 fois plus de prairies que le béton**, selon les définitions :
  - au plus bas : 198 ha de prairies permanentes RPG bétonnées, face à 11 069 ha retournés, toutes prairies permanentes confondues ;
  - au plus haut : 532 ha (198 + 334 ha d'herbe hors PAC), face à 4 442 ha de prairies anciennes retournées.
  - **La part du béton dans les pertes de prairies va donc de 2 % à 11 %.**
- **Cette part est plus faible que les 15 % de l'étude Agreste** pour la Manche (2008-2019). Ce n'est pas contradictoire : Agreste fait un bilan net, sur des sources OSCOM, prairies temporaires incluses. Il faut le dire comme ça dans le pitch. **Toujours afficher la fourchette, jamais un seul chiffre.**
- **Le module charrue est indispensable** : sans lui, l'outil verrait moins d'un vingtième des pertes de prairies dans la Manche.
- **Volumes :** 2,4 Mo d'archive par département pour le béton, quelques secondes de calcul. Le critère de sobriété est facilement tenu.

## Réserves et suites

1. ~~Valider la règle d'artificialisation~~ **Fait (test T5b).** La règle retrouvait 97,5 % de l'officiel, mais le script utilise désormais la couche officielle IGN : 782 ha, dont 197 ha sur des prairies permanentes, et une part du béton de 1,7 %. Les chiffres de ce compte rendu correspondent à l'ancienne règle.
2. **Fenêtres différentes selon les départements :** 2019→2022 pour la Manche, l'Eure et la Seine-Maritime ; 2020→2023 pour le Calvados et l'Orne. Il faudra annualiser (ha/an) avant toute comparaison régionale.
3. **Le béton hors RPG** (496 ha, dont 334 ha d'herbe) ne peut être qualifié que par l'OCS GE. Il faudra ajouter les autres croisements prévus : haies, ZNIEFF, zones potentiellement humides.
4. **Unité minimale de collecte de l'OCS GE :** les petits changements échappent à la couche. C'est à documenter dans la page de méthode.
5. **Même limite que T2b :** les communes sont rattachées avec les contours geo.api, et environ 1 % des parcelles ne sont pas rattachées.
