# Human pressures on biodiversity: national and European datasets usable for Normandy

Scope: open datasets produced by national bodies (IGN, Cerema, MTE/Géorisques/BRGM/INERIS, RTE/ODRÉ, INSEE, Météo-France) or European ones (EEA, Copernicus). Datasets we already use are excluded (CORINE Land Cover, RPG, IGN hedges, EPF Normandie brownfields and land consumption, Phytatmo).

## Summary table (13 datasets kept and checked, plus 2 flagged)

| # | Dataset (exact name) | Producer | Access | Format | Resolution / unit | Time coverage / last update | Licence | Normandy | Volume |
|---|---|---|---|---|---|---|---|---|---|
| 1 | OCS GE (new generation, v2.0) + OCS GE Artificialisation | IGN (funded by DGALN) | data.gouv: https://www.data.gouv.fr/datasets/ocs-ge and https://www.data.gouv.fr/datasets/ocs-ge-artificialisation; download service: https://data.geopf.fr/telechargement/resource/OCSGE?zone=D014 (replace D014 with D027, D050, D061 or D076); WMS/WMTS data.geopf.fr | GPKG (Lambert-93), WMS/WMTS | Large-scale vector, 2 dimensions (cover and use) | 2 vintages per department, plus a DIFF (change) layer; data.gouv pages updated 15 Oct 2026 | Licence Ouverte 2.0 | **5/5 departments**, 2 vintages + DIFF (details below) | not measured (one GPKG per department) |
| 2 | CoSIA (Couverture du Sol par IA), v1.0 | IGN | https://www.data.gouv.fr/datasets/cosia; https://data.geopf.fr/telechargement/resource/COSIA?zone=D0xx; WMS/WMTS IGNF_COSIA_2017-2020 / 2021-2023 / 2024-2026 | GPKG, WMS/WMTS | Derived from 20 cm orthophotos; 15 classes (building, impervious/pervious surface, swimming pool, greenhouse, bare soil, conifer, broadleaf, scrub, lawn, crop, ploughed land, vineyard…) | 2 or 3 vintages per department (updated 14 Oct 2026) | Licence Ouverte 2.0 | **5/5**; the Orne has only 2 vintages (2020, 2023) | not measured |
| 3 | Consommation d'espaces naturels, agricoles et forestiers du 1er janvier 2011 au 1er janvier 2025 (CONSOENAF 2011-2025) | Cerema (land-tax files, artificialisation portal) | https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61 | CSV (31.1 MB), XLSX (24.3 MB), GPKG (up to 436.9 MB) | Commune + 1 km × 1 km grid; annual flows | Annual flows 2011-2012 to 2024-2025; dataset updated 8 Oct 2026, files dated 24 Jul 2026 | Licence Ouverte 2.0 | All of France | ~31 MB (CSV) |
| 4 | BD TOPO® v3.5 | IGN | https://www.data.gouv.fr/datasets/bd-topo-r; download by department: https://geoservices.ign.fr/bdtopo | SHP, GPKG, SQL | 3D vector, metric accuracy | Quarterly updates; last update 7 Oct 2026; a "BD TOPO Historique" is also available | Licence Ouverte 2.0 | All of France | several GB per department (not checked) |
| 5 | Copernicus HRL Imperviousness: Imperviousness Density 2024 (10 m and 100 m), Impervious Built-Up 2024, Imperviousness Change 2021-2024 (20 m) | EEA / Copernicus Land Monitoring Service | https://land.copernicus.eu/en/products/high-resolution-layer-imperviousness | GeoTIFF (EEA 100 × 100 km tiles) | 10 m (density), 20 m (change) | 2006 to 2024, updated every 3 years | Free and open Copernicus access; **EU Login account required to download** (not checked here) | All of Europe | ~GB per tile |
| 6 | Industrial installations (ICPE under authorisation or registration) | MTE / Géorisques (BRGM), DREAL data | Database: https://www.georisques.gouv.fr/donnees/bases-de-donnees; API: `https://georisques.gouv.fr/api/v1/installations_classees?code_insee=…` (tested, no key); WFS: https://georisques.gouv.fr/services | CSV, JSON (API), WMS/WFS | Point (establishment), with SIRET, NAF, regime, Seveso, IED, and boolean flags for cattle/pigs/poultry/quarry/wind turbine/industry | Continuous | Etalab 2.0 (as stated on the Géorisques site) | All of France (excluding installations under simple declaration) | ~137,000 installations nationally (third-party, unofficial source) |
| 7 | National pollutant emissions register (IREP), "Installations industrielles rejetant des polluants" | MTE / INERIS via Géorisques | https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants | CSV/Excel per year (zip of 8 files: emissions, establishments, withdrawals, discharges, hazardous and non-hazardous waste) | Establishment (point); tonnes per pollutant and per medium (air, water, soil) | Annual; updated twice a year; the page says "last update December 2024" | Etalab 2.0 | All of France | not measured |
| 8 | Industrial Reporting under the IED 2010/75/EU and E-PRTR Regulation (EC) No 166/2006 | EEA | SDI record: https://sdi.eea.europa.eu/catalogue/srv/eng/catalog.search#/metadata/9405f714-8015-4b5b-a63c-280b82861b3d; https://industry.eea.europa.eu/industrial-emissions/dataset | SQL/Access database, CSV, GPKG ("various formats") | Installation (point) | 2007-2024 in the latest version; metadata updated 25 Sep 2026 | EEA free reuse (exact licence not read) | All of Europe | not measured |
| 9 | Polluted sites and soils: CASIAS (former industrial sites), SSP/ex-BASOL, SIS (soil information sectors) | MTE / BRGM via Géorisques | CASIAS CSV: https://mapsref.brgm.fr/wxs/georisques/georisques_dl?&service=wfs&version=2.0.0&request=getfeature&typename=etablissement_point&outputformat=csvtext; API: `https://georisques.gouv.fr/api/v1/ssp?code_insee=…` (tested); data.gouv page: https://www.data.gouv.fr/datasets/carte-des-anciens-sites-industriels-et-activites-de-services-casias | CSV, JSON, WMS/WFS | Point (site); SIS as polygons | Daily updates (SIS, SSP) | Etalab 2.0 (licence "not specified" on the data.gouv page) | All of France; CASIAS complete only for activities before 2005 | Rouen alone: 572 CASIAS entries |
| 10 | Registre national des installations de production et de stockage d'électricité (as of 31 Aug 2026) | RTE / ODRÉ (Open Data Réseaux Énergies) | https://www.data.gouv.fr/datasets/5bfcc5a006e3e744e304ccf0; API: https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/registre-national-installation-production-stockage-electricite-agrege/exports/csv | CSV, JSON, Opendatasoft API | Installation (located by commune); installations under 36 kW aggregated | Half-yearly or quarterly vintages (31 Dec 2023, 31 Dec 2024, 31 Dec 2025, 30 Jun 2026, 31 Aug 2026); updated 13 Oct 2026 | Licence Ouverte 2.0 | All of France | ~42 MB (CSV, according to a data.gouv listing) |
| 11 | Onshore wind (wind farms and turbines) | MTE / Géorisques | https://www.georisques.gouv.fr/donnees/bases-de-donnees ("Eolien terrestre" tab) | CSV | Turbine (point) and farm, with the farm's life cycle | Continuous | Etalab 2.0 | All of France | not measured |
| 12 | Annual average daily traffic on the national road network (TMJA) | Ministère de la Transition écologique | https://www.data.gouv.fr/datasets/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national; SHP 2024: https://static.data.gouv.fr/resources/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national/20250818-100425/tmja-rrnc-2024-shp.zip | SHP (zip), CSV | Section of non-concession national road, with TMJA and % heavy vehicles | 2019, then 2022, 2023 and 2024; updated 18 Aug 2025 | Licence Ouverte (fr-lo) | Non-concession national roads only (not the concession motorways A13, A28, A29, A84… nor the departmental network) | 2.2 MB (SHP 2024) |
| 13 | Tourist accommodation capacity (and tourist accommodation occupancy) | INSEE | https://www.data.gouv.fr/datasets/capacites-dhebergements-touristiques (Melodi file: https://api.insee.fr/melodi/file/DS_TOUR_CAP/DS_TOUR_CAP_2026_CSV_FR); https://www.data.gouv.fr/datasets/frequentation-des-hebergements-touristiques | CSV | Commune (and EPCI, department…); rooms, beds, camping pitches | Annual, 2026 vintage; updated 9 Oct 2026 | Licence Ouverte 2.0 | All of France | small |
| 14 (flagged) | National coastal erosion indicator | Cerema | https://www.data.gouv.fr/datasets/indicateur-national-de-lerosion-cotiere-1 → https://www.geolittoral.developpement-durable.gouv.fr/telechargement-en-ligne-donnees-geolittoral-a802.html#indi_nat_erosion | SHP | Shoreline sections, at 1:100,000 | **2018 version (old)**; change over at least 50 years | "Not specified" on data.gouv (licence to check) | The whole Normandy coast (all of mainland France) | small |
| 15 (flagged) | DRIAS, les futurs du climat (regionalised climate projections) | Météo-France (with IPSL, CERFACS, CNRM) | https://www.drias-climat.fr/ (data.gouv page: https://www.data.gouv.fr/datasets/drias-projections-climatiques-pour-ladaptation-de-nos-societes) | NetCDF/CSV (portal) | ~8 km grid (SAFRAN) (not checked) | data.gouv page updated 29 Apr 2024 | Licence Ouverte (fr-lo); a free account is probably needed to download (not checked) | All of France | variable |

