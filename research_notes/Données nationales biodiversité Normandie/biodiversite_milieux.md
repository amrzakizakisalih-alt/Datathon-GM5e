# National & European open datasets on biodiversity, species, habitats and ecological continuity, usable for Normandy (Datathon Normandie 2026)

Scope: quick inventory, as of 17 Oct 2026. Excludes datasets we already use (patrinat_* WFS ZNIEFF/N2000/protected areas, HAIES.BOCAGES, RPG, BCAE, CLC, BD Forêt, GBIF, Naïades/Hub'Eau, Phytatmo). "P1" = problem 1 (where to prioritise restoration); "P2" = problem 2 (human–nature interaction indicators).

Verification legend: **[V]** existence/access checked; **[V-partial]** existence confirmed but some fields (licence, format, Normandy coverage) not confirmed; **[NV]** known candidate, NOT verified (listed under Open points only).

## Species and observations beyond GBIF

### In short
OpenObs (INPN/SINP, PatriNat) is the main national observation source beyond GBIF, with a documented public API; species status tables (BDC statuts / protected and regulated species, MNHN) are freshly updated on data.gouv.fr (3 Oct 2026) but the licence is not stated on the data.gouv page. ONB indicators are national-level; raw STOC data were not found as an open download.

### Sources
**1. OpenObs – observations d'espèces (SINP national) [V]**
- Producer: UMS PatriNat (OFB, CNRS, MNHN); French portal for species observation data of the INPN, the national SINP platform; gives open access to non-sensitive public data, occurrence and synthesis data — [GBIF Living Atlases – OpenObs](https://living-atlases.gbif.org/participants/openobs)
- Access: Swagger API docs at https://openobs.mnhn.fr/api/docs; Biocache Service at openobs.mnhn.fr/biocache-service/; code on GitHub (gbiffrance) — [GBIF Living Atlases – OpenObs](https://living-atlases.gbif.org/participants/openobs)
- Volume: 134,922,015 observation records as of July 2023; built on the Atlas of Living Australia (ALA) stack, first version 2020 — [GBIF Living Atlases – OpenObs](https://living-atlases.gbif.org/participants/openobs)
- data.gouv.fr entry "INPN – Données d'observation et de suivi sur les espèces" points to OpenObs as the consultation/download tool; SINP aims at free, open release of naturalist data — [data.gouv.fr – INPN observations](https://www.data.gouv.fr/datasets/inpn-donnees-dobservation-et-de-suivi-sur-les-especes)
- Caveat: some cached biocache-service occurrences/search pages returned HTTP 500 — endpoint may be unstable; plan a fallback (bulk download per département) — [search-result observation of openobs.mnhn.fr redirect pages](https://openobs.mnhn.fr/redirect/inpn/taxa/922315?view=map)
- Use: P1 (species richness / heritage-species hotspots per grid cell or commune; overlap with degraded habitats); P2 (observation effort as a human–nature engagement proxy).
- Normandy coverage: national (metropolitan France) — sensitive species are blurred/withheld (non-sensitive data only).

**2. INPN – Espèces protégées et réglementées (BDC statuts linked to TAXREF) [V-partial]**
- Producer: MNHN; ZIP (49.2 KB per data.gouv page metadata), metadata updated 3 Oct 2026; download https://www.data.gouv.fr/api/1/datasets/r/9169283d-e2d2-415e-a3ea-157380b3b097 — [data.gouv.fr – INPN espèces protégées et réglementées](https://www.data.gouv.fr/datasets/inpn-especes-protegees-et-reglementees)
- Licence: "License Not Specified" on the data.gouv page (site footer = Licence Ouverte 2.0, but not confirmed for the dataset) — FLAG — [data.gouv.fr](https://www.data.gouv.fr/datasets/inpn-especes-protegees-et-reglementees)
- TAXREF version not stated on the page; the ZIP size (49 KB) suggests it may be a pointer/partial file — the full BDC statuts table is normally on inpn.mnhn.fr (the URL https://inpn.mnhn.fr/telechargement/referentielEspece/bdc-statuts-especes returned HTTP 404) — [data.gouv.fr](https://www.data.gouv.fr/datasets/inpn-especes-protegees-et-reglementees)
- Use: P1 (weighting observations by protection / Red List status — key prioritisation criterion); P2 (share of threatened species).

**3. Red Lists (national & regional)**
- Normandy regional Red Lists are produced by regional bodies (e.g. reptiles validated by Normandy CSRPN 13/01/2022, birds by Groupe Ornithologique Normand, mammals by Groupe Mammalogique Normand) — out of scope as "regional producers", but statuses are typically integrated into BDC statuts — [Liste rouge des Reptiles de Normandie (LASHF)](https://lashf.org/wp-content/uploads/2022/08/Liste-rouge-des-Reptiles-de-Normandie.pdf)
- Normandy ZNIEFF-determinant list (DREAL, 2024) notes it has not benefited from the latest TAXREF updates (v15) — taxonomic joins will need TAXREF harmonisation — [DREAL Normandie – liste espèces dét. ZNIEFF 2024](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/02-2024-liste-synthetique-especes-det-znieff-normandie.pdf)

**4. ONB indicators / Vigie-Nature STOC [V-partial]**
- ONB is steered by OFB with SDES (CGDD); ~100 indicators published on naturefrance.fr; STOC (participatory monitoring) first data 1989 — [ONB presentation, Séminaire données biodiversité 2021](https://seminaire-donnees-biodiversite.naturefrance.fr/wp-content/uploads/sites/30/2021/05/SeminaireDonneesBiodiversite_05_ONB.pdf)
- ONB indicator "Évolution des oiseaux communs spécialistes" is built on STOC (random listening points across the national territory); STOC coordinated by MNHN and LPO — [RNF consultation STOC (2026)](https://reserves-naturelles.org/wp-content/uploads/2026/04/consultation_stoc_zpf.pdf)
- Use: P2 (headline trend indicators: common birds, artificialisation, etc.) — but mostly national, not regional.

### Our reading
- OpenObs + BDC statuts is the core species stack: join on CD_NOM (TAXREF) to compute "heritage species" layers per 1 km / 5 km grid for Normandy.
- ONB indicators are mainly national; useful as benchmarks for a Normandy dashboard rather than as spatial inputs.

### Open points
- Exact TAXREF version (v18 expected) and licence of the current BDC statuts table not confirmed; the INPN download page URL tried returned 404.
- No open download of raw STOC/Vigie-Nature data found; ONB territorial (regional) breakdowns not verified.
- UICN France national Red List open tables not checked (likely included in BDC statuts).
- OpenObs volume for Normandy specifically and current (2026) total not found.

## Habitats and wetlands

### In short
CarHab now covers ~91% of mainland France, but Normandy is NOT among the regions fully covered — check département by département. The INRAE "milieux potentiellement humides" raster (50 m, 2014) is national but old. EEA Natura 2000 end-2024 tabular data adds habitats/species per site. Copernicus HRL Small Woody Features 2021 (5 m) is new (published Sept 2025) but requires an EEA/CLMS login.

### Sources
**5. CarHab – cartographie nationale des habitats (MTE/OFB/MNHN/IGN) [V-partial]**
- 91% of mainland France + Corsica mapped, 88 départements covered; the 8 regions covered at 100% do not include Normandy → partial Normandy coverage (which of 14/27/50/61/76 is unknown) — [Ministère – programme CarHab](https://www.ecologie.gouv.fr/politiques-publiques/carhab-programme-cartographie-nationale-predictive-habitats-naturels)
- Data for 44 départements available as open data on the INPN CarHab page (figure dated Sept 2024, outdated) + map viewer; target: national map at 1:25,000 by 2026 — [Ministère – programme CarHab](https://www.ecologie.gouv.fr/politiques-publiques/carhab-programme-cartographie-nationale-predictive-habitats-naturels); programme page [INPN – CarHab](https://inpn.mnhn.fr/programme/carhab?lg=en) (the FR URL returned 404)
- Département datasets are published on INPN as "jeux de données" (e.g. Meurthe-et-Moselle: habitats from cross of biotopes × vegetation physiognomy) — [INPN – CarHab Meurthe-et-Moselle](https://inpn.mnhn.fr/habitat/jeudonnees/88407?lg=en)
- Use: P1 (the key layer for degraded/fragmented semi-natural habitats, at 1:25,000).

**6. Enveloppes des milieux potentiellement humides de France métropolitaine (INRAE / Agrocampus Ouest) [V]**
- Producer: UMR 1069 SAS INRAE – Agrocampus Ouest / US 1106 InfoSol INRAE; GeoTIFF raster, 50 m resolution, published 01/02/2014; probability classes (très forte / forte / importante) — [data.gouv.fr – Superficies des zones potentiellement humides par département](https://www.data.gouv.fr/datasets/superficies-des-zones-potentiellement-humides-par-departement-france-metropolitaine-corse)
- Departmental aggregate dataset also on data.gouv.fr — same source.
- Outdated (2014 model) — FLAG.
- Related, basin-scale (Agence de l'eau Seine-Normandie, a state body): "Prélocalisation des zones humides potentielles dans le bassin Seine-Normandie" (shapefile, WMS, WFS) — covers Seine-Normandie basin (most of Normandy; western Manche/Orne parts may fall under Loire-Bretagne basin — not verified) — [data.gouv.fr – Prélocalisation ZH Seine-Normandie](https://www.data.gouv.fr/datasets/prelocalisation-des-zones-humides-potentielles-dans-le-bassin-seine-normandie)
- Use: P1 (wetland restoration potential: potential wetland minus current artificial/arable land use).

**7. EEA – Natura 2000 (tabular) version end 2024 (+ rev. 01) [V-partial]**
- EEA catalogue lists "Natura 2000 (vector) – version end 2024" (CC-BY 4.0) and "Natura 2000 (tabular) – version end 2024" + "rev. 01"; descriptive data come from national Standard Data Forms (species and habitat types per site) — [EEA SDI catalogue record](https://sdi.eea.europa.eu/catalogue/srv/api/records/91357f39-7866-41ce-b447-43905c364ec8)
- Per-site SDFs also on INPN as PDF + XML (reference database July 2024) — [INPN – site FR7401128](https://inpn.mnhn.fr/site/natura2000/FR7401128/tab/documentaion?lg=en)
- Use: P1 (conservation status/representativity of Annex I habitats per site → which N2000 sites hold habitats in poor condition). Boundaries already known; the TABULAR part is the added value.

**8. Copernicus HRL Small Woody Features 2021 / Small Landscape Features (EEA/CLMS) [V]**
- 5 m raster (SWF 2021), 100 m density raster, Woody Vegetation Layer 2021; published 30 Sept 2025, temporal coverage 2021–2022; vector GeoPackage published 21 Oct 2025; 100×100 km tiles on EEA grid; GeoTIFF + WMS — [EEA – CLMS HRL datasets](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-high-3/)
- Downloads require authentication (free EEA/CLMS account) — FLAG — [EEA – CLMS HRL datasets](https://www.eea.europa.eu/data-and-maps/data/copernicus-land-monitoring-service-high-3/)
- Content: hedgerows/linear structures + woody patches 200–5000 m²; PUM covers 2018→2021 change detection — [CLMS PUM HRL SLF 2021](https://library.land.copernicus.eu/products/High_Resolution_Layer_CLMS_PUM_HRLSLF_v1.pdf)
- Use: P1 (bocage fragmentation, 2018–2021 hedgerow loss as a European cross-check of IGN HAIES); complements rather than duplicates HAIES.BOCAGES.

### Our reading
- For Normandy, CarHab gaps likely mean a mixed approach: CarHab where available + CLC/HRL + potential wetlands elsewhere.
- Wetland potential (INRAE 2014) × RPG arable/urban = simple "restorable wetland" indicator for P1.

### Open points
- CarHab availability per Normandy département not confirmed (INPN programme page returned 404; search returned nothing). Must check https://inpn.mnhn.fr/programme/carhab manually.
- Copernicus HRL Grassland 2021/2023, Water & Wetness, Tree Cover Density, ESA WorldCover (10 m, 2020/2021, CC-BY 4.0) and EEA Ecosystem Types map — [NV] not verified.
- RAMSAR / "inventaires nationaux zones humides" via sig.reseau-zones-humides.org — not checked.
- Licence of the Seine-Normandie prélocalisation dataset not checked; exact basin overlap with Normandy not checked.

## Continuities & fragmentation (ROE, TVB, trame noire / light pollution, road-kill)

### In short
The ROE (OFB) is the key national river-continuity dataset (>104,000 obstacles in 2020, continuously updated, CSV/SHP). No national open trame-noire / light-pollution dataset was found on data.gouv.fr (only metropolitan datasets for Aix-Marseille and Grand Paris). No open road-kill dataset found.

### Sources
**9. ROE – Référentiel des Obstacles à l'Écoulement (OFB, with Sandre) [V]**
- National participatory referential coordinated by OFB, continuously updated incl. overseas; attributes: location, name, type, state, low-water drop height class, fish-pass devices — [data.gouv.fr – Obstacles à l'écoulement Guadeloupe (OFB-ROE/Sandre)](https://www.data.gouv.fr/datasets/obstacles-a-lecoulement-guadeloupe)
- >104,000 obstacles in mainland France (Dec 2020), census acknowledged incomplete — [OFB 2020 report](https://www.bourgogne-franche-comte.developpement-durable.gouv.fr/IMG/pdf/202012_ofb_valorisation_oe_indicateurs_final_cle541e85.pdf)
- CSV and SHP downloads on data.ofb.fr catalogue; list also consultable on Sandre site — [data.gouv.fr OFB records, excerpt](https://www.data.gouv.fr/datasets/obstacles-a-lecoulement/informations)
- data.gouv.fr "Obstacles à l'écoulement ROE" record: producer Agence de l'eau Seine-Normandie, Licence Ouverte 2.0, last update 18 June 2024, spatial coverage metropolitan France; no direct file URL on the page — [data.gouv.fr – Obstacles à l'écoulement ROE](https://www.data.gouv.fr/datasets/obstacles-a-lecoulement/informations)
- Département extract exists for Orne (Sandre, validity May 2022) — [data.gouv.fr – ROE Orne 2022](https://www.data.gouv.fr/datasets/referentiel-des-obstacles-a-lecoulement-roe-pour-les-obstacles-situes-sur-les-cours-deau-du-departement-de-lorne-en-2022)
- Use: P1 (obstacle density per river km / per BV; prioritising dam removal / fish passes for migratory fish – Normandy salmon/eel rivers); P2 (pressure indicator).

**10. Trame noire / light pollution [no national dataset found]**
- data.gouv.fr trame-noire datasets found are local: Aix-Marseille-Provence (Cerema, LUOJIA-1 2018 images at 130 m, updated 22 Aug 2024) and Métropole du Grand Paris (2022 satellite radiance, Licence Ouverte, chiroptera habitat rasters) — [data.gouv.fr – Trame noire](https://www.data.gouv.fr/datasets/trame-noire); [data.gouv.fr – MGP trame noire biodiversité](https://www.data.gouv.fr/datasets/nature-trame-noire-enjeux-de-la-pollution-lumineuse-sur-la-biodiversite)
- Some of these records show licence "non spécifiée" despite the description citing Licence Ouverte — FLAG — same sources.

### Our reading
- For Normandy, a light-pollution layer would have to be derived from global satellite night-light products (e.g. VIIRS/Black Marble from NASA/NOAA — not verified here) — not a French national dataset.
- ROE + BD TOPAGE (not checked) gives a computable "fragmentation per stream segment" metric.

### Open points
- Current ROE version/date on data.ofb.fr and Sandre (2025/2026) not checked; volume for Normandy unknown.
- National TVB datasets (SRCE are regional; national "continuités écologiques" layers on Géoplateforme) — not checked.
- ICE (Informations sur la Continuité Écologique, OFB fish-passability) — not checked.
- Road-kill / wildlife-collision open data: none found.
- National light-pollution map (e.g. DarkSkyLab/OFB "trame noire" national) — not found.

## Forest biodiversity (IGN Inventaire forestier, old-growth forests, ONF réserves biologiques)

### In short
IGN's raw National Forest Inventory data (plots + trees + eco-floristic data) are on data.gouv.fr under Licence Ouverte (updated 30 June 2026), with plot coordinates at 1 km precision; a separate "Indices écologiques" dataset (campaigns 2005–2018) adds ecological indices.

### Sources
**11. Données brutes de l'inventaire forestier (IGN) [V]**
- Producer IGN; Licence Ouverte; last update 30 June 2026; ~6,000 plots/year, ~60,000 tree measurements/year, eco-floristic data, incl. poplar stands; coordinates given to the nearest km; data.gouv resource is an HTML link (15.3 KB) to the IGN Inventaire forestier site — https://www.data.gouv.fr/api/1/datasets/r/5c9b5781-0010-4497-8adf-539e9a7a77ef — [data.gouv.fr – Données brutes IFN](https://www.data.gouv.fr/datasets/donnees-brutes-de-l-inventaire-forestier)
- Use: P1 (deadwood, very large trees, stand structure, species composition → forest naturalness / habitat quality by sylvo-ecoregion; Normandy is fully covered by the systematic grid but sample density per département is limited).

**12. Indices écologiques de l'inventaire forestier (IGN) [V-partial]**
- Complement to raw data; ZIP "Données brutes et indices écologiques – campagnes 2005 à 2018" with CSV files — [data.gouv.fr – Indices écologiques IFN](https://www.data.gouv.fr/datasets/indices-ecologiques-de-linventaire-forestier)
- Possibly outdated (2018 last campaign) — FLAG.

### Our reading
- With 1 km coordinate blurring, IFN is best aggregated at sylvo-ecoregion / département level, not used pixel-wise.

### Open points
- Old-growth / subnatural forest datasets (e.g. WWF "forêts subnaturelles", "forêts anciennes" from État-major maps by IGN/INRAE) — not checked.
- ONF réserves biologiques: probably within patrinat protected-area layers already known (RB intégrales/dirigées), not separately checked.

## Marine & coastal biodiversity (OFB AMP, Ifremer/Sextant, EMODnet)

### In short
EMODnet EUSeaMap (EUNIS 2019 predictive seabed habitats) covers the Channel coast; the 2023 version is archived and superseded by a 2025 release.

### Sources
**13. EMODnet Seabed Habitats – EUSeaMap broad-scale predictive habitat map [V]**
- 2023 version archived, superseded by the 2025 version; 2023 zip download: https://files.emodnet-seabedhabitats.eu/data/EUSeaMap_2023.zip; WMS available; separate substrate layer; classified EUNIS 2019 level 3 (and level 2, other schemes); covers NE Atlantic incl. Channel — [EMODnet catalogue – EUSeaMap 2023](https://emodnet.ec.europa.eu/geonetwork/srv/api/records/0a1cb988-22de-48b2-8cda-d90947ef77d1)
- Licence CC-BY 4.0 per a secondary source (Marine Scotland) — verify on EMODnet record — [marine.gov.scot](https://marine.gov.scot/?q=maps/68)
- Method report on Ifremer Archimer — [Archimer 00859/97116](https://archimer.ifremer.fr/doc/00859/97116)
- Use: P1 (coastal/marine habitat priorities: e.g. seagrass/maerl potential zones off Manche/Calvados; overlap with fishing/port pressures).

### Our reading
- Use the 2025 EUSeaMap release (link from the EMODnet catalogue record / https://emodnet.ec.europa.eu/en/seabed-habitats) rather than 2023.

### Open points
- OFB marine protected areas (AMP) layer, Ifremer Sextant layers (e.g. herbiers de zostères, REBENT), EMODnet Biology — not checked.
- Exact URL and licence of EUSeaMap 2025 not verified.

## Summary table of verified items

| # | Dataset | Producer | Access | Format / resolution | Time / update | Licence | Normandy |
|---|---|---|---|---|---|---|---|
|1|OpenObs|PatriNat (OFB/CNRS/MNHN)|openobs.mnhn.fr/api/docs|API (biocache), CSV|continuous|open (non-sensitive)|full|
|2|BDC statuts / espèces protégées|MNHN|data.gouv ZIP|tabular|upd. 3 Oct 2026|NOT specified on page|n/a (taxa)|
|5|CarHab|MTE/OFB/MNHN|inpn.mnhn.fr/programme/carhab|vector 1:25,000|by dept, target 2026|open (per ministry)|PARTIAL|
|6|Milieux potentiellement humides|INRAE/Agrocampus|data.gouv|GeoTIFF 50 m|2014|open|full, OLD|
|7|Natura 2000 tabular end 2024|EEA|sdi.eea.europa.eu|tabular + vector|end 2024|CC-BY 4.0 (vector)|full|
|8|HRL Small Woody Features 2021|EEA/CLMS|eea.europa.eu / land.copernicus.eu|GeoTIFF 5 m, 100 m; GPKG|2021, pub. Sept–Oct 2025|open, LOGIN required|full|
|9|ROE|OFB/Sandre|data.ofb.fr, data.gouv|CSV, SHP points|continuous; dg record 2024|LO 2.0|full|
|11|IFN données brutes|IGN|data.gouv → inventaire-forestier.ign.fr|CSV, 1 km blurred plots|upd. 30 Jun 2026|Licence Ouverte|full|
|12|IFN indices écologiques|IGN|data.gouv|CSV|2005–2018|(LO assumed, NV)|full|
|13|EUSeaMap|EMODnet|files.emodnet-seabedhabitats.eu|vector EUNIS 2019|2023 (archived) / 2025|CC-BY 4.0 (secondary)|full coast|
