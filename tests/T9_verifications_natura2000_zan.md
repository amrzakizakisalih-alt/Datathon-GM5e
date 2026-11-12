# T9 : vérification des retournements en Natura 2000 et des projections ZAN extrêmes

Date : 01/11/2026. Résultat : **les deux signaux sont expliqués.** Le premier n'est pas une anomalie de calcul, mais il doit être présenté avec prudence. Le second est maintenant détecté automatiquement par le calcul.

## 1. Retournements de prairies en Natura 2000

**Constat de départ (T8) :** jusqu'à 37 ha par an de prairies permanentes retournées dans des sites Natura 2000, surtout dans l'Orne.

**Analyse dans l'Orne :** 890 ha retournés de 2015 à 2024 (513 événements), dont 685 ha de prairies anciennes.
- **Ils sont concentrés sur un site.** « Bocages et vergers du sud Pays d'Auge » (FR2502014) totalise 542 ha, soit 61 %. Ce site est désigné pour ses vieux arbres, ses haies et ses vergers, qui abritent un coléoptère protégé, et non pour ses prairies. Suivent la Haute vallée de l'Orne (194 ha) et la vallée du Sarthon (88 ha).
- **Les prairies retournées** étaient pour 31 % des prairies en rotation longue (code PRL) et pour 69 % des prairies permanentes (PPH).
- **Ce qui les remplace :** surtout du maïs ensilage (380 ha), puis du blé, du maïs grain et de l'avoine.
- **Ce qu'elles sont devenues :** sur les 685 ha de prairies anciennes retournées, 170 ha étaient revenus en prairie en 2024, 397 ha étaient toujours cultivés et 118 ha n'étaient plus déclarés.

