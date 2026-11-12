# Pressions humaines sur la biodiversité : jeux de données nationaux et européens utilisables en Normandie

Périmètre : jeux de données ouverts produits par des organismes nationaux (IGN, Cerema, MTE/Géorisques/BRGM/INERIS, RTE/ODRÉ, INSEE, Météo-France) ou européens (EEA, Copernicus). Les jeux déjà connus de l'équipe sont exclus (CORINE Land Cover, RPG, haies IGN, friches et consommation foncière EPF Normandie, Phytatmo). Vérifications faites le 17/10/2026, via l'API data.gouv.fr, le flux de téléchargement IGN (data.geopf.fr) et des appels directs à l'API Géorisques.

## Tableau de synthèse (13 jeux retenus et vérifiés, plus 2 signalés)

| # | Jeu de données (nom exact) | Producteur | Accès | Format | Résolution / maille | Couverture temporelle / dernière MAJ | Licence | Normandie | Volume |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OCS GE (nouvelle génération, v2.0) + OCS GE Artificialisation | IGN (financement DGALN) | data.gouv : https://www.data.gouv.fr/datasets/ocs-ge et https://www.data.gouv.fr/datasets/ocs-ge-artificialisation ; flux de téléchargement : https://data.geopf.fr/telechargement/resource/OCSGE?zone=D014 (remplacer D014 par D027, D050, D061 ou D076) ; WMS/WMTS data.geopf.fr | GPKG (Lambert-93), WMS/WMTS | Vecteur grande échelle, 2 dimensions (couverture et usage) | 2 millésimes par département, plus une couche DIFF (changements) ; fiches data.gouv mises à jour le 15/10/2026 | Licence Ouverte 2.0 | **5/5 départements**, 2 millésimes + DIFF (détail ci-dessous) | non mesuré (un GPKG par département) |
| 2 | CoSIA (Couverture du Sol par IA), v1.0 | IGN | https://www.data.gouv.fr/datasets/cosia ; https://data.geopf.fr/telechargement/resource/COSIA?zone=D0xx ; WMS/WMTS IGNF_COSIA_2017-2020 / 2021-2023 / 2024-2026 | GPKG, WMS/WMTS | Dérivée d'orthophotos à 20 cm ; 15 classes (bâtiment, zone imperméable/perméable, piscine, serre, sol nu, conifère, feuillu, broussaille, pelouse, culture, terre labourée, vigne…) | 2 ou 3 millésimes par département (MAJ 14/10/2026) | Licence Ouverte 2.0 | **5/5** ; l'Orne n'a que 2 millésimes (2020, 2023) | non mesuré |
| 3 | Consommation d'espaces naturels, agricoles et forestiers du 1er janvier 2011 au 1er janvier 2025 (CONSOENAF 2011-2025) | Cerema (fichiers fonciers, portail de l'artificialisation) | https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61 | CSV (31,1 Mo), XLSX (24,3 Mo), GPKG (jusqu'à 436,9 Mo) | Commune + carroyage 1 km x 1 km ; flux annuels | Flux annuels 2011-2012 à 2024-2025 ; jeu mis à jour le 08/10/2026, fichiers du 24/07/2026 | Licence Ouverte 2.0 | France entière | ~31 Mo (CSV) |
| 4 | BD TOPO® v3.5 | IGN | https://www.data.gouv.fr/datasets/bd-topo-r ; téléchargement par département : https://geoservices.ign.fr/bdtopo | SHP, GPKG, SQL | Vecteur 3D, précision métrique | Mise à jour trimestrielle ; dernière MAJ 07/10/2026 ; « BD TOPO Historique » disponible aussi | Licence Ouverte 2.0 | France entière | plusieurs Go par département (non vérifié) |
| 5 | Copernicus HRL Imperviousness : Imperviousness Density 2024 (10 m et 100 m), Impervious Built-Up 2024, Imperviousness Change 2021-2024 (20 m) | EEA / Copernicus Land Monitoring Service | https://land.copernicus.eu/en/products/high-resolution-layer-imperviousness | GeoTIFF (tuiles EEA 100 x 100 km) | 10 m (densité), 20 m (changement) | 2006 à 2024, mise à jour tous les 3 ans | Accès libre et gratuit Copernicus ; **compte EU Login requis pour le téléchargement** (non vérifié ici) | Europe entière | ~Go par tuile |
| 6 | Installations industrielles (ICPE soumises à autorisation ou enregistrement) | MTE / Géorisques (BRGM), données DREAL | Base : https://www.georisques.gouv.fr/donnees/bases-de-donnees ; API : `https://georisques.gouv.fr/api/v1/installations_classees?code_insee=…` (testée, sans clé) ; WFS : https://georisques.gouv.fr/services | CSV, JSON (API), WMS/WFS | Point (établissement), avec SIRET, NAF, régime, Seveso, IED, et indicateurs booléens bovins/porcs/volailles/carrière/éolienne/industrie | En continu | Etalab 2.0 (mention du site Géorisques) | France entière (hors installations soumises à simple déclaration) | ~137 000 installations au niveau national (source tierce, non officielle) |
| 7 | Registre national des émissions polluantes (IREP), « Installations industrielles rejetant des polluants » | MTE / INERIS via Géorisques | https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants | CSV/Excel par année (zip de 8 fichiers : émissions, établissements, prélèvements, rejets, déchets dangereux et non dangereux) | Établissement (point) ; tonnes par polluant et par milieu (air, eau, sol) | Annuel ; MAJ semestrielle ; la fiche indique « dernière mise à jour décembre 2024 » | Etalab 2.0 | France entière | non mesuré |
| 8 | Industrial Reporting under the IED 2010/75/EU and E-PRTR Regulation (EC) No 166/2006 | EEA | Enregistrement SDI : https://sdi.eea.europa.eu/catalogue/srv/eng/catalog.search#/metadata/9405f714-8015-4b5b-a63c-280b82861b3d ; https://industry.eea.europa.eu/industrial-emissions/dataset | Base SQL/Access, CSV, GPKG (« various formats ») | Installation (point) | 2007-2024 dans la version la plus récente ; métadonnées mises à jour le 25/09/2026 | Libre réutilisation EEA (licence non extraite) | Europe entière | non mesuré |
| 9 | Sites et sols pollués : CASIAS (anciens sites industriels), SSP/ex-BASOL, SIS (secteurs d'information sur les sols) | MTE / BRGM via Géorisques | CSV CASIAS : https://mapsref.brgm.fr/wxs/georisques/georisques_dl?&service=wfs&version=2.0.0&request=getfeature&typename=etablissement_point&outputformat=csvtext ; API : `https://georisques.gouv.fr/api/v1/ssp?code_insee=…` (testée) ; fiche data.gouv : https://www.data.gouv.fr/datasets/carte-des-anciens-sites-industriels-et-activites-de-services-casias | CSV, JSON, WMS/WFS | Point (site) ; SIS en polygones | MAJ quotidienne (SIS, SSP) | Etalab 2.0 (licence « non précisée » sur la fiche data.gouv) | France entière ; CASIAS exhaustif seulement pour les activités antérieures à 2005 | Rouen seule : 572 entrées CASIAS |
| 10 | Registre national des installations de production et de stockage d'électricité (au 31/08/2026) | RTE / ODRÉ (Open Data Réseaux Énergies) | https://www.data.gouv.fr/datasets/5bfcc5a006e3e744e304ccf0 ; API : https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/registre-national-installation-production-stockage-electricite-agrege/exports/csv | CSV, JSON, API Opendatasoft | Installation (localisée à la commune) ; installations de moins de 36 kW agrégées | Millésimes semestriels ou trimestriels (31/12/2023, 31/12/2024, 31/12/2025, 30/06/2026, 31/08/2026) ; MAJ 13/10/2026 | Licence Ouverte 2.0 | France entière | ~42 Mo (CSV, d'après un listing data.gouv) |
| 11 | Éolien terrestre (parcs et éoliennes) | MTE / Géorisques | https://www.georisques.gouv.fr/donnees/bases-de-donnees (onglet « Eolien terrestre ») | CSV | Éolienne (point) et parc, avec le cycle de vie du parc | En continu | Etalab 2.0 | France entière | non mesuré |
| 12 | Trafic moyen journalier annuel sur le réseau routier national (TMJA) | Ministère de la Transition écologique | https://www.data.gouv.fr/datasets/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national ; SHP 2024 : https://static.data.gouv.fr/resources/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national/20250818-100425/tmja-rrnc-2024-shp.zip | SHP (zip), CSV | Section de route nationale non concédée, avec TMJA et % de poids lourds | 2019 puis 2022, 2023 et 2024 ; MAJ 18/08/2025 | Licence Ouverte (fr-lo) | Routes nationales non concédées uniquement (pas les autoroutes concédées A13, A28, A29, A84… ni le réseau départemental) | 2,2 Mo (SHP 2024) |
| 13 | Capacités d'hébergements touristiques (et Fréquentation des hébergements touristiques) | INSEE | https://www.data.gouv.fr/datasets/capacites-dhebergements-touristiques (fichier Melodi : https://api.insee.fr/melodi/file/DS_TOUR_CAP/DS_TOUR_CAP_2026_CSV_FR) ; https://www.data.gouv.fr/datasets/frequentation-des-hebergements-touristiques | CSV | Commune (et EPCI, département…) ; chambres, lits, emplacements de camping | Annuel, millésime 2026 ; MAJ 09/10/2026 | Licence Ouverte 2.0 | France entière | petit |
| 14 (signalé) | Indicateur national de l'érosion côtière | Cerema | https://www.data.gouv.fr/datasets/indicateur-national-de-lerosion-cotiere-1 → https://www.geolittoral.developpement-durable.gouv.fr/telechargement-en-ligne-donnees-geolittoral-a802.html#indi_nat_erosion | SHP | Tronçons de trait de côte, au 1/100 000 | **Version 2018 (ancienne)** ; évolution sur au moins 50 ans | « Non précisée » sur data.gouv (licence à vérifier) | Toute la côte normande (métropole entière) | petit |
| 15 (signalé) | DRIAS, les futurs du climat (projections climatiques régionalisées) | Météo-France (avec IPSL, CERFACS, CNRM) | https://www.drias-climat.fr/ (fiche data.gouv : https://www.data.gouv.fr/datasets/drias-projections-climatiques-pour-ladaptation-de-nos-societes) | NetCDF/CSV (portail) | Grille ~8 km (SAFRAN) (non vérifié) | Fiche data.gouv mise à jour le 29/04/2024 | Licence Ouverte (fr-lo) ; un compte gratuit est probablement nécessaire pour télécharger (non vérifié) | France entière | variable |

## 1. Artificialisation et consommation d'espace

### Takeaway
En octobre 2026, la Normandie est entièrement couverte par OCS GE v2.0 (2 millésimes et une couche de changements par département) et par CoSIA (3 millésimes, sauf l'Orne qui en a 2). La série Cerema CONSOENAF fournit des flux annuels de consommation d'ENAF à la commune et au carreau de 1 km, de 2011 à 2025. Ces trois jeux forment le socle quantitatif de la pression d'artificialisation. Copernicus HRL Imperviousness 2024 (10 m) apporte une vision comparable au reste de l'Europe.

### Cited Findings
- Le flux de téléchargement IGN (paramètre `zone=`) liste, pour **OCS GE v2.0** : Calvados D014 millésimes 2020 et 2023, plus DIFF-2020-2023 (publiée le 17/04/2025) ; Eure D027 2019 et 2022, plus DIFF-2019-2022 (12/06/2025) ; Manche D050 2019 et 2022, plus DIFF (10/03/2025) ; Orne D061 2020 et 2023, plus DIFF (12/03/2025) ; Seine-Maritime D076 2019 et 2022, plus DIFF (12/06/2025). Tous en GPKG Lambert-93 — [data.geopf.fr OCSGE](https://data.geopf.fr/telechargement/resource/OCSGE?zone=D014)
- Le même flux liste, pour **CoSIA v1.0** : D014 2020, 2023 et 2026 ; D027 2019, 2022 et 2025 ; D050 2019, 2022 et 2025 ; D061 2020 et 2023 seulement ; D076 2019, 2022 et 2025. Tous en GPKG Lambert-93 — [data.geopf.fr COSIA](https://data.geopf.fr/telechargement/resource/COSIA?zone=D050)
- OCS GE est décrite comme un « référentiel national » d'occupation du sol à 2 dimensions (couverture et usage), utilisé pour piloter l'artificialisation au sens de la loi Climat et Résilience (art. L.101-2-1 du code de l'urbanisme) ; licence Ouverte 2.0 ; fiche mise à jour le 15/10/2026. Des services WMS/WMTS existent pour les couches ARTIF 2016-2017 à 2024-2026, ainsi que des couches « ARTIFICIALISATION-EXEMPTIONS » — [data.gouv OCS GE Artificialisation](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation) ; [data.gouv OCS GE](https://www.data.gouv.fr/datasets/ocs-ge)
- CoSIA est un sous-produit de la production OCS GE, constitué de « prédictions » IA en 15 classes, dont bâtiment, zone imperméable, serre et sol nu — [data.gouv CoSIA](https://www.data.gouv.fr/datasets/cosia). Résolution source de 20 cm par pixel ; marges d'erreur publiées par département et par classe — [IGN, documentation technique CoSIA](https://geoservices.ign.fr/sites/default/files/2025-04/Cosia_Documentation_Technique_IGN_2023.pdf). La documentation de décembre 2025 (v1.0) compte 15 classes, contre 16 dans la version 2023 — [DC CoSIA 1.0](https://geoservices.ign.fr/sites/default/files/2025-12/DC_CoSIA_1-0.pdf)
- CONSOENAF 2011-2025 (Cerema) : licence Ouverte 2.0 ; mailles commune et carreaux de 1 km ; pas de temps annuel ; mis à jour le 08/10/2026 ; CSV de 31,1 Mo, XLSX de 24,3 Mo, plusieurs GPKG (dont un de 436,9 Mo) — [data.gouv CONSOENAF](https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61). La version 2009-2023 est archivée — [data.gouv COENAF 2009-2023](https://www.data.gouv.fr/datasets/consommation-despaces-naturels-agricoles-et-forestiers-du-1er-janvier-2009-au-1er-janvier-2023). La série cumulée 2009-2024 est aussi publiée par l'Observatoire des territoires — [Observatoire des territoires](https://www.observatoire-des-territoires.gouv.fr/consommation-despaces-naturels-agricoles-et-forestiers-enaf-entre-le-1er-janvier-2009-et-le-1er)
- Les données Cerema issues des fichiers fonciers servent au suivi officiel de l'objectif de réduction de moitié de la consommation d'ENAF (2011-2021 par rapport à 2021-2031) — [doc-datafoncier Cerema](https://doc-datafoncier.cerema.fr/doc/export/509)
- BD TOPO v3.5 : description vectorielle 3D de précision métrique (thèmes bâti, transport, hydrographie, occupation du sol, services et activités, zones réglementées) ; mise à jour trimestrielle ; dernière MAJ 07/10/2026 ; licence Ouverte 2.0 ; téléchargement par département ou par région (SHP, GPKG, SQL) — [data.gouv BD TOPO](https://www.data.gouv.fr/datasets/bd-topo-r)
- Copernicus HRL Imperviousness : les produits suivants sont catalogués sur l'API CLMS : Imperviousness Density 2024 (10 m et 100 m), Impervious Built-Up 2024, Imperviousness Change 2021-2024 (20 m et 100 m) et Imperviousness Change Classified 2021-2024 — [CLMS Imperviousness Density 2024](https://land.copernicus.eu/api/en/products/high-resolution-layer-imperviousness/imperviousness-density-2024). Le millésime 2021 a introduit une méthode U-Net et une couche de changement du bâti 2018-2021 — [CLMS news HRL IMD 2021](https://land.copernicus.eu/en/news/product-update-high-resolution-layer-imperviousness-2021)

### Inferences
- Pour le problème 1 (restauration), la couche OCS GE DIFF donne directement les polygones artificialisés entre deux millésimes, environ 3 ans d'écart, à grande échelle. CONSOENAF donne une série longue et homogène (2011-2025) à la commune ou au carreau de 1 km, adaptée à un indicateur de politique publique (problème 2).
- Les millésimes ne sont pas synchronisés : Eure, Manche et Seine-Maritime sont en 2019/2022, Calvados et Orne en 2020/2023. Une comparaison régionale doit tenir compte de ce décalage d'un an.
- BD TOPO (tronçons de route et de voie ferrée, bâti) permet de calculer des indicateurs de fragmentation, comme la taille effective de maille (effective mesh size) ou la densité de routes par maille.
- CoSIA sert d'indicateur complémentaire de densité de surfaces imperméables et de serres, au 20 cm d'origine. C'est une prédiction IA, avec des erreurs à prendre en compte.

### Gaps
- Urban Atlas (Copernicus) non vérifié. Il ne couvre de toute façon que les aires urbaines fonctionnelles (Caen, Rouen, Le Havre, Cherbourg…), pas toute la région.
- Volumes des GPKG OCS GE et CoSIA par département non mesurés.
- La nécessité d'un compte EU Login pour télécharger les HRL Copernicus n'a pas été vérifiée lors de cette session (c'était le cas jusqu'ici d'après les connaissances antérieures).
- Le portail artificialisation.developpement-durable.gouv.fr n'a pas été consulté directement. Les données Cerema passent par data.gouv.fr.

## 2. Industrie et pollution

### Takeaway
Géorisques expose en open data, sans clé (testé le 17/10/2026), les ICPE soumises à autorisation ou enregistrement, les sites et sols pollués (CASIAS, SSP/ex-BASOL, SIS), le registre IREP et l'éolien terrestre. Tout est accessible par téléchargement CSV, par WFS ou par une API REST interrogeable par code INSEE. L'équivalent européen est la base Industrial Reporting de l'EEA (IED et E-PRTR, 2007-2024). Pour les stations d'épuration, aucun jeu national unique à jour n'a été trouvé.

### Cited Findings
- La page « Bases de données » de Géorisques liste 18 bases, dont : CASIAS (CSV) ; Éolien terrestre (parcs et éoliennes, avec le cycle de vie du parc) ; Installations industrielles (ICPE soumises à autorisation ou enregistrement, en fonctionnement ou en cessation) ; Installations industrielles rejetant des polluants (IREP) ; SIS (MAJ quotidienne, CSV) ; Sites et sols pollués (ex-BASOL). Des services WMS/WFS sont proposés sur https://georisques.gouv.fr/services. Un bandeau signale : « Dans un contexte d'attaque informatiques, des restrictions d'accès pour certaines localisations géographiques sont appliquées » — [Géorisques bases de données](https://www.georisques.gouv.fr/donnees/bases-de-donnees)
- IREP : « mis à jour 2 fois par an » ; données par année, à l'échelle nationale, dans un zip de 8 fichiers (émissions, établissements, prélèvements, rejets, production et traitement de déchets dangereux et non dangereux) ; source INERIS ; couverture métropole, Corse et DROM ; « Date de dernière mise à jour décembre 2024 » — [Géorisques IREP](https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants)
- Test de l'API `https://georisques.gouv.fr/api/v1/installations_classees?code_insee=14118` (Caen), sans clé : 47 résultats. Champs renvoyés : raisonSociale, codeNaf, longitude/latitude, bovins/porcs/volailles/carriere/eolienne/industrie (booléens), statutSeveso, ied, regime, serviceAIOT (« DREAL Normandie »), siret — [API Géorisques](https://georisques.gouv.fr/api/v1/installations_classees?code_insee=14118)
- Test de l'API `https://georisques.gouv.fr/api/v1/ssp?code_insee=76540` (Rouen) : 572 entrées CASIAS, avec activité principale, statut, date_maj et un lien vers la fiche BRGM — [API Géorisques SSP](https://georisques.gouv.fr/api/v1/ssp?code_insee=76540)
- La base ICPE de Géorisques ne recense pas les installations soumises à déclaration. CASIAS (ex-BASIAS) n'est complet que pour les activités antérieures à 2005 — [Préfecture du Rhône, tableau des sources](https://www.rhone.gouv.fr/contenu/telechargement/49441/273079/file/tableau_source_information.pdf)
- La fiche data.gouv CASIAS (BRGM) donne un export CSV direct par WFS (mapsref.brgm.fr) et des services WMS/WFS SSP_ETABLISSEMENT ; licence « non précisée » sur data.gouv — [data.gouv CASIAS](https://www.data.gouv.fr/datasets/carte-des-anciens-sites-industriels-et-activites-de-services-casias)
- L'ancienne « Base des installations classées (ICPE) » sur data.gouv n'est plus à jour depuis le 28/02/2021 — [data.gouv ICPE (obsolète)](https://www.data.gouv.fr/datasets/base-des-installations-classees-icpe)
- EEA « Industrial Reporting under the IED 2010/75/EU and E-PRTR Regulation (EC) No 166/2006 » : la version la plus récente couvre 2007-01-01 à 2024-12-31 (métadonnées datées du 25/09/2026). Contenu : localisation et données administratives des grands complexes industriels, rejets et transferts de polluants, transferts de déchets, données des grandes installations de combustion (LCP) — [EEA SDI record](https://sdi.eea.europa.eu/catalogue/srv/eng/catalog.search#/metadata/9405f714-8015-4b5b-a63c-280b82861b3d) ; [EEA Industrial emissions portal](https://industry.eea.europa.eu/industrial-emissions/dataset)
- Stations d'épuration : le jeu data.gouv « Assainissement » est en réalité un jeu de la DDTM de l'Eure (STEU et zones de traitement), moissonné et daté du 15/11/2024. La couche STEU de l'Eure intègre la conformité 2024 au titre de 2023. Ces données proviennent du portail d'information sur l'assainissement communal (référentiel ERU) — [data.gouv Assainissement](https://www.data.gouv.fr/datasets/assainissement) ; [STEU de l'Eure](https://data.gouv.fr/en/datasets/les-stations-de-traitement-des-eaux-usees-de-leure)

### Inferences
- Pour une pression industrielle par maille, on peut combiner la densité d'ICPE (API, avec filtres Seveso, IED et élevages) et les tonnages IREP par milieu (air et eau). L'E-PRTR de l'EEA permet de comparer avec d'autres régions européennes. Le chevauchement entre IREP et E-PRTR est important : il faut dédoublonner.
- Le champ booléen `carriere` de l'API ICPE permet d'extraire les carrières autorisées en Normandie, ce qui répond en partie au besoin « extraction ».
- Les élevages ICPE (bovins, porcs, volailles) peuvent servir de proxy de la pression agricole intensive, ponctuelle.
- Les restrictions géographiques d'accès à Géorisques peuvent gêner des participants situés hors de France ou derrière certains VPN.

### Gaps
- Le portail national de l'assainissement communal (ROSEAU / « assainissement.developpement-durable.gouv.fr ») n'a pas pu être consulté : la page testée renvoie une 404. Pas de lien vérifié vers un export national des STEU avec leur conformité ERU.
- Le volume de la base IREP et le millésime de données le plus récent (2023 ou 2024) ne sont pas confirmés. La fiche indique « décembre 2024 » comme dernière mise à jour, ce qui est peut-être obsolète par rapport à une MAJ semestrielle.
- La licence exacte des fichiers EEA Industrial Reporting n'a pas été extraite.

## 3. Extraction et énergie

### Takeaway
Les installations de production d'électricité (éolien, photovoltaïque au sol, hydraulique…) sont couvertes par le registre national ODRÉ/RTE (au 31/08/2026), localisé à la commune, et par la base Éolien terrestre de Géorisques. Pour les carrières, aucun jeu national dédié n'a été trouvé : les données sont soit régionales (DREAL), soit à extraire de l'ICPE Géorisques (champ `carriere`).

### Cited Findings
- « Registre national des installations de production et de stockage d'électricité (au 31/08/2026) », organisation Open Data Réseaux Énergies, licence Ouverte 2.0, mis à jour le 13/10/2026. Exports CSV et JSON par l'API Opendatasoft — [data.gouv registre ODRÉ](https://www.data.gouv.fr/datasets/5bfcc5a006e3e744e304ccf0)
- RTE produit ce registre (art. L142-9-1 du code de l'énergie) à partir des données transmises par les gestionnaires de distribution. Millésimes précédents : 31/12/2023, 31/12/2024, 31/12/2025 et 30/06/2026. Un CSV d'environ 42 Mo est signalé — [data.gouv registre 30/06/2026](https://www.data.gouv.fr/datasets/registre-national-des-installations-de-production-et-de-stockage-delectricite-au-30-06-2026) ; [registre 31/12/2025](https://www.data.gouv.fr/datasets/69c4af4e5c9f9567df414fc6)
- Géorisques diffuse une base « Eolien terrestre » : parcs éoliens avec leur cycle de vie, et éoliennes composant chaque parc — [Géorisques bases de données](https://www.georisques.gouv.fr/donnees/bases-de-donnees)
- Les recherches data.gouv sur « carrières » ne renvoient que des jeux régionaux ou locaux (Bretagne, Bourgogne-Franche-Comté, Île-de-France, Hauts-de-France, Cantal…), pas de jeu national — [data.gouv recherche « carrières »](https://www.data.gouv.fr/datasets/carrieres-actives-definies-par-le-schema-regional-des-carrieres-de-bretagne)

### Inferences
- Le registre ODRÉ est localisé à la commune, pas au point. Pour localiser précisément les parcs éoliens, mieux vaut utiliser Géorisques (éoliennes en points). Pour les parcs solaires au sol, il faut croiser avec OCS GE ou CoSIA, ou avec la BD TOPO (thème « services et activités »).
- Pour les carrières, l'option nationale reste l'API ICPE (`carriere=true`). Les couches DREAL Normandie (schéma régional des carrières) sont hors périmètre « national » mais complémentaires.

### Gaps
- Pas de jeu national open data dédié aux carrières (BRGM, schémas régionaux) vérifié dans cette session.
- Pas de jeu national vérifié qui donne l'emprise surfacique des parcs photovoltaïques au sol.

## 4. Pollution lumineuse

### Takeaway
Aucun jeu national français de pollution lumineuse en open data couvrant la Normandie n'a été trouvé. Sur data.gouv, les produits existants sont locaux ou régionaux (Métropole du Grand Paris, Occitanie, Bretagne, Aix-Marseille). Les sources satellitaires globales exigent un compte (NASA Black Marble) ou sont sous licence non commerciale avec formulaire de demande (World Atlas, Falchi et al., 2016).

### Cited Findings
- Les recherches « pollution lumineuse » et « trame noire » sur data.gouv ne renvoient que des jeux locaux ou régionaux : Métropole du Grand Paris (radiance, indice NSB), modélisation de la pollution lumineuse en Occitanie, trame noire en Bretagne, Aix-Marseille-Provence — [data.gouv modélisation pollution lumineuse Occitanie](https://www.data.gouv.fr/datasets/modelisation-de-la-pollution-lumineuse-en-occitanie) ; [Trame noire en Bretagne](https://www.data.gouv.fr/datasets/trame-noire-en-bretagne-atlas-cartographiques)
- NASA Black Marble (VNP46, VJ146) : composites de lumière nocturne quotidiens, mensuels et annuels, au format HDF5, archivés sur LAADS DAAC. Le téléchargement automatisé (blackmarblepy) nécessite un jeton LAADS (compte Earthdata) — [NASA Earthdata Black Marble](https://www.earthdata.nasa.gov/data/projects/black-marble) ; [blackmarblepy PyPI](https://pypi.org/project/blackmarblepy)
- New World Atlas of Artificial Night Sky Brightness : GeoTIFF d'environ 2,9 Go à 30 secondes d'arc. Licence CC BY-NC 4.0 depuis novembre 2019. Accès FTP sur formulaire de demande — [B2FIND record](https://b2find.eudat.eu/dataset/df8cd562-df6a-51bf-ad64-7421cf8c8623) ; [GFZ press](https://www.gfz.de/en/press/news/details/new-atlas-of-light-pollution)

### Inferences
- Pour la Normandie, la voie la plus réaliste est d'utiliser les composites annuels VIIRS (Black Marble VNP46A4, ou EOG VNL). Les comptes nécessaires sont gratuits mais obligatoires : c'est à signaler comme « pas totalement open ». Le World Atlas peut servir à des fins non commerciales, ce qui est acceptable pour un datathon, sous réserve de la licence NC.

### Gaps
- Les produits de La Nuit est Belle, AVEX et Cerema (trame noire nationale) n'ont pas été vérifiés. Aucun jeu national ouvert n'a été trouvé sur data.gouv.
- Les conditions d'accès d'EOG (Colorado School of Mines, VIIRS Nighttime Lights) n'ont pas été vérifiées. Une inscription est probablement requise.

## 5. Pression liée aux transports

### Takeaway
Les TMJA du réseau routier national non concédé sont ouverts (SHP et CSV, millésimes 2019, 2022, 2023 et 2024). Ils ne couvrent ni les autoroutes concédées ni les routes départementales. Pour la densité de réseau, la BD TOPO (thème transport) est la référence. Aucun jeu national ouvert de collisions faune-véhicules n'a été trouvé.

### Cited Findings
- TMJA : moyenne annuelle du nombre de véhicules par jour, tous sens confondus, généralement accompagnée d'un pourcentage de poids lourds, par section (nom de route, longueur, coordonnées de début et de fin). Ressources : TMJA_RRNc_2024 (SHP 2,2 Mo, CSV 0,2 Mo), 2023, 2022 et 2019. Licence Ouverte ; MAJ 18/08/2025 — [data.gouv TMJA](https://www.data.gouv.fr/datasets/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national)
- La DIR Nord-Ouest publie un bilan des trafics 2024 sur son réseau national (environ 1 000 km, 11 départements, environ 150 capteurs) — [DIRNO bilan trafic 2024](https://www.dir.nord-ouest.developpement-durable.gouv.fr/IMG/pdf/20251106_bilan_trafic_2024_dirno.pdf)
- Une recherche « collisions faune » sur data.gouv ne donne aucun résultat (0 jeu) — [data.gouv](https://www.data.gouv.fr/datasets/?q=collisions%20faune)

### Inferences
- Pour une pression routière régionale complète, on peut pondérer la densité de tronçons BD TOPO par importance (attribut nature et importance) et utiliser le TMJA seulement là où il existe. Le suffixe « RRNc » des fichiers indique le réseau non concédé : les grandes autoroutes normandes concédées (A13, A28, A29, A84 partiellement) n'ont pas de TMJA dans ce jeu.

### Gaps
- Pas de données ouvertes de trafic sur les autoroutes concédées (SANEF, ALIS, etc.) ni sur le réseau départemental national vérifiées.
- Pas de données nationales ouvertes sur les collisions avec la faune (l'OFB et les réseaux de naturalistes ont des données, mais elles ne sont pas ouvertes au niveau national d'après cette recherche).

## 6. Pression touristique et récréative

### Takeaway
L'INSEE publie en open data (Licence Ouverte 2.0) les capacités d'hébergement touristique à la commune (millésime 2026) et la fréquentation des hébergements. C'est un proxy simple de la pression touristique, notamment sur le littoral normand.

### Cited Findings
- « Capacités d'hébergements touristiques » (INSEE) : nombre d'établissements, de chambres, de lits et d'emplacements de camping, par type (hôtels, campings, autres) et par nombre d'étoiles ; niveaux géographiques de la commune à la région ; annuel ; couverture 2026 ; MAJ 09/10/2026 ; CSV via l'API Melodi — [data.gouv INSEE capacités](https://www.data.gouv.fr/datasets/capacites-dhebergements-touristiques)
- « Fréquentation des hébergements touristiques » (INSEE), MAJ 04/10/2026, Licence Ouverte 2.0 — [data.gouv INSEE fréquentation](https://www.data.gouv.fr/datasets/frequentation-des-hebergements-touristiques)

### Inferences
- Un ratio lits touristiques / habitants ou lits par km² à la commune est un indicateur direct de pression saisonnière, utile pour le problème 2. La fréquentation n'est probablement pas disponible à la commune (secret statistique), ce qui n'a pas été vérifié.

### Gaps
- Granularité spatiale de la fréquentation non vérifiée.
- Pas de jeu national ouvert de fréquentation des espaces naturels trouvé.

## 7. Changement climatique et exposition côtière

### Takeaway
L'indicateur national de l'érosion côtière du Cerema couvre tout le littoral normand mais date de 2018. DRIAS fournit les projections climatiques régionalisées, avec un accès probablement soumis à inscription.

### Cited Findings
- Indicateur national de l'érosion côtière (Cerema) : évolution de la position du trait de côte sur au moins 50 ans, en métropole et dans 5 DROM. Fiche datée du 28/06/2018 ; licence « non précisée » sur data.gouv ; téléchargement SHP sur Géolittoral — [data.gouv indicateur érosion](https://www.data.gouv.fr/datasets/indicateur-national-de-lerosion-cotiere-1)
- L'indicateur est produit au 1/100 000 à partir de traits de côte relevés sur photos aériennes. Les traits récents viennent de photos de 2005-2014, les anciens de photos de 1920-1957 — [Cerema, spécifications techniques](https://www.geolittoral.developpement-durable.gouv.fr/IMG/pdf/specif-tech-carto-indicateur-erosion.pdf) ; [data.gouv durée analysée](https://www.data.gouv.fr/datasets/duree-analysee-pour-levolution-du-trait-de-cote-1)
- DRIAS met à disposition des projections climatiques régionalisées (IPSL, CERFACS, CNRM-GAME). Fiche data.gouv sous Licence Ouverte (fr-lo), mise à jour le 29/04/2024 — [data.gouv DRIAS](https://www.data.gouv.fr/datasets/drias-projections-climatiques-pour-ladaptation-de-nos-societes)

### Inferences
- Pour le problème 1, l'érosion côtière peut pondérer la priorité de restauration des habitats littoraux (dunes, marais arrière-littoraux), mais les données sont anciennes : les traits de côte ont plus de 10 ans.
- Les couches Géorisques « Retrait-gonflement des argiles 2026 » et « Zonages inondation 2026 » ne sont pas des pressions sur la biodiversité au sens strict, mais elles existent et sont récentes.

### Gaps
- Les modalités d'accès DRIAS (compte, format NetCDF, grille 8 km) n'ont pas été vérifiées dans cette session.
- Les données Météo-France ouvertes (meteo.data.gouv.fr) n'ont pas été vérifiées.
- L'existence d'une mise à jour de l'indicateur national d'érosion postérieure à 2018 n'a pas été vérifiée.
