# Open data for detecting and measuring grassland ploughing in Normandy (2010–2025)

Statements marked "UNVERIFIED" were not checked against a source and appear only under Our reading or Open points.

## 1. RPG multi-year: crop codes for permanent and temporary grassland, history products, 2015 break

### In short
The RPG is still the best source for parcel-level, year-to-year detection. From 2015 (RPG v2.0) each parcel carries a Telepac crop code: PPH and PRL fall in culture group 18 "Prairies permanentes", PTR in group 19 "Prairies temporaires". The 2024 edition added a separate "PP" (prairies permanentes) database among 8 databases. We found no official IGN/ASP "RPG transitions" product. INRAE's "RPG complété" (Cantelaube & Lardot, Etalab 2.0, 2018–2023) completes single years but does not track parcels across years.

### Sources
- **Producer, licence, coverage.** The RPG on data.gouv.fr is produced by IGN. ASP manages the programme and MASA checks regulatory compliance. Licence: Licence Ouverte v2.0, France entière, annual updates. Resources were updated 15 Apr 2026; the page was last updated 29 Sep 2026 — [data.gouv.fr RPG](https://www.data.gouv.fr/fr/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/)
- **Structure change in 2024.** The 2024 edition split the RPG into 8 databases. Six cover parcels/îlots (Parcelles, Ilots, GCP, **PP**, IAE, BIO) and two cover non-agricultural surfaces (SNA) and homogeneous density zones (ZDH). The GCP base groups parcels into 4 categories: arable land (TA), permanent crops (CP), **permanent grassland (PP)** and wooded areas (SB). Before 2024 the RPG held parcel data and, depending on the year, îlot data — [data.gouv.fr RPG](https://www.data.gouv.fr/fr/datasets/registre-parcellaire-graphique-rpg-contours-des-parcelles-et-ilots-culturaux-et-leur-groupe-de-cultures-majoritaire/)
- **Old link redirect.** geoservices.ign.fr/rpg now redirects (301) to cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_RPG. That page could not be read (it needs JavaScript) — [cartes.gouv.fr IGNF_RPG](https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_RPG)
- **Version 2.0 descriptif.** The "RPG Version 2.0 – Descriptif de contenu et de livraison" document (DC_DL_RPG_2-0) is mirrored on regional portals — [geo2france DC_DL_RPG_2-0.pdf](https://www.geo2france.fr/geonetwork/srv/api/records/4e510f8c-7a18-4fd1-a523-517cc52ae8a3/attachments/DC_DL_RPG_2-0.pdf); [odgeo Grand Est copy](https://odgeo.grandest.fr/documentation/RPG_2/DC_DL_RPG_2-0.pdf)
- **Codes and groups.**
  - PPH = permanent grassland with no or few woody forage resources.
  - PRL = "prairie en rotation longue" (6 years or more).
  - In the RPG v2.0 nomenclature, PPH and PRL belong to group 18 "Prairies permanentes" and PTR to group 19 "Prairies temporaires". An INRAE ODR table gives the same split.
  - Sources: [INRAE ODR "Les prairies dans le RPG"](https://odr.inrae.fr/intranet/carto_joomla/index.php/ressource/documents/reseau-systeme-de-culture-systeme-de-production/rpg/3266-isop-contibution-odr-2021/file); [Telepac notice cultures 2019](https://www.telepac.agriculture.gouv.fr/telepac/pdf/tas/2019/Dossier-PAC-2019_notice_cultures-precisions.pdf); [Telepac notice 2018](https://www1.telepac.agriculture.gouv.fr/telepac/pdf/tas/2018/Dossier-PAC-2018_notice_cultures-precisions.pdf); [Telepac notice 2015](https://www3.telepac.agriculture.gouv.fr/telepac/pdf/tas/2015/Dossier-PAC-2015_notice_cultures-precisions.pdf)
- **Caveat on PRL.** A chamber of agriculture note (Ardèche, 2023) says the PRL code was removed. This conflicts with the national notices above, so check the code list for each campaign — [conf07 note2_codeculture_pp2.pdf](https://conf07.fr/wp-content/uploads/2023/04/note2_codeculture_pp2.pdf)
- **Legal definition of permanent grassland.** Under the CAP, grassland becomes permanent after **five full years** (6th CAP declaration or more). Any temporary grassland left in place becomes permanent after five years, **even if it was ploughed and resown during that period** — [Telepac fiche BCAE 1, 2026](https://www2.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2026/technique/Conditionnalite-2026_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf)
- **INRAE "RPG complété".** By Pierre Cantelaube and Benjamin Lardot (INRAE US ODR), hosted on Recherche Data Gouv, Etalab 2.0, each edition with a DOI (e.g. 10.57745/QLNGFX for Île-de-France 2023).
  - Content: completes one year of the RPG and adds agricultural parcels outside the RPG. Vector shapefiles, sources IGN and OSO/CESBIO, processed 2025.
  - Editions seen: 2018–2023, split by region or département (Île-de-France 2020–2023, Occitanie 2022–2023, Rhône-Alpes 2021, depts 29, 73, 89).
  - Sources: [b2find – RPG complété 2023 IDF](https://b2find.eudat.eu/dataset/fa17a031-59b2-534c-b0d4-75412a14bf9f); [b2find – RPG complété 2018 dpt 29](https://b2find.eudat.eu/dataset/f66fa1f8-95d8-503d-92c6-8ec0f72a48c8)

### Our reading
- **Year-to-year detection method.** A permanent → arable conversion could be flagged by geometric intersection of year N with year N+1 (2015–2025): a parcel declared PPH/PRL (group 18) in N and an arable code (group 1–17, 24–26…) in N+1.
- **Sobriety-friendly variant.** For a light product, aggregate group-18 area by commune or EPCI each year instead of tracking parcels.
- **Why intersection is required.** Without an official parcel ID that persists across years, each N/N+1 pair needs a spatial overlay. Parcel boundaries change every year, so a minimum overlap threshold is needed (e.g. >50 % of the area).
- **Temporary grassland ploughed within 5 years.** By the legal definition above, PTR ploughed before its 5th year is **not** a loss of permanent grassland. PTR → arable flows should be reported separately (normal rotation).
- **UNVERIFIED: 2010–2014.** These years were published only as anonymised îlots with the majority culture group (RPG v1, groups 18 "Prairies permanentes" / 19 "Prairies temporaires", 28 "Divers"), with no crop code per parcel. This creates a structural break in 2015: before 2015, analysis is possible only at îlot or commune level, as a share of group-18 area.
- **UNVERIFIED: other permanent-grassland codes.** The Telepac list also has other group-18 codes (e.g. SPH/SPL surfaces pastorales, BOP bois pâturés). These are rare in Normandy but should be checked in the code list for each campaign.
- **Volume.** About 845,000 parcels per year for Normandy (our figure). Downloading only the Normandy region or département files each year keeps the volume at a few hundred MB per year. Exact sizes were not checked.

### Open points
- No official "RPG historique / parcel-tracking / transitions" product from IGN, ASP or MASA was found. "RPG Explorer" and Lab'IA/INRAE parcel-tracking products could not be confirmed.
- We did not confirm whether a Normandy (or Normandy département) edition of "RPG complété" exists. Searching Recherche Data Gouv for "RPG complété Normandie" is recommended.
- The exact 2024+ code list and the schema of the new "PP" database (e.g. whether it includes the year the grassland was established) were not read, because the cartes.gouv.fr page could not be read.

## 2. Theia OSO (CESBIO) annual land-cover maps

### In short
OSO is a national raster at 10 m (some pages say 20 m), Etalab 2.0, with maps for 2018–2024 (DOIs). It has one "prairies" class mixing permanent and temporary grassland, so it can detect grassland → crop changes pixel by pixel but cannot apply the CAP "permanent" status. Theia itself reports that grassland-type and natural herbaceous classes are among the hardest to map.

### Sources
- **Catalogue entry (OSO_RASTER_L3B).** Single GeoTIFF for mainland France, from Sentinel-2 with the iota² chain and Random Forest. DOIs listed for 2018–2024 ("9 maps" in total). Licence ETALAB 2.0. The description says 20 m while the characteristics section says 10 m — [Theia hydroweb.next OSO_RASTER_L3B](https://hydroweb.next.theia-land.fr/catalog/details/OSO_RASTER_L3B)
- **Vector version (OSO VECTOR L3B).** Also exists, on CNES GEODES — [GEODES OSO vector](https://geodes.cnes.fr/?p=12386)
- **Nomenclature.** 17 classes in 2016–2017, then 23 classes from 2018 (backward compatible). Some product sheets say 24 classes. Later updates extended it towards 30 classes, adding wetlands and more agricultural classes — [Theia product sheet OSO 2020](https://www.theia-land.fr/wp-content/uploads/2024/05/FicheProduit_2020-OSO.pdf); [Planet docs CNES land cover map](https://docs.planet.com/data/public-data/other-datasets/cnes-land-cover-map/); [Theia land cover product update](https://www.theia-land.fr/?p=23764)
- **Class accuracy.** Theia reports that the agricultural classes (7) perform best. Natural environments ("lawns and heaths"), urban areas, orchards and vineyards remain hard to detect — [Theia land cover product update](https://www.theia-land.fr/?p=23764)
- **2023 Theia workshop.** Per-class precision, recall and F-score were given only for summer and winter crops (sunflower, maize, rice, soybean, rapeseed, straw cereals, protein crops), not grassland. Plans: reprocess past years with the 23-class nomenclature, then a seasonal OSO in 2024–2025 — [Theia atelier agriculture 2023, Thierion](https://www.theia-land.fr/wp-content/uploads/2023/03/PPT-AtelierAGRICULTURE2023-ART14fev_1b_Thierion-OSO-v3.pdf)

### Our reading
- **Uses in the project.** Use OSO to cross-check RPG transitions, or to see grassland loss outside the RPG (non-declared land). Its training data come from the RPG, so it is not an independent source for agricultural parcels.
- **UNVERIFIED: classes.** The 23-class nomenclature has "Prairies" separate from "Pelouses" (natural grassland). The annual crops are split into winter crops and summer crops, and further into types (straw cereals, rapeseed, maize, sunflower, soybean, protein crops, tubers, etc.). The maps are typically distributed as 10 m rasters per year. Several GB for France, so cropping to Normandy is needed.

### Open points
- **Grassland accuracy.** No published F-score for the "prairies" class in 2018–2024 was found. The per-year validation reports (labo.obs-mip.fr/multitemp) need to be checked.
- **2016–2017 and 2025.** we did not confirm whether 2016–2017 maps can still be downloaded, or whether a 2025 map exists.
- **Account.** we did not confirm whether downloading from Theia requires an account (a Login link is shown).

## 3. Copernicus HRL Grassland / Vegetated Land Cover Characteristics (VLCC), Croplands

### In short
As of 2026, CLMS provides annual 10 m pan-European grassland layers for 2017 onward (2017–2023 released). They include a **Ploughing Indicator** (years since last ploughing, per 10 m pixel, used to separate temporary from permanent grassland), Herbaceous Cover, Mowing Events and Mowing Dates. There is also a 3-yearly Grassland Change layer (20 m, 2015–2018 and 2018–2021) and a Croplands suite (Crop Types etc., 10 m yearly). This is the most directly relevant satellite product for detecting ploughing of old grassland outside the RPG.

### Sources
- **Grassland datasets on WEkEO** (identifier EO:JRC:DAT:CLMS unless marked legacy):
  - Grassland 2017–present, 10 m yearly (with confidence layer) and 100 m yearly
  - Grassland Change 2018–2021, 20 m, 3-yearly
  - Legacy (EO:EEA:DAT:HRL:GRA): Grassland Change 2015–2018 (20 m) and Grassland 2015 (20 m / 100 m)
  - Ploughing Indicator 2017–present, 10 m yearly
  - Herbaceous Cover 2017–present, 10 m yearly
  - Grassland Mowing Dates and Mowing Events 2017–present, 10 m yearly
  - Example identifier: `clms_vlcc_grassland_europe_10m_yearly_v1`
  - Source: [WEkEO help – HRL datasets transition](https://help.wekeo.eu/en/articles/16540530-hrl-datasets-transition-how-to-access-croplands-grasslands-and-tree-cover-data)
- **Cropland datasets on WEkEO** (same identifier):
  - Crop Types 2017–present, 10 m yearly, with confidence layer
  - Bare Soil Before / After
  - Cropping Seasons
  - Fallow Land Presence / Duration
  - Main Crop and Secondary Crop Emergence / Harvest / Duration
  - Source: [WEkEO help](https://help.wekeo.eu/en/articles/16540530-hrl-datasets-transition-how-to-access-croplands-grasslands-and-tree-cover-data)
- **Ploughing indicator definition.** For each 10 m pixel with herbaceous cover, it gives the number of years since the last ploughing event. It is auxiliary data used to produce the Grassland status products and to distinguish temporary from permanent grasslands — [CLMS Ploughing indicator 2019](https://land.copernicus.eu/en/products/high-resolution-layer-grasslands/ploughing-indicator-2019-raster-10-m-europe-yearly)
- **STAC collection.** On Copernicus Data Space: `clms_vlcc_ploughing-indicator_europe_10m_yearly_v1`. It continues the 2015 and 2018 PLOUGH layers (rolling archive) — [CDSE STAC](https://stac.dataspace.copernicus.eu/v1/collections/clms_vlcc_ploughing-indicator_europe_10m_yearly_v1)
- **Release timeline.** The first VLCC release (May 2025) covered 2017–2021. A later release added 2022–2023 and the United Kingdom — [GAF](https://www.gaf.de/copernicus-land-monitoring-service-releases-new-high-resolution-layers-hrls-across-europe/); [GeoVille](https://www.geoville.com/news/newsdetail/major-update-of-the-copernicus-land-monitoring-high-resolution-layers-for-the-years-2022-2023/)
- **Resolution and coverage.** Status layers are 10 m. Annual grassland and cropland layers cover EEA38. Change layers are 20 m and 3-yearly (2018–2021, 2021–2024). Crop layers start in 2017 with 17 crop classes — [GAF](https://www.gaf.de/copernicus-land-monitoring-service-releases-new-high-resolution-layers-hrls-across-europe/)
- **Methodology documents.** ATBD v2 / v2.1 — [CLMS library VLCC ATBD v2](https://library.land.copernicus.eu/products/High_Resolution_Layer_Vegetated_Land_Cover_Characteristics_ATBD_v2.html); [ATBD v2.1](https://library.land.copernicus.eu/products/products_HRL_VLCC_ATBD_v2.1.html)
- **Mowing events 2022–2023.** At the time of the GeoVille post, updates were "to be announced" — [GeoVille](https://www.geoville.com/news/newsdetail/major-update-of-the-copernicus-land-monitoring-high-resolution-layers-for-the-years-2022-2023/)

### Our reading
- **Year-to-year detection method.** A grassland pixel in year N (Grassland status) whose Ploughing Indicator resets to 0 / "ploughed this year", followed by non-grassland or crop in N+1 (Crop Types), is a direct satellite signal of retournement at 10 m.
- **Aggregation.** It can be summarised on a 1 km grid or by commune or EPCI, and is independent of CAP declarations.
- **Volume.** Normandy is about 30,000 km², i.e. about 300 million pixels at 10 m. That is roughly 300 MB per uint8 layer per year before compression. For sobriety, use STAC/COG windowed reads on the Normandy bbox, or pre-aggregate to 100 m or 1 km.
- **UNVERIFIED: account and licence.** Downloads via WEkEO or Copernicus Data Space require a free account (STAC metadata can be browsed openly). Copernicus Land data are under the Copernicus free, full and open data policy (attribution required).

### Open points
- **Accuracy.** Producer/user accuracy for the Grassland status and the Ploughing Indicator was not found. The CLMS validation reports need to be checked.
- **Login.** Whether EU Login, WEkEO or CDSE registration is strictly required was not confirmed.
- **Grassland Change 2021–2024.** Release status was not confirmed.

## 4. CLC+ Backbone, CLC+ Instances, ESA WorldCover, Dynamic World, EU Crop Map (JRC), ESA WorldCereal

### In short
CLC+ Backbone (10 m, 11 classes, 2018 / 2021 / 2023) separates "Permanent herbaceous" (class 6) from "Periodically herbaceous" (class 7, i.e. arable/ploughed). That is useful for a 3-epoch check, but 2021 accuracy (78.9 % blind validation) is below its own target. EU Crop Map (2018, 2022, 10 m, CC-BY-4.0) gives only two time points. WorldCover, Dynamic World and WorldCereal are global products that do not distinguish permanent grassland (unverified details below).

### Sources
- **CLC+ Backbone 2023 release.** 10 m, 11 major land-cover classes, EEA38 + UK. Method similar to previous years (Sentinel-2 time series + deep-learning classifier) — [CLMS news 2023 release](https://land.copernicus.eu/en/news/2023-release-of-clcplus-backbone-now-available); [CLC+ Backbone 2023 ATBD](https://library.land.copernicus.eu/products/CLCplus_Backbone_2023_ATBD_v1.html)
- **Herbaceous classes.** Class 6 = "Permanent herbaceous", class 7 = "Periodically herbaceous" (2018 metadata). The 2018 metadata quotes 90 % overall accuracy as the target value — [EEA SDI CLC+ Backbone record](https://sdi.eea.europa.eu/catalogue/copernicus/api/records/cd534ebf-f553-42f0-9ac1-62c1dc36d32c); [CLMS API clc-backbone-2018](https://land.copernicus.eu/api/en/products/clc-backbone/clc-backbone-2018)
- **2021 validation.** Below the >90 % target at EEA38 level: blind validation 78.9 %, plausibility validation 85.3 %. A 2023 validation report (dated 30/09/2025) exists, but its figures were not read — [Validation report CLC+ Backbone 2021](https://land.copernicus.eu/en/technical-library/validation-report-clcplus-backbone-2021/@@download/file); [Validation report 2023](https://land.copernicus.eu/en/technical-library/validation-report-clcplus-backbone-2023/@@download/file)
- **EU Crop Map 2022 (JRC).**
  - Coverage and method: EU-27, Sentinel-1 + Sentinel-2 + LUCAS 2022 in situ, Random Forest (primary map + gap-filling map).
  - Accuracy: overall 79.3 % for 7 major land-cover classes and 70.6 % for 19 crop types.
  - Access: JRC repository and Google Earth Engine (`JRC/D5/EUCROPMAP/V1`, 2018 and 2022), CC-BY-4.0. Paper: Ghassemi et al. 2024, *Scientific Data*, doi 10.1038/s41597-024-03884-y.
  - Sources: [JRC publication JRC136054](https://publications.jrc.ec.europa.eu/repository/handle/JRC136054); [GEE catalogue](https://developers.google.com/earth-engine/datasets/catalog/JRC_D5_EUCROPMAP_V1); [DOAJ Sci Data 2024](https://doaj.org/article/a5f52dfdb57a46eb8dbf6166d0c3b33d)

### Our reading
- **How to use CLC+ Backbone.** Comparing 2018 → 2021 → 2023 for class 6 → class 7 gives a coarse, 3-epoch view of grassland ploughing at 10 m. Classification noise (~79 % overall accuracy) will probably generate many false changes. Only use it aggregated, e.g. on a 1 km grid or by EPCI, and checked against the RPG.
- **UNVERIFIED: ESA WorldCover.** 10 m, 2020 and 2021 only, CC-BY 4.0. Classes "Grassland" vs "Cropland", with no permanent/temporary split. Two epochs from different algorithm versions, so not suitable for change detection.
- **UNVERIFIED: Dynamic World.** Google/WRI, 10 m near-real-time, 2015–present, CC-BY 4.0, via Earth Engine. Classes "grass" vs "crops" as probabilities. Noisy per scene, would need annual compositing, and depends on Earth Engine (heavy, not "sober").
- **UNVERIFIED: ESA WorldCereal.** 10 m, mainly 2021 global maps (temporary crops, maize, winter/spring cereals). It maps cropland, not grassland status, so it adds little over the RPG and HRL Crop Types for Normandy.
- **UNVERIFIED: EU Crop Map grassland.** Its legend has a single grassland class, with no permanent/temporary split.

### Open points
- Per-class accuracy of CLC+ Backbone 2023 for classes 6 and 7 was not read.
- The status of CLC+ Instances (CLC+ Core / LISA-type products) as of 2026 was not found.
- Grassland-class accuracy of EU Crop Map 2022 was not found (it is in the Sci Data paper).
- WorldCover, Dynamic World and WorldCereal details were not re-verified.

## 5. IGN OCS GE v2.0 and CoSIA

### In short
The national OCS GE has two dimensions: cover (CS) and use (US). Grassland and annual crops both fall under herbaceous cover (CS2.2.1 "Formations herbacées"), and national use code US1.1 "Agriculture" is not split nationally into pasture vs crops. So OCS GE change layers will mostly **miss** retournement (herbaceous → herbaceous, agriculture → agriculture). Only some regional enriched versions add US1.1.3 "Pâturages" / US1.1.4 "Cultures".

### Sources
- **Nomenclature.** OCS GE is two-dimensional (CS cover / US use). CS 2.2.1 "Formations herbacées" and US 1.1 "Agriculture" are separate entries. An Occitanie presentation (OCSOD) shows sub-codes US1.1.3 "Pâturages et élevages", US1.1.4 "Cultures" and US1.1.0 "Agriculture restante". The same presentation shows polygons split into "Prairies potentielles" — [openig atelier OCSOD 2025](https://www.openig.org/sites/default/files/2025-12/atelier_ocsid_partie1.pdf); [DataSud OCS GE legend](https://www.datasud.fr/fr/dataset/datasets/4810/resource/6820/download/)
- **Regional variant.** OCS GE2 Grand Est uses its own codes: "231 – Prairies, friches et délaissés agricoles" separate from crops. These cannot be mapped directly onto national CS/US codes — [DataGrandEst nomenclature OCS GE2](https://www.datagrandest.fr/portail/sites/default/files/nomenclature_finale_ocs_ge2_vf.pdf)
- **IGN product specifications.** OCS GE NG (new generation) and OCS GE — [SE_OCSGE_NG (2025)](https://geoservices.ign.fr/sites/default/files/2025-10/SE_OCSGE_NG.pdf); [SE_OCS_GE](https://geoservices.ign.fr/sites/default/files/2021-07/SE_OCS_GE.pdf)

### Our reading
- Our "bloc béton" product (OCS GE v2.0 change layers) therefore captures grassland lost to artificialisation but not ploughing. This matches the gap we identified.
- **UNVERIFIED: CoSIA.** IGN, AI on aerial orthophotos, 0.2–1.5 m. Classes include "Pelouse", "Culture" and "Terre labourée", and are derived from orthophoto missions about every 3 years per département. A pelouse → culture / terre labourée change between two campaigns could in theory capture ploughing. However, a single photo date cannot separate temporary from permanent grassland, and a recently resown field confuses the classes.

### Open points
- We did not verify whether the national OCS GE v2.0 US1.1 has official sub-classes in Normandy deliveries.
- CoSIA's exact class list and the available millésimes for Calvados, Eure, Manche, Orne and Seine-Maritime were not checked.

## 6. Agreste Teruti / Teruti-Lucas, Recensement agricole, regional Normandy sources (DRAAF OSCom, BCAE 1 ratio)

### In short
The key regional source is **OSCom** (Observatoire des sols à l'échelle communale, DRAAF Normandie + DDTM 76), built from ASP CAP surfaces and BD TOPO. It gives commune-level land-use stocks since 2008 (2008, 2013, 2018, 2023; annual balances), and underlies the Agreste figures: −103,000 ha of grassland 2008–2019, 809,000 ha in 2019, arable land +89,000 ha. On data.gouv.fr, Teruti-Lucas is only available as aggregates last updated 2019. BCAE 1 gives only a regional ratio: Normandy reference 32.94 % (2018, recalculated in 2024).

### Sources
- **Agreste Études Normandie n°6 (Sept 2021).**
  - Normandy lost 103,000 ha of grassland 2008–2019 (≈ −11 %), leaving 809,000 ha in 2019 per OSCOM, out of about 2 Mha of agricultural land.
  - Arable land gained nearly 89,000 ha; "l'artificialisation explique globalement le reste".
  - Calvados, Manche and Orne lost 71,000 ha of grassland (69 % of the regional loss) and gained 62,000 ha of arable land.
  - ¾ of ploughed grassland came from specialised dairy farms.
  - Sources cited: ASP-surfaces PAC, BDNI 2007–2018, OSCOM 2008–2019, DRAAF estimate.
  - The study maps grassland loss smoothed on 1 km² hexagons (Biweight kernel, 7.5 km radius).
  - It refers to a "Présentation de l'OSCOM 2008-2019 : consultation, couches et métadonnées".
  - Source: [Agreste Études n°6 – Prairies Normandie 2008-2019](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Agreste Études Normandie n°19 (March 2026).**
  - OSCom (DRAAF Normandie and DDTM 76) has tracked land use since 2008. Map source: "BDTOPO IGN 2012-2023 / OSCOM 2023".
  - 2023: agricultural 68.1 %, artificialised 9.2 %, natural 22.7 %.
  - 2008–2023: agricultural land −26,984 ha (−1.30 %), artificialised land +29,287 ha (+11.8 %).
  - By département: Calvados −7,462 ha, Manche −7,103, Seine-Maritime −6,689, Eure −3,705, Orne −2,025.
  - Agricultural land lost 2,786 ha in 2023 alone. National comparison: Teruti 2022.
  - Source: [Agreste Études n°19 – Occupation des sols 2008-2023](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/acces-etudes-19_isag-oscom.pdf)
- **Long-term context.** Normandy lost nearly 900,000 ha of grassland 1970–2020 — [Agreste Études n°12, agriculture normande 1970-2020](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/20220825-agreste_etudes_n12-agri_norm_70_20.pdf). The Chamber of Agriculture gives 871,000 ha of grassland in 2022 (SAA, a different definition from OSCOM) — [Chambre d'agriculture Normandie, fiche 11 prairies](https://normandie.chambres-agriculture.fr/fileadmin/user_upload/Normandie/506_Fichiers-communs/PDF/AGRISCOPIE/Panorama_agriculture/fiche_11_-_prairies_et_fourrages.pdf)
- **Teruti-Lucas on data.gouv.fr.** The dataset (Ministère de l'Agriculture, open licence) has metadata last updated July 2019 — [data.gouv.fr tag sols](https://data.gouv.fr/en/datasets/?tag=sols). Agreste published "Occupation du territoire (TERUTI) – Séries longues depuis 1982" in May 2025 — [DRAAF BFC méthodologie et sources](https://draaf.bourgogne-franche-comte.agriculture.gouv.fr/IMG/pdf/methodologie_et_sources.pdf)
- **BCAE 1 (2026).**
  - Annual ratio = permanent grassland area / total eligible area declared in the region, compared with a 2018 reference ratio.
  - Degradation >10 %: obligation to re-establish grassland.
  - Degradation between 4 % and 10 %: prior authorisation plus compensation grassland, kept in grass for at least 5 years.
  - Annex 1: Normandy reference ratio = **32.94 %**.
  - Source: [Telepac fiche BCAE 1 2026](https://www2.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2026/technique/Conditionnalite-2026_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf); 2025 version: [Telepac BCAE 1 2025](https://www.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2025/technique/Conditionnalite-2025_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf)
- **Ratio history (secondary press).** The arrêté of 31 Oct 2023 showed Normandy at −6.45 %, the largest drop (Grand Est −3.42 %, Bretagne −4.60 %, Pays de la Loire −5.20 %). Regulation (EU) 2024/1235 allowed a one-time recalculation: Normandy's 2018 ratio went from 34.93 % to 32.94 %. Normandy, Pays de la Loire, Bretagne and Grand Est escaped the authorisation/interdiction regimes for 2025, retroactive to 1 Jan 2024 — [Réussir – PAC et prairie permanente](https://www.reussir.fr/chevre/pac-et-prairie-permanente-quelles-sont-les-regles-de-retournement); [Réussir Lait – 4 régions](https://www.reussir.fr/lait/prairies-permanentes-4-regions-en-regime-dautorisation-ou-dinterdiction)
- **CSRPN Normandie.** Its motion of 12 Dec 2024 on grassland exists on the DREAL Normandie site. It could not be opened — [motion CSRPN 2024-12-12](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf)

### Our reading
- **The 82 % / 18 % split.** Our project notes' figure ("82 % to arable, 18 % to artificialisation") is not stated as such in Agreste n°6 text extracted here. That text gives −103,000 ha of grassland and +89,000 ha of arable land (≈86 % if it were all from grassland), with artificialisation as "the rest". The split may be in a part of the document we did not read, so check the exact wording before quoting it.
- **Teruti.** It is a statistical point survey, usable only as regional or national aggregates. It is not suitable for EPCI or commune maps.
- **OSCom.** It is the closest existing "official" commune-level grassland stock series for Normandy (2008–2023). If its layers are published (on the DRAAF site or a GéoNormandie / CRAIG-type portal), it would let us validate an RPG-based EPCI indicator.
- **Thresholds 2025 vs 2026.** One secondary summary said the 2025 fiche used 5 % as a threshold, but the 2026 fiche text read directly says 4 % and 10 %. Use the 2026 text.

### Open points
- **OSCom access.** Not confirmed: where the OSCom layers are published (URL), their licence, and whether the grassland item is at commune scale.
- **Recensement agricole 2010/2020 STH by commune.** Availability was not checked. Communal data are subject to statistical secrecy, so expect blanked cells.
- **Annual ratio values.** Normandy's annual BCAE 1 ratios for 2023–2025 (not just the reference) were not found in a primary source (the arrêtés).
- **Other regional layers.** No DRAAF, DREAL, ANBDD or Région layer specific to "prairies retournées" was found beyond OSCom and the Agreste studies.