## 1. Artificialisation and land take

### In short
As of October 2026, Normandy is fully covered by OCS GE v2.0 (2 vintages and a change layer per department) and by CoSIA (3 vintages, except the Orne, which has 2). Cerema's CONSOENAF series gives annual flows of natural, agricultural and forest land (ENAF) consumption by commune and by 1 km cell, from 2011 to 2025. These three datasets are the quantitative basis for artificialisation pressure. Copernicus HRL Imperviousness 2024 (10 m) gives a view comparable with the rest of Europe.

### Sources
- The IGN download service (`zone=` parameter) lists, for **OCS GE v2.0**: Calvados D014 vintages 2020 and 2023, plus DIFF-2020-2023 (published 17 Apr 2025); Eure D027 2019 and 2022, plus DIFF-2019-2022 (12 Jun 2025); Manche D050 2019 and 2022, plus DIFF (10 Mar 2025); Orne D061 2020 and 2023, plus DIFF (12 Mar 2025); Seine-Maritime D076 2019 and 2022, plus DIFF (12 Jun 2025). All in GPKG, Lambert-93 — [data.geopf.fr OCSGE](https://data.geopf.fr/telechargement/resource/OCSGE?zone=D014)
- The same service lists, for **CoSIA v1.0**: D014 2020, 2023 and 2026; D027 2019, 2022 and 2025; D050 2019, 2022 and 2025; D061 2020 and 2023 only; D076 2019, 2022 and 2025. All in GPKG, Lambert-93 — [data.geopf.fr COSIA](https://data.geopf.fr/telechargement/resource/COSIA?zone=D050)
- OCS GE is described as a two-dimensional (cover and use) "national reference" for land cover, used to monitor artificialisation under the Climat et Résilience law (art. L.101-2-1 of the code de l'urbanisme); Licence Ouverte 2.0; page updated 15 Oct 2026. WMS/WMTS services exist for the ARTIF layers 2016-2017 to 2024-2026, as well as "ARTIFICIALISATION-EXEMPTIONS" layers — [data.gouv OCS GE Artificialisation](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation); [data.gouv OCS GE](https://www.data.gouv.fr/datasets/ocs-ge)
- CoSIA is a by-product of OCS GE production, made of AI "predictions" in 15 classes, including building, impervious surface, greenhouse and bare soil — [data.gouv CoSIA](https://www.data.gouv.fr/datasets/cosia). Source resolution is 20 cm per pixel; error margins are published by department and by class — [IGN, CoSIA technical documentation](https://geoservices.ign.fr/sites/default/files/2025-04/Cosia_Documentation_Technique_IGN_2023.pdf). The December 2025 documentation (v1.0) has 15 classes, against 16 in the 2023 version — [DC CoSIA 1.0](https://geoservices.ign.fr/sites/default/files/2025-12/DC_CoSIA_1-0.pdf)
- CONSOENAF 2011-2025 (Cerema): Licence Ouverte 2.0; commune and 1 km cell units; annual time step; updated 8 Oct 2026; 31.1 MB CSV, 24.3 MB XLSX, several GPKG files (one of 436.9 MB) — [data.gouv CONSOENAF](https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61). The 2009-2023 version is archived — [data.gouv COENAF 2009-2023](https://www.data.gouv.fr/datasets/consommation-despaces-naturels-agricoles-et-forestiers-du-1er-janvier-2009-au-1er-janvier-2023). The cumulative 2009-2024 series is also published by the Observatoire des territoires — [Observatoire des territoires](https://www.observatoire-des-territoires.gouv.fr/consommation-despaces-naturels-agricoles-et-forestiers-enaf-entre-le-1er-janvier-2009-et-le-1er)
- Cerema data from the land-tax files are used for the official monitoring of the target to halve ENAF consumption (2011-2021 compared with 2021-2031) — [doc-datafoncier Cerema](https://doc-datafoncier.cerema.fr/doc/export/509)
- BD TOPO v3.5: 3D vector description with metric accuracy (buildings, transport, hydrography, land cover, services and activities, regulated areas); quarterly updates; last update 7 Oct 2026; Licence Ouverte 2.0; download by department or by region (SHP, GPKG, SQL) — [data.gouv BD TOPO](https://www.data.gouv.fr/datasets/bd-topo-r)
- Copernicus HRL Imperviousness: the following products are listed in the CLMS API: Imperviousness Density 2024 (10 m and 100 m), Impervious Built-Up 2024, Imperviousness Change 2021-2024 (20 m and 100 m) and Imperviousness Change Classified 2021-2024 — [CLMS Imperviousness Density 2024](https://land.copernicus.eu/api/en/products/high-resolution-layer-imperviousness/imperviousness-density-2024). The 2021 vintage introduced a U-Net method and a 2018-2021 built-up change layer — [CLMS news HRL IMD 2021](https://land.copernicus.eu/en/news/product-update-high-resolution-layer-imperviousness-2021)

### Our reading
- For problem 1 (restoration), the OCS GE DIFF layer directly gives the polygons artificialised between two vintages, about 3 years apart, at large scale. CONSOENAF gives a long, consistent series (2011-2025) by commune or 1 km cell, suited to a public-policy indicator (problem 2).
- The vintages are not synchronised: Eure, Manche and Seine-Maritime are 2019/2022, Calvados and Orne 2020/2023. A regional comparison has to account for this one-year offset.
- BD TOPO (road and rail sections, buildings) can be used to compute fragmentation indicators, such as effective mesh size or road density per cell.
- CoSIA works as a complementary indicator of the density of impervious surfaces and greenhouses, at the original 20 cm. It is an AI prediction, with errors to take into account.

### Open points
- Urban Atlas (Copernicus) not checked. In any case it covers only functional urban areas (Caen, Rouen, Le Havre, Cherbourg…), not the whole region.
- Volumes of the OCS GE and CoSIA GPKG files per department not measured.
- Whether an EU Login account is needed to download the Copernicus HRLs was not checked (it has been so far; to be confirmed).
- The artificialisation.developpement-durable.gouv.fr portal was not consulted directly. The Cerema data go through data.gouv.fr.

## 2. Industry and pollution

### In short
Géorisques publishes as open data, with no key (tested on 17 Oct 2026), the ICPE under authorisation or registration, polluted sites and soils (CASIAS, SSP/ex-BASOL, SIS), the IREP register and onshore wind. Everything can be reached through CSV download, WFS or a REST API queried by INSEE code. The European equivalent is the EEA Industrial Reporting database (IED and E-PRTR, 2007-2024). For wastewater treatment plants, no single up-to-date national dataset was found.

### Sources
- The Géorisques "Bases de données" page lists 18 databases, including: CASIAS (CSV); Onshore wind (wind farms and turbines, with the farm's life cycle); Industrial installations (ICPE under authorisation or registration, operating or closed); Industrial installations releasing pollutants (IREP); SIS (daily updates, CSV); Polluted sites and soils (ex-BASOL). WMS/WFS services are offered at https://georisques.gouv.fr/services. A banner states: "Dans un contexte d'attaque informatiques, des restrictions d'accès pour certaines localisations géographiques sont appliquées" (access is restricted from some locations because of cyber-attacks) — [Géorisques bases de données](https://www.georisques.gouv.fr/donnees/bases-de-donnees)
- IREP: "updated twice a year"; data per year, at national scale, in a zip of 8 files (emissions, establishments, withdrawals, discharges, production and treatment of hazardous and non-hazardous waste); source INERIS; covers mainland France, Corsica and the overseas departments; "last update December 2024" — [Géorisques IREP](https://www.georisques.gouv.fr/donnees/bases-de-donnees/installations-industrielles-rejetant-des-polluants)
- Test of the API `https://georisques.gouv.fr/api/v1/installations_classees?code_insee=14118` (Caen), with no key: 47 results. Fields returned: raisonSociale, codeNaf, longitude/latitude, bovins/porcs/volailles/carriere/eolienne/industrie (booleans), statutSeveso, ied, regime, serviceAIOT ("DREAL Normandie"), siret — [API Géorisques](https://georisques.gouv.fr/api/v1/installations_classees?code_insee=14118)
- Test of the API `https://georisques.gouv.fr/api/v1/ssp?code_insee=76540` (Rouen): 572 CASIAS entries, with main activity, status, date_maj and a link to the BRGM sheet — [API Géorisques SSP](https://georisques.gouv.fr/api/v1/ssp?code_insee=76540)
- The Géorisques ICPE database does not list installations under simple declaration. CASIAS (ex-BASIAS) is complete only for activities before 2005 — [Préfecture du Rhône, table of sources](https://www.rhone.gouv.fr/contenu/telechargement/49441/273079/file/tableau_source_information.pdf)
- The CASIAS data.gouv page (BRGM) gives a direct CSV export via WFS (mapsref.brgm.fr) and SSP_ETABLISSEMENT WMS/WFS services; licence "not specified" on data.gouv — [data.gouv CASIAS](https://www.data.gouv.fr/datasets/carte-des-anciens-sites-industriels-et-activites-de-services-casias)
- The former "Base des installations classées (ICPE)" on data.gouv has not been updated since 28 Feb 2021 — [data.gouv ICPE (obsolete)](https://www.data.gouv.fr/datasets/base-des-installations-classees-icpe)
- EEA "Industrial Reporting under the IED 2010/75/EU and E-PRTR Regulation (EC) No 166/2006": the latest version covers 2007-01-01 to 2024-12-31 (metadata dated 25 Sep 2026). Content: location and administrative data of large industrial complexes, pollutant releases and transfers, waste transfers, data on large combustion plants (LCP) — [EEA SDI record](https://sdi.eea.europa.eu/catalogue/srv/eng/catalog.search#/metadata/9405f714-8015-4b5b-a63c-280b82861b3d); [EEA Industrial emissions portal](https://industry.eea.europa.eu/industrial-emissions/dataset)
- Wastewater treatment plants: the data.gouv dataset "Assainissement" is in fact a DDTM de l'Eure dataset (treatment plants and treatment zones), harvested and dated 15 Nov 2024. The Eure plant layer includes 2024 compliance for 2023. These data come from the information portal on municipal sanitation (ERU reference) — [data.gouv Assainissement](https://www.data.gouv.fr/datasets/assainissement); [Eure treatment plants](https://data.gouv.fr/en/datasets/les-stations-de-traitement-des-eaux-usees-de-leure)

### Our reading
- For industrial pressure per cell, ICPE density (API, with Seveso, IED and livestock filters) can be combined with IREP tonnages per medium (air and water). The EEA E-PRTR allows comparison with other European regions. IREP and E-PRTR overlap heavily, so duplicates must be removed.
- The boolean `carriere` field of the ICPE API can extract authorised quarries in Normandy, which partly answers the "extraction" need.
- ICPE livestock farms (cattle, pigs, poultry) can serve as a point proxy for intensive agricultural pressure.
- Géorisques' geographic access restrictions may affect participants outside France or behind some VPNs.

### Open points
- The national municipal sanitation portal (ROSEAU / "assainissement.developpement-durable.gouv.fr") could not be consulted: the page is no longer online. No checked link to a national export of treatment plants with their ERU compliance.
- The volume of the IREP database and its most recent data year (2023 or 2024) are not confirmed. The page gives "December 2024" as the last update, which may be out of date for a twice-yearly update.
- The exact licence of the EEA Industrial Reporting files was not read.

## 3. Extraction and energy

### In short
Electricity production installations (wind, ground-mounted solar, hydro…) are covered by the national ODRÉ/RTE register (as of 31 Aug 2026), located by commune, and by the Géorisques onshore wind database. For quarries, no dedicated national dataset was found: the data are either regional (DREAL) or must be extracted from the Géorisques ICPE (`carriere` field).

### Sources
- "Registre national des installations de production et de stockage d'électricité (au 31/08/2026)", organisation Open Data Réseaux Énergies, Licence Ouverte 2.0, updated 13 Oct 2026. CSV and JSON exports through the Opendatasoft API — [data.gouv ODRÉ register](https://www.data.gouv.fr/datasets/5bfcc5a006e3e744e304ccf0)
- RTE produces this register (art. L142-9-1 of the code de l'énergie) from data sent by the distribution network operators. Previous vintages: 31 Dec 2023, 31 Dec 2024, 31 Dec 2025 and 30 Jun 2026. A CSV of about 42 MB is listed — [data.gouv register 30/06/2026](https://www.data.gouv.fr/datasets/registre-national-des-installations-de-production-et-de-stockage-delectricite-au-30-06-2026); [register 31/12/2025](https://www.data.gouv.fr/datasets/69c4af4e5c9f9567df414fc6)
- Géorisques publishes an "Eolien terrestre" database: wind farms with their life cycle, and the turbines that make up each farm — [Géorisques bases de données](https://www.georisques.gouv.fr/donnees/bases-de-donnees)
- data.gouv searches for "carrières" return only regional or local datasets (Bretagne, Bourgogne-Franche-Comté, Île-de-France, Hauts-de-France, Cantal…), no national dataset — [data.gouv search "carrières"](https://www.data.gouv.fr/datasets/carrieres-actives-definies-par-le-schema-regional-des-carrieres-de-bretagne)

### Our reading
- The ODRÉ register is located by commune, not by point. To locate wind farms precisely, Géorisques (turbines as points) is better. For ground-mounted solar farms, cross with OCS GE or CoSIA, or with BD TOPO ("services et activités" theme).
- For quarries, the national option remains the ICPE API (`carriere=true`). The DREAL Normandie layers (regional quarry plan) are outside the "national" scope but complementary.

### Open points
- No dedicated national open dataset on quarries (BRGM, regional plans) was checked.
- No checked national dataset gives the footprint of ground-mounted solar farms.

## 4. Light pollution

### In short
No French national open dataset on light pollution covering Normandy was found. On data.gouv, the existing products are local or regional (Métropole du Grand Paris, Occitanie, Bretagne, Aix-Marseille). Global satellite sources require an account (NASA Black Marble) or are under a non-commercial licence with a request form (World Atlas, Falchi et al., 2016).

### Sources
- data.gouv searches for "pollution lumineuse" and "trame noire" return only local or regional datasets: Métropole du Grand Paris (radiance, NSB index), light-pollution modelling in Occitanie, the dark-sky network in Bretagne, Aix-Marseille-Provence — [data.gouv light-pollution modelling Occitanie](https://www.data.gouv.fr/datasets/modelisation-de-la-pollution-lumineuse-en-occitanie); [Trame noire en Bretagne](https://www.data.gouv.fr/datasets/trame-noire-en-bretagne-atlas-cartographiques)
- NASA Black Marble (VNP46, VJ146): daily, monthly and annual night-light composites, in HDF5, archived on LAADS DAAC. Automated download (blackmarblepy) needs a LAADS token (Earthdata account) — [NASA Earthdata Black Marble](https://www.earthdata.nasa.gov/data/projects/black-marble); [blackmarblepy PyPI](https://pypi.org/project/blackmarblepy)
- New World Atlas of Artificial Night Sky Brightness: GeoTIFF of about 2.9 GB at 30 arc-seconds. Licence CC BY-NC 4.0 since November 2019. FTP access on request — [B2FIND record](https://b2find.eudat.eu/dataset/df8cd562-df6a-51bf-ad64-7421cf8c8623); [GFZ press](https://www.gfz.de/en/press/news/details/new-atlas-of-light-pollution)

### Our reading
- For Normandy, the most realistic route is the annual VIIRS composites (Black Marble VNP46A4, or EOG VNL). The accounts needed are free but mandatory, which should be flagged as "not fully open". The World Atlas can be used for non-commercial purposes, which is acceptable for a datathon, subject to the NC licence.

### Open points
- The products of La Nuit est Belle, AVEX and Cerema (national dark-sky network) were not checked. No national open dataset was found on data.gouv.
- Access conditions for EOG (Colorado School of Mines, VIIRS Nighttime Lights) were not checked. Registration is probably required.

## 5. Transport pressure

### In short
TMJA traffic data for the non-concession national road network are open (SHP and CSV, vintages 2019, 2022, 2023 and 2024). They cover neither concession motorways nor departmental roads. For network density, BD TOPO (transport theme) is the reference. No national open dataset on wildlife–vehicle collisions was found.

### Sources
- TMJA: annual mean number of vehicles per day, both directions combined, usually with a share of heavy vehicles, per section (road name, length, start and end coordinates). Resources: TMJA_RRNc_2024 (SHP 2.2 MB, CSV 0.2 MB), 2023, 2022 and 2019. Licence Ouverte; updated 18 Aug 2025 — [data.gouv TMJA](https://www.data.gouv.fr/datasets/trafic-moyen-journalier-annuel-sur-le-reseau-routier-national)
- The DIR Nord-Ouest publishes a 2024 traffic review for its national network (about 1,000 km, 11 departments, about 150 sensors) — [DIRNO 2024 traffic review](https://www.dir.nord-ouest.developpement-durable.gouv.fr/IMG/pdf/20251106_bilan_trafic_2024_dirno.pdf)
- A data.gouv search for "collisions faune" returns no results (0 datasets) — [data.gouv](https://www.data.gouv.fr/datasets/?q=collisions%20faune)

### Our reading
- For a complete regional road-pressure indicator, BD TOPO section density can be weighted by importance (nature and importance attributes), using TMJA only where it exists. The "RRNc" suffix of the files means the non-concession network: Normandy's main concession motorways (A13, A28, A29, A84 in part) have no TMJA in this dataset.

### Open points
- No checked open traffic data for concession motorways (SANEF, ALIS, etc.) or for the departmental network.
- No national open data on wildlife collisions (OFB and naturalist networks hold data, but they are not open at national level as far as we found).

## 6. Tourism and recreation pressure

### In short
INSEE publishes as open data (Licence Ouverte 2.0) tourist accommodation capacity by commune (2026 vintage) and accommodation occupancy. It is a simple proxy for tourism pressure, especially on the Normandy coast.

### Sources
- "Capacités d'hébergements touristiques" (INSEE): number of establishments, rooms, beds and camping pitches, by type (hotels, campsites, other) and by star rating; geographic levels from commune to region; annual; 2026 coverage; updated 9 Oct 2026; CSV through the Melodi API — [data.gouv INSEE capacity](https://www.data.gouv.fr/datasets/capacites-dhebergements-touristiques)
- "Fréquentation des hébergements touristiques" (INSEE), updated 4 Oct 2026, Licence Ouverte 2.0 — [data.gouv INSEE occupancy](https://www.data.gouv.fr/datasets/frequentation-des-hebergements-touristiques)

### Our reading
- A ratio of tourist beds to inhabitants, or beds per km², by commune is a direct indicator of seasonal pressure, useful for problem 2. Occupancy is probably not available by commune (statistical secrecy), which was not checked.

### Open points
- Spatial granularity of the occupancy data not checked.
- No national open dataset on visitor numbers in natural areas found.

## 7. Climate change and coastal exposure

### In short
Cerema's national coastal erosion indicator covers the whole Normandy coast but dates from 2018. DRIAS provides regionalised climate projections, with access probably requiring registration.

### Sources
- National coastal erosion indicator (Cerema): change in shoreline position over at least 50 years, in mainland France and 5 overseas departments. Page dated 28 Jun 2018; licence "not specified" on data.gouv; SHP download on Géolittoral — [data.gouv erosion indicator](https://www.data.gouv.fr/datasets/indicateur-national-de-lerosion-cotiere-1)
- The indicator is produced at 1:100,000 from shorelines digitised on aerial photos. Recent shorelines come from 2005-2014 photos, old ones from 1920-1957 photos — [Cerema, technical specifications](https://www.geolittoral.developpement-durable.gouv.fr/IMG/pdf/specif-tech-carto-indicateur-erosion.pdf); [data.gouv period analysed](https://www.data.gouv.fr/datasets/duree-analysee-pour-levolution-du-trait-de-cote-1)
- DRIAS provides regionalised climate projections (IPSL, CERFACS, CNRM-GAME). data.gouv page under Licence Ouverte (fr-lo), updated 29 Apr 2024 — [data.gouv DRIAS](https://www.data.gouv.fr/datasets/drias-projections-climatiques-pour-ladaptation-de-nos-societes)

### Our reading
- For problem 1, coastal erosion can weight the restoration priority of coastal habitats (dunes, back-dune marshes), but the data are old: the shorelines are more than 10 years old.
- The Géorisques layers "Retrait-gonflement des argiles 2026" (clay shrink-swell) and "Zonages inondation 2026" (flood zones) are not biodiversity pressures in the strict sense, but they exist and are recent.

### Open points
- DRIAS access conditions (account, NetCDF format, 8 km grid) were not checked.
- Open Météo-France data (meteo.data.gouv.fr) were not checked.
- Whether the national erosion indicator has been updated since 2018 was not checked.
