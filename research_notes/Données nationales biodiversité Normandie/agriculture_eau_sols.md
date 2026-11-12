# National and European open datasets on agriculture practices, pesticides, water (quantity and ecological state) and soils for Normandy (Datathon Normandie 2026)

Scope: about 15 national and European open datasets. Excluded because we already have them: RPG and derived IGN layers, Naïades surface-water quality, Phytatmo, Agreste in general. All the national datasets below cover the whole of metropolitan France, so all 5 Normandy departments (14 Calvados, 27 Eure, 50 Manche, 61 Orne, 76 Seine-Maritime) are covered unless flagged. Fields marked "not verified" could not be confirmed.

## Pesticides (BNV-D sales and purchases, NODU/QSA, groundwater pesticides, Ecophyto)

### In short
BNV-D purchases by buyer postcode are the key pesticide-pressure layer. They are open (Licence Ouverte), annual 2013–2024, and available on data.gouv.fr and through a Hub'Eau API. Combined with Hub'Eau "Qualité des nappes" (ADES groundwater, pesticides included), they give a pressure-to-impact pair for prioritisation (problem 1) and a trend indicator (problem 2).

### Sources
- **D1. "Achats de produits phytosanitaires à l'échelle du code postal" (BNV-D)**
  - Data: purchases of plant-protection products by buyer postcode, as active-substance quantities, adjuvants excluded.
  - Coverage: latest edition 2013–2024, published 21/04/2026.
  - Format: Parquet files split by purchase year, with product-level and substance-level files at postcode, department and national scales — [data.gouv.fr](https://www.data.gouv.fr/datasets/achats-de-produits-phytosanitaires-a-lechelle-du-code-postal/informations)
  - Conflicting metadata on the landing page: producer shown as SDES, Licence Ouverte / Open Licence, HTML + CSV resources, CSV updated 22 July 2026, page metadata dated 17 Oct 2026 — [data.gouv.fr dataset page](https://www.data.gouv.fr/datasets/achats-de-produits-phytosanitaires-a-lechelle-du-code-postal/). Other sources describe BNV-D as OFB-operated (see the next point).
- **D1 caveats:**
  - Postcodes with 5 or fewer farms are suppressed ("secrétisées") — [data.gouv.fr dataset page](https://www.data.gouv.fr/datasets/achats-de-produits-phytosanitaires-a-lechelle-du-code-postal/)
  - The purchase location does not tell you where or when products were applied — [data.gouv.fr](https://www.data.gouv.fr/datasets/achats-de-produits-phytosanitaires-a-lechelle-du-code-postal/informations)
  - An older archived page, "Achats de pesticides par code postal", covers the same source — [data.gouv.fr archive](https://www.data.gouv.fr/datasets/achats-de-pesticides-par-code-postal/informations)
- **D1 by API:** Hub'Eau API "Vente et achat de produits phytopharmaceutiques", source "BNV-D Traçabilité" operated by the Office français de la biodiversité (OFB) — [Hub'Eau APIs list](https://hubeau.eaufrance.fr/page/apis). The same page lists the "Qualité des nappes" API, which covers groundwater quality (pesticides included); its source database is not named on that page.
- **BNV-D background:** a 2024 BNV-D infographic is published by Eaufrance — [eaufrance.fr infographic](https://www.eaufrance.fr/sites/default/files/documents/infographie_bnvd_2024.pdf). A DRAAF document describes the BNV-D purchase series as annual, which matches the 2013-onward series — [DRAAF Pays de la Loire](https://draaf.pays-de-la-loire.agriculture.gouv.fr/IMG/pdf/5_cries_22-11-16_bnvd.pdf)

### Our reading
- Problem 1: aggregate BNV-D postcode purchases to the commune or water-body catchment (postcode-to-commune correspondence table from La Poste open data), normalise by RPG agricultural area, and use the result as a "pesticide pressure" factor. Problem 2: use the 2013–2024 trends per area as an indicator of positive or negative change. Suppressed postcodes are probably sparse in Normandy's farming areas but may hit small urban or coastal postcodes.
- Hub'Eau "Qualité des nappes" (ADES): filter on pesticide parameter codes and Normandy department codes to get groundwater-impact points (JSON/CSV, no account needed in practice; not formally verified).

### Open points
- Not checked: the NODU/QSA Ecophyto indicators by region or department (published by the Ministry of Agriculture as reports, often PDF rather than machine-readable). Treat them as context only.
- The exact Hub'Eau API documentation URLs for BNV-D and "Qualité des nappes", and their licence (Hub'Eau data is generally Licence Ouverte), were not confirmed on that page.
- Conflicting producer (SDES vs OFB) and format (Parquet vs CSV) metadata for D1 is unresolved. Check the resources on download.

## Good practices (organic farming, HVE, CAP/MAEC beneficiaries, Label bas-carbone, hedges)

### In short
Two clean, open, recent "good practice" layers exist: Agence Bio organic surfaces, livestock and operators per commune (updated July 2026), and the HVE directory (June 2025, but only for farms that agreed to be listed, and with farm names). CAP beneficiary data (Telepac transparency) names individual beneficiaries and is not available as a current bulk download on data.gouv.fr. Label bas-carbone projects are listed on a ministry web page, not as a confirmed open dataset.

### Sources
- **D2. Agence Bio — "Historique détaillé des surfaces, cheptels et nombre d'opérateurs par commune (BIO COMMUNE)"**
  - Content: certified organic area, area in conversion years 1–3, organic livestock (beehives included), and operator counts by type (producers, processors, distributors, importers), by commune (INSEE code).
  - Format and update: xlsx/csv, last updated 8 July 2026 — [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/surfaces-cheptels-et-nombre-doperateurs-bio-a-la-commune/)
  - Location rule: parcels are declared in the commune of the activity site, or failing that the head office, so area may be shifted between communes — [data.gouv.fr](https://www.data.gouv.fr/datasets/61a6250d8660681353681fa8)
  - Caveat on older snapshots: the 2018/2019 pages warn that surfaces and livestock are underestimated by about 10% on average — [data.gouv.fr Opérateurs Bio 2019](https://www.data.gouv.fr/datasets/operateurs-bio-2019)
- **D3. "Annuaire des exploitations certifiées Haute Valeur Environnementale"** (Ministry of Agriculture)
  - Content: farms certified HVE at 1 June 2025 that agreed to appear in the directory. Fields: name or company name, address, postcode, region, department, commune, website, main activity (crop or livestock), direct sales, certification date.
  - Format and volume: CSV (about 3.1 MB) + Excel, updated 30 July 2025 — [data.gouv.fr](https://www.data.gouv.fr/datasets/61a92b5148113b5780a01cfb/)
  - National totals by region and sector are in ministry tables: 39,738 farms in June 2025, of which 32,509 under the 2022 v4 standard — [agriculture.gouv.fr table](https://agriculture.gouv.fr/telecharger/139743)
- **CAP beneficiaries (Telepac transparency):**
  - The old data.gouv.fr datasets cover only 2010–2012: "Aides perçus par les bénéficiaires au titre de la PAC", last updated Nov 2015 — [data.gouv.fr](https://www.data.gouv.fr/datasets/5653545ac751df55b3aad371); "Telepac, les bénéficiaires de la PAC", not updated since July 2014 — [data.gouv.fr](https://data.gouv.fr/en/datasets/telepac-les-beneficiaires-de-la-pac)
  - A forum post on the dataset says later years (2015–2018) are on the Telepac site, with more than 1.8 million rows for 2018 — [data.gouv.fr discussion](https://www.data.gouv.fr/datasets/telepac-les-beneficiaires-de-la-pac/discussions)
  - Legal basis: publication under Regulation (EC) 259/2008, searchable by name, commune or amount — [Assemblée nationale written answer](https://www.assemblee-nationale.fr/dyn/13/questions/QANR5L13QE61077.pdf)
- **Label bas-carbone:** the list of labelled projects (location, method, project holders, expected reductions and co-benefits) is published on the ministry's label page — [DRIEAT 2021 webinar report](https://www.drieat.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/210112_cr_webinaire_lbc.pdf). Recent brochures point to https://mtect.fr/714, and the framework was updated by Decree 2025-917 of 5 Sept 2025 — [DREAL Grand Est 2026 brochure](https://www.grand-est.developpement-durable.gouv.fr/IMG/pdf/20260306-lbc-plaquette-w.pdf)

### Our reading
- D2 (organic area per commune ÷ RA 2020 or RPG agricultural area) and D3 (HVE farm counts per commune) give direct "positive interaction" indicators for problem 2.
- D3 contains business names and addresses. For a publishable output, aggregate to counts per commune or EPCI and drop names.
- D3 is opt-in, so it undercounts. Treat it as a minimum and cross-check against the ministry's regional totals.
- CAP beneficiary data: if used, aggregate MAEC/organic-aid amounts per commune and never publish names. In practice it is hard to bulk-download for recent years (assumption based on the sources above). Prefer the RPG-derived layers we already have, or the RA 2020 tables.

### Open points
- No current bulk-download URL was found for Telepac transparency data (2023–2025 campaigns), nor for the EU-level FEADER/EAGF beneficiaries search (EU "Data on CAP beneficiaries" portal, not verified).
- No machine-readable Label bas-carbone project file was found on data.gouv.fr. The list seems to be a web page or spreadsheet on the ministry site; check https://mtect.fr/714 and filter for "Plantation de haies" projects in Normandy.
- "Plantons des haies" programme results: no open dataset found.
- The national hedge layer (Dispositif national de suivi des bocages, OFB/IGN) was not checked here; it is already in our data inventory (HAIES.BOCAGES).

## Agriculture structure (Recensement agricole 2020 communal tables, livestock)

### In short
The RA 2020 communal data (56 mapped indicators plus historical tables, with 2010 for comparison) are open on data.gouv.fr (Agreste, updated Oct 2025). They are the best source for livestock density, grassland share and farm size at commune level. Watch out for statistical secrecy and the "head-office commune" location rule.

### Sources
- **D4. "Agreste - Données COMMUNALES du recensement agricole - Cartographie 2020 et Tableaux interactifs historiques"**
  - Content: 56 cartographic indicators of RA 2020 at commune level (Geoclip), plus historical interactive communal tables.
  - Format and update: xlsx, URL resources and an API, updated 3 Oct 2025. Some resources are flagged unavailable — [data.gouv.fr](https://www.data.gouv.fr/datasets/5369931da3a729239d2040d8/)
- Companion dataset: "Agreste - Cartographie des données du recensement agricole", 2020 and 2010 results by commune, canton, department and region — [data.gouv.fr](https://www.data.gouv.fr/datasets/53699038a3a729239d20394f/)
- The Observatoire des territoires offers downloadable RA-derived indicators, for example change in agricultural area (SAU) 2010–2020. Data is located at the commune of the farm's main production site, so commune figures need care — [Observatoire des territoires](https://www.observatoire-des-territoires.gouv.fr/evolution-surface-agricole-utilisee-sau-2010-2020); see also [change in number of farms 2010–2020](https://www.observatoire-des-territoires.gouv.fr/evolution-du-nombre-dexploitations-agricoles-entre-2010-et-2020)

### Our reading
- For Normandy, the most useful variables are the change in permanent grassland and livestock units (cattle, a major driver of bocage persistence or loss), SAU and farm-count changes 2010–2020, and average farm size. These are pressure or trend factors for both problems.
- RA data is about 6 years old as of Oct 2026 (next census around 2030). It is not outdated for structural indicators but should be flagged as a 2020 snapshot.

### Open points
- The exact list of the 56 indicators and how many communes are secrecy-masked in Normandy were not checked.
- Annual livestock data (BDNI cattle database, "cheptel" statistics by department from Agreste SAA) was not verified.

## Water quantity and ecological state (Hub'Eau, WFD status, ROE)

### In short
Hub'Eau provides 13 free REST APIs on a single portal. Those relevant here are piezometry, hydrometry (near real-time), water withdrawals (BNPE), hydrobiology (bio-indices from Naïades), fish (electrofishing), river temperature, ONDE flow observations and coastal surveillance. Water-body ecological status (WFD) is easiest to get openly from the EEA WISE WFD 3rd-cycle (2022) layers (CC BY 4.0). The French 2025 état des lieux was not found as an open dataset.

### Sources
- **D5. Hub'Eau (OFB/BRGM/Eaufrance)** lists these APIs: Vente et achat de produits phytopharmaceutiques; Écoulement des cours d'eau (ONDE visual campaigns); Qualité de l'eau potable; Surveillance des eaux littorales (QUADRIGE); Hydrobiologie; Prélèvements en eau; Hydrométrie (more than 6,000 stations, near real-time); Température des cours d'eau (automatic sensors); Qualité des cours d'eau; Qualité des nappes; Piézométrie; Indicateurs des services; Poisson (scientific electrofishing) — [Hub'Eau APIs](https://hubeau.eaufrance.fr/page/apis)
- Hub'Eau endpoint details (from the R package `hubeau`, INRAE):
  - Hydrobiologie: stations, bio-indices (indices) and taxa (taxons), sourced from Naïades.
  - Écoulement (ONDE): stations, observations and annual campaigns.
  - Prélèvements: time series, works and withdrawal points (query by commune INSEE code and year). Documentation: https://hubeau.eaufrance.fr/page/api-prelevements-eau
  - Température: stations and time series.
  - Source for all of the above — [hubeau R package manual](https://inrae.r-universe.dev/hubeau/doc/manual.html); see also the [INRAE HAL paper](https://hal.inrae.fr/hal-04601100/file/hubeau.pdf)
- **D6. EEA WISE WFD (3rd RBMP, reporting 2022)**
  - Layers: surface water bodies WFD2022_SurfaceWaterBody_WM and ecological status WFD2022_SurfaceWaterBody_EcologicalStatusOrPotentialValue_WM_TS, served through Discomap ArcGIS REST. Downloads via EEA SDI. Licence CC BY 4.0.
  - Caveat: some WFD2022 map services are labelled "for testing purposes" — [EEA Discomap service](https://marine.discomap.eea.europa.eu/arcgis/rest/services/WISE_WFD/WFD2022_SurfaceWaterBody_WM/MapServer); [EEA SDI catalogue](https://sdi.eea.europa.eu/catalogue/srv/api/records/6a789198-969c-4ee6-be68-074c380a3e6e); [WISE Freshwater visualisation](https://water.europa.eu/freshwater/europe-freshwater/visualization/surface-water-bodies-ecological-status-or-potential-by-country)
- Seine-Normandie basin on data.gouv.fr: "Etat et objectif des masses d'eau souterraine affleurante dans le bassin Seine-Normandie" (SDAGE 2022–2027 status and objectives; shapefile, WMS, WFS; last updated April 2022, files republished May 2025) — [data.gouv.fr](https://www.data.gouv.fr/datasets/etat-et-objectif-des-masses-deau-souterraine-affleurante-dans-le-bassin-seine-normandie). This is basin-agency data (Seine-Normandie covers all of Normandy) rather than strictly national.
- The 2025 Seine-Normandie état des lieux exists: the basin scientific council's opinion on it was published on HAL in 2025/2026 — [HAL hal-05505501](https://hal-lara.archives-ouvertes.fr/hal-05505501v1). In the 2019 état des lieux, about 32% of the basin's 1,782 river water bodies were in good ecological status — [Banque des Territoires](https://www.banquedesterritoires.fr/bassin-seine-normandie-letat-ecologique-des-cours-deau-progresse-mais-trop-lentement)

### Our reading
- Problem 1: WFD ecological status (D6) per water body gives "degraded" aquatic habitats. Hub'Eau hydrobiology indices (I2M2, IBD, IPR fish) give station-level biological condition. ONDE drying frequency and BNPE withdrawals give quantitative pressure.
- Problem 2: trends in hydrobiology and fish indices, and the share of ONDE "assec" (dry) observations by summer campaign, can serve as human–nature interaction indicators.
- Everything can be filtered on code_departement in (14, 27, 50, 61, 76) or code_region = 28. Hub'Eau APIs need no account (assumption based on general practice; the list page did not say).

### Open points
- No open machine-readable file was found for the 2025 état des lieux (cycle 4, SDAGE 2028–2033) water-body status. Check the Seine-Normandie water agency site and rapportage.eaufrance.fr. If unavailable, the EEA 2022 layers reflect the 2019 assessment, which is outdated (based on data from about 2015–2017).
- ROE (Référentiel des obstacles à l'écoulement, OFB/Sandre) was not verified; it is probably covered in the biodiversity notes.
- Hub'Eau licence terms were not confirmed (terms-of-use page not read).

## Coastal water (bathing water, shellfish areas REPHY/REMI, nitrates, green tides)

### In short
Ifremer's REPHY (phytoplankton and hydrology since 1987, CC BY 4.0, annual fixed releases on SEANOE, with a Normandy RHLN regional subset) and REMI (shellfish-area microbiology) are the key national coastal datasets. Bathing-water results are open via the Ministry of Health's "rapportage de la saison balnéaire" on data.gouv.fr.

### Sources
- **D7. REPHY — French Observation and Monitoring program for Phytoplankton and Hydrology** (Ifremer)
  - SEANOE DOI 10.17882/47248, whole French metropolitan coast since 1987.
  - Data shared with regional networks, including RHLN (Normandy). Files split into whole dataset and regional subsets, and into PHYTO (counts) and HYDRO (physico-chemistry, pigments) — [SEANOE](https://seanoe.org/data/00361/47248)
  - Annual fixed-file updates covering years before the current one — [Ifremer manual](https://archimer.ifremer.fr/doc/00409/52016/52666.pdf); licence CC BY 4.0 — [marineinfo.org record](https://marineinfo.org/doc/dataset/2451)
- **D8. REMI — French microbiological monitoring program of mollusc harvesting areas** (Ifremer), SEANOE DOI 10.17882/47157 — [Archimer citation](https://archimer.ifremer.fr/doc/00409/52017). Coverage, structure and licence were not confirmed.
- Hub'Eau "Surveillance des eaux littorales" API draws on QUADRIGE (the Ifremer database behind REPHY and REMI) — [Hub'Eau APIs](https://hubeau.eaufrance.fr/page/apis)
- **D9. Bathing water:** the Ministry of Health syntheses point to the data.gouv.fr dataset "données de rapportage de la saison balnéaire" (https://www.data.gouv.fr/fr/datasets/donnees-de-rapportage-de-la-saison-balneaire-1/), with baignades.sante.gouv.fr as the public access point. The 2025 synthesis notes quality has tended to decline in recent years — [Synthèse bilan QEB 2025](https://baignades.sante.gouv.fr/baignades/editorial/fr/actualites/Synthese_bilan_QEB_2025_v0.pdf)
- Classification uses 4 classes based on E. coli and enterococci over the last 4 seasons — [ARS Occitanie report](https://www.occitanie.ars.sante.fr/media/80722/download?inline)

### Our reading
- For Normandy's long coastline (Manche, Calvados, Seine-Maritime), REMI microbiology classes and bathing-water classes are good downstream indicators of land-based pressure (livestock effluents, sanitation). REPHY gives eutrophication signals at estuaries such as the Seine and the Baie des Veys.
- Green tides are mainly a Brittany issue. Normandy has some local episodes (e.g. western Cotentin), but no dedicated national green-tide dataset was checked, so this is low priority.

### Open points
- Nitrate vulnerable zones (zones vulnérables, Sandre/Ministry) were not verified; they are a known Sandre/Atlas-catalogue layer and nearly all of Normandy is classified as vulnerable (unverified).
- The current contents of the bathing-water data.gouv.fr dataset (latest season, format) were not checked.
- The EEA bathing water dataset (European) was not checked.

## Soils (GIS Sol, RMQS, soil carbon, 1:250k soil map, ESDAC erosion)

### In short
GIS Sol data (RMQS point cartograms, national soil-carbon maps) is distributed through the GIS Sol Dataverse on entrepot.recherche.data.gouv.fr and the INRAE geocatalogue, but parts are images or PDFs and fine-scale 1:250k maps are not downloadable from one national place. ESDAC/JRC RUSLE2015 erosion rasters (100 m, EU) are free but need a request form, with no redistribution to third parties, so they are not strictly "open data".

### Sources
- **D10. GIS Sol Dataverse** (INRAE/GIS Sol), at entrepot.recherche.data.gouv.fr/dataverse/gissol (filter keyword "carbone").
  - Products include a national soil carbon stock map (part of the FAO global map), RMQS campaign 1 (2001–2009) point cartograms of organic carbon, and loss-on-ignition carbon. Some carbon maps are only images or PDFs — [DataGrandEst webinar FAQ 2024](https://datagrandest.fr/portail/sites/default/files/dge2024-webinaire_donnees_sol_sous_sol_faq_v01.pdf)
  - Example record: RMQS campaign 1 cation exchange capacity cartogram — [agroenvgeo geonetwork](https://agroenvgeo.data.inra.fr/geonetwork/srv/api/records/d5e05cbc-fb4d-573d-af8f-a020d2ad0de3). data.gouv.fr also has "Carbone organique dans l'horizon de surface" — [data.gouv.fr](https://www.data.gouv.fr/datasets/a1b0807c-9bff-4f6a-a5e7-130316742f56-uuid/informations)
  - Order of magnitude: the top 30 cm of French soils hold about 3.58 Pg C (RMQS campaign 1) — [Martin et al. 2022, EGS](https://www.afes.fr/wp-content/uploads/2023/04/EGS_2022_29_Martin_329-352.pdf)
- Spatial data entry point: geodata.inrae.fr (replacing agroenvgeo). Géoportail's soil layer is view-only. Regional 1:250k soil references (RRP) are often distributed regionally. The Refersols tool (webapps.gissol.fr) shows which soil studies exist — [AFES/RMT webinar on Normandy soil data, 2025](https://www.afes.fr/wp-content/uploads/2025/03/donnees_sols_RMT_CRA_normandie.pdf); [INRAE presentation 2024](https://hal.inrae.fr/hal-04627465v1/document)
- **D11. ESDAC "Soil erosion by water (RUSLE2015)"** (JRC)
  - Data: 100 m rasters for 2010 and 2016, EU-28, about 2 GB each.
  - Access: free of charge but via a request form; no passing data to third parties, though use for any purpose is allowed; citation required (Panagos et al. 2015, Env. Sci. & Policy 54: 438–447; Panagos et al. 2020, Remote Sensing 12: 1365) — [ESDAC](https://esdac.jrc.ec.europa.eu/node/135857); [ESDAC catalogue](https://esdac.jrc.ec.europa.eu/taxonomy/term/4394)

### Our reading
- Problem 1: RUSLE erosion (D11) is a strong pressure layer for Normandy's loess plateaus (Pays de Caux, Eure), which are known for muddy runoff and erosion. It can be overlaid with the loss of grassland and hedges. Flag it as "registration required, no redistribution": do not re-host the raw raster in the datathon kit; each participant must request it.
- RMQS is a 16 km grid, so there are only a few dozen points in Normandy. Use it for context or validation, not for fine prioritisation.
- For Normandy's 1:250k RRP soil map, the Normandy chamber of agriculture / RMT data (regional producer) may be the practical source, which is outside this national scope.

### Open points
- The exact Dataverse records (DOIs, licences, Normandy coverage of the 1:250k RRP) were not opened.
- BDETM (trace elements database), BDAT (soil analyses) and LUCAS Soil (JRC, also form-based) were not verified.
- The ESDAC temporary download links seen had expiry dates of Feb–Jul 2026. A new request is needed as of Oct 2026.