**Croisement avec les « prairies sensibles » de la PAC** (couche BCAE de l'IGN, 10 198 parcelles, 45 659 ha) : la PAC interdit de retourner ces prairies, qui sont situées en Natura 2000.

| Département | Retournés en Natura 2000, 2015-2024 (ha) | dont sur une prairie sensible actuelle (ha) |
|---|---|---|
| Calvados | 318 | 1 |
| Eure | 128 | 18 |
| Manche | 155 | 53 |
| Orne | 890 | 60 |
| Seine-Maritime | 100 | 36 |
| **Normandie** | **≈ 1 590** | **≈ 168** (11 %, ≈ 19 ha/an) |

**Conclusions :**
- **Ce n'est pas une infraction.** L'indicateur `charrue_natura2000` mesure des retournements **dans le périmètre** de sites Natura 2000, qui sont pour l'essentiel autorisés.
- **Le libellé à afficher :** « prairies retournées dans un site Natura 2000 », avec une note expliquant que la plupart des sites concernés ne sont pas désignés pour leurs prairies. Le code le précise désormais (`src/qualite_epci.py`).
- **Pas d'indicateur « prairies sensibles retournées » par EPCI.** Les 168 ha reposent sur un rattachement approximatif (point intérieur de la parcelle) à une couche actuelle, qui ne reflète pas forcément la situation au moment du retournement. Un tel chiffre pourrait être lu comme une accusation d'infraction. On le garde comme ordre de grandeur régional, à discuter avec la DRAAF si elle le souhaite.
- **Pour le volet écologique de l'écran 1, mieux vaut mettre en avant les prairies humides retournées** (zones humides inventoriées et milieux potentiellement humides) : elles sont plus parlantes et moins ambiguës.

## 2. Projections ZAN extrêmes

| EPCI | Projection 2031 (% de l'enveloppe) | Explication |
|---|---|---|
| CC de la Vallée de la Haute Sarthe | 1 046 % | **Un seul flux** : 52,2 ha classés « activité » aux Ventes-de-Bourse en 2022-2023, soit 61 % de la consommation 2021-2025 de l'EPCI, contre 0,8 ha sur toute la période 2011-2021 dans cette commune |
| CC Cœur de Nacre | 479 % | Croissance diffuse et réelle : Courseulles-sur-Mer (31 ha en 2021-2025) et Douvres-la-Délivrande (27 ha), surtout pour l'habitat, sur une base faible (79 ha en 2011-2021) |
| CC Pré-Bocage Intercom | 342 % | Consommation répartie sur plusieurs communes, sans flux dominant (le principal pèse 5 %) |
| CC Cœur Côte Fleurie | 338 % | Idem (Trouville, Tourgéville, Villers-sur-Mer) |

**Le cas des Ventes-de-Bourse, élucidé :**
- **L'OCS GE ne voit que 0,2 ha artificialisé** dans la commune entre 2020 et 2023, alors que les fichiers fonciers comptent 52 ha.
- **L'hypothèse d'une centrale solaire est écartée.** Le registre national des installations électriques (ODRÉ) n'y recense que trois petites installations photovoltaïques, de 89 à 140 kW.
- **La photo aérienne** (Géoportail, comparaison de plusieurs dates, faite par l'équipe le 01/11/2026) montre un grand site clôturé au nord-ouest de la commune, dont la partie terrassée s'étend.
- **Géorisques** identifie ce site : une installation classée de SUEZ RV Normandie, sous régime d'autorisation et marquée « carrière ». C'est vraisemblablement un site de stockage de déchets associé à une carrière (L93 ≈ 496 900 / 6 827 700).
- **L'OCS GE 2023** (couche d'artificialisation complète du département) classe ce site comme artificialisé sur environ 68 ha : de l'herbe à usage de réseaux d'utilité publique et de gestion des déchets (CS2.2.1 / US4.3, 46,6 ha) et des surfaces terrassées (CS1.1.2.1 / US4.3, 20,2 ha). Comme la couche des changements 2020-2023 ne montre rien sur ce site, **il était déjà classé artificialisé en 2020**. Les terrassements visibles transforment de l'herbe en sol terrassé à l'intérieur d'un périmètre déjà artificialisé : aucun changement n'est donc enregistré.
- **Conclusion.** Les 52 ha « consommés » en 2022-2023 dans les fichiers fonciers correspondent, selon toute vraisemblance, à **l'enregistrement tardif au cadastre d'un site déjà en usage**. Ce n'est pas une nouvelle consommation d'espace naturel sur la période. La projection ZAN de l'EPCI doit donc être lue hors de ce flux (404 %), et la mention du flux doit être affichée.
- **Ce que le cas enseigne :** les fichiers fonciers (consommation, base du ZAN jusqu'en 2031) et l'OCS GE (artificialisation) peuvent enregistrer un même site à des dates très différentes. L'alerte `alerte_flux_unique` sert précisément à repérer ces cas.

**Correction :** `src/sobriete_epci.py` calcule désormais, pour chaque EPCI, quatre nouvelles colonnes.
- `principal_flux_2021_2025` : la commune, l'année, la surface et la destination du plus gros flux annuel.
- `part_principal_flux_pct` : la part de ce flux dans la consommation 2021-2025.
- `alerte_flux_unique` : vraie quand ce flux fait au moins 20 ha **et** au moins la moitié de la consommation 2021-2025.
- `projection_2031_pct_hors_principal` : la projection sans ce flux.

**Résultat :**
- **Seule la Vallée de la Haute Sarthe déclenche l'alerte.** Sans son flux principal, elle resterait à 404 %, du fait de sa très faible consommation de référence.
- **Règle d'affichage :** quand l'alerte est levée, afficher la projection hors flux principal à côté de la projection brute, avec la mention du flux.

## Fichiers modifiés

- `src/sobriete_epci.py` : détection du flux principal et projection sans lui.
- `src/qualite_epci.py` : documentation de l'indicateur Natura 2000.
- `data/raw/zonages/prairies_sensibles.geojson` : couche BCAE téléchargée pour cette vérification. Elle n'est pas utilisée dans le calcul.
- `data/raw/ocsge_artif_complet/d61_2023/` : couche d'artificialisation complète de l'Orne en 2023 (140 Mo), téléchargée pour vérifier le site SUEZ. Elle n'est pas utilisée dans le calcul.
- `data/processed/sobriete_epci.csv` et `tableau_regional_epci.csv` : régénérés, 63 colonnes. Les totaux régionaux ne changent pas.
