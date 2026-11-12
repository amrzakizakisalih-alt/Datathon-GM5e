# National open datasets: socio-economic context and public/private actions for nature (usable for Normandy)

Scope: datasets from NATIONAL producers (State, INSEE, OFB, Urssaf, Cerema, IGN, OFGL, EU), covering the 5 Normandy départements (14 Calvados, 50 Manche, 61 Orne, 27 Eure, 76 Seine-Maritime). Status checked 17 Oct 2026. Quick inventory: existence, access link and main metadata verified on the landing page; columns/content not deep-dived unless stated.

## Q1. Restoration / nature actions and funding ("positive interactions" side)

### Takeaway
The strongest national, project-level, geocodable source is the **Fonds vert project list** (CSV/XLSX, 2023–2025 vintages, commune code, Etalab 2.0, includes dedicated "Fonds vert Biodiversité" files), complemented by **Cartofriches** (brownfield sites with a Cerema "renaturation" mutability index), the **ABC (Atlas de la biodiversité communale)** list from OFB, and the **EU LIFE project database** (exportable). Several items on the wish list (Label bas-carbone registry, TEN, Agences de l'eau aid, Natura 2000 contracts, Conservatoire du littoral parcels) have NO clean national open-data file: they exist as web listings/maps or PDFs only.

### Cited Findings

**D1 — Fonds Vert – Liste des projets subventionnés** (producer: Ministère de la Transition écologique)
- URL: https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/ — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/)
- Format CSV + XLSX, 10 files incl. "Fonds vert Biodiversité" files; dataset last updated 28 July 2026; vintages 2023, 2024, 2025 (a project is in vintage N when its grant was committed before 31 Dec N) — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/)
- Unit: one row per project × beneficiary; location = "code commune" column, often empty for intercommunal/departmental/regional projects, and sometimes the sponsor's commune rather than the project site; no coordinates mentioned — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/)
- Licence Licence Ouverte / Etalab 2.0 — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/)
- Scale: 2023–2025 Fonds vert financed >25,000 projects, €4.5bn of grants, >13,000 beneficiaries; budget programme P380 — [data.gouv.fr search snippet of dataset description](https://www.data.gouv.fr/datasets/66a215a463a9da4fb801b8cf)
- Normandy: national coverage, so Normandy included (filter by code commune / département).
- Use: Problem 2 (map of public "positive" actions: renaturation, biodiversity, friches, adaptation, per commune; € per capita indicators); Problem 1 (where restoration is already funded vs. gaps).

**D2 — Sites référencés dans Cartofriches** (producer: Cerema, national inventory of brownfield sites)
- URL: https://www.data.gouv.fr/datasets/sites-references-dans-cartofriches/ — [data.gouv.fr](https://www.data.gouv.fr/datasets/sites-references-dans-cartofriches/)
- Inventory is explicitly a SAMPLE of existing friches and heterogeneous across the territory; data dictionary (Nov 2021) in resources — [data.gouv.fr](https://www.data.gouv.fr/datasets/61892a26c94e39bde1dbf7ac/)
- Includes Cerema-computed mutability indices P_PV, P_residentiel, P_equipement, P_tertiaire, P_industriel and **P_renaturation** — [data.gouv.fr discussion](https://www.data.gouv.fr/datasets/sites-references-dans-cartofriches/discussions)
- One page indicates an update on 23 July 2026 (not confirmed) — [search result](https://www.data.gouv.fr/datasets/sites-references-dans-cartofriches/)
- Beware: a separate dataset titled just "Cartofriches" is a Loiret extract (last update Apr 2023), not the national file — [data.gouv.fr](https://www.data.gouv.fr/datasets/cartofriches)
- Unit: site (point/polygon). Format and licence not verified this session.
- Use: Problem 1 (renaturation opportunities on brownfields, feasibility via P_renaturation; fits ZAN and "territorial development" narrative).

**D3 — Données des Atlas de la biodiversité communale (ABC) en France métropolitaine et outre-mer** (producer: OFB)
- URL: https://www.data.gouv.fr/datasets/donnees-des-atlas-de-la-biodiversite-communale-en-france-metropolitaine-et-outre-mer — [data.gouv.fr](https://www.data.gouv.fr/datasets/donnees-des-atlas-de-la-biodiversite-communale-en-france-metropolitaine-et-outre-mer)
- Dataset page last updated 8 Oct 2026; resources dated 14 Feb 2023 to 25 Nov 2025; 4 resources are URL links; licence CC-BY; metadata quality 56%, "some files not available" — [data.gouv.fr](https://www.data.gouv.fr/datasets/donnees-des-atlas-de-la-biodiversite-communale-en-france-metropolitaine-et-outre-mer)
- Points to https://abc.naturefrance.fr/, which lists ABCs funded by OFB and inventoried by the Ministry; the list of ABC projects can be consulted and downloaded there — [data.gouv.fr](https://www.data.gouv.fr/datasets/donnees-des-atlas-de-la-biodiversite-communale-en-france-metropolitaine-et-outre-mer)
- OFB supports new ABCs each year (e.g. 2023: 76 projects covering 394 communes) — [OFB press release 2023](https://www.ofb.gouv.fr/sites/default/files/Fichiers/Presse/cp-laureats-abc-juillet2023.pdf); programme page updated 8 Sep 2025 — [OFB](https://ofb.gouv.fr/les-atlas-de-la-biodiversite-communale)
- Unit: project / commune(s). Normandy: national, included.
- Use: Problem 2 (commune-level "engagement for nature" indicator; good-practice communes); Problem 1 (communes with knowledge base = higher feasibility).

**D4 — Territoires engagés pour la nature (TEN)** (producer: OFB / regional steering groups)
- No data.gouv.fr dataset or CSV export found; OFB hosts a searchable list + map (≈621 members at crawl time) with collectivity name and population class — [OFB](https://ofb.gouv.fr/territoires-engages-nature?page=2)
- Normandy: 18 laureates announced Dec 2019 (regional press release) — [Préfecture de région Normandie](https://www.prefectures-regions.gouv.fr/normandie/Actualites/Annonce-officielle-des-laureats-normands-du-dispositif-Territoires-engages-pour-la-nature)
- NOT TRULY OPEN DATA: would require scraping the OFB listing. Use: Problem 2 (engaged-collectivity flag).

**D5 — LIFE Public Database (EU, CINEA)**
- URL: https://webgate.ec.europa.eu/life/publicWebsite/search/advanced — Advanced Projects Search with export option — [LIFE Public Database](https://webgate.ec.europa.eu/life/publicWebsite/search/advanced)
- Database covers all LIFE projects since 1992; public dashboard filterable by country, city, sub-programme, beneficiaries, financing; updated daily — [CINEA news](https://cinea.ec.europa.eu/news-events/news/new-public-life-projects-dashboard-promotes-transparency-and-understanding-2023-07-27_en); [data.europa.eu](https://data.europa.eu/en/news-events/news/discover-all-cinea-programmes-new-dashboard)
- Unit: project (beneficiary city; no fine geolocation). Licence: EC reuse policy (not verified). France filter not confirmed against live site.
- Use: Problem 2 (large EU-funded nature/climate projects in Normandy, e.g. estuary/wetland projects), benchmark of good practices.

**D6 — Aides-territoires API** (producer: ANCT / beta.gouv)
- API https://aides-territoires.beta.gouv.fr/api/ (docs at /api/docs), v1.8.1; Licence Ouverte 2.0 — [Aides-territoires data page](https://aides-territoires.beta.gouv.fr/data/)
- **REQUIRES AN ACCOUNT**: API key from account settings, exchanged for a Bearer token valid 24h — [Aides-territoires data page](https://aides-territoires.beta.gouv.fr/data/)
- Content: ~3,000 public aid schemes (sponsor, description, nature, geographic area, eligibility, link); also a downloadable dataset on data.gouv.fr — [data.gouv.fr dataservice](https://www.data.gouv.fr/dataservices/api-aides-territoires); [data.gouv.fr dataset](https://www.data.gouv.fr/datasets/aides-financieres-et-en-ingenierie-disponibles-pour-les-collectivites-territoriales-et-leurs-partenaires-locaux)
- Note: these are AVAILABLE aid schemes (offers), not funded projects.
- Use: Problem 1 feasibility (which funding levers exist for a given restoration type/territory); policy recommendation layer for elected officials.

**Agence de l'eau Seine-Normandie (AESN) aid** (national public body; Normandy fully in the Seine-Normandie basin)
- Awards published on AESN website as "Commission des aides – bilan des aides signées"; no open-data dataset URL found — [Préfecture IDF](https://www.prefectures-regions.gouv.fr/ile-de-france/Region-et-institutions/L-action-de-l-Etat/Amenagement-du-territoire-transport-et-environnement/Environnement/Eau/L-agence-de-l-eau-attribue-132-millions-d-euros-d-aides-pour-1-200-projets-pour-l-eau-sur-le-bassin-Seine-Normandie)
- AESN Normandy 2024 note: €643M of aid for 3,850 projects (basin-wide figure as reported) — [economie.eaufrance.fr](https://economie.eaufrance.fr/sites/default/files/2024-05/doc538-aesn_notenormandie2024.pdf)

**Label bas-carbone**
- A national "registre de projets du Label bas carbone" exists (data cited as of 8 Oct 2025, by region and forest/agri type) but no public download link found — [DREAL BFC presentation](https://www.bourgogne-franche-comte.developpement-durable.gouv.fr/IMG/pdf/colloque_lbc_pleniere_dgec_dreal_.pdf)
- Only a regional extract exists on data.gouv.fr (Nouvelle-Aquitaine, Apr 2024, licence "not specified") — [data.gouv.fr](https://www.data.gouv.fr/datasets/nouvelle-aquitaine-label-bas-carbone)
- Framework revised by Décret 2025-917 and arrêté of 5 Sep 2025 — [DREAL Grand Est leaflet 2026](https://www.grand-est.developpement-durable.gouv.fr/IMG/pdf/20260306-lbc-plaquette-w.pdf)

**Conservatoire du littoral**
- data.gouv.fr organisation page shows 0 datasets — [data.gouv.fr](https://www.data.gouv.fr/organizations/conservatoire-du-littoral/datasets); a regional PACA "domaine protégé" layer exists (2024) — [DataSud](https://www.datasud.fr/geonetwork/srv/api/records/0f7421f8-fbc4-4110-bdc2-3d74292f58fd)

### Inferences
- Fonds vert is the backbone for a "public positive actions" indicator: aggregate € and project counts per commune/EPCI, per measure (biodiversity, renaturation, friches), normalised by population (link D8). The missing-commune-code caveat means EPCI-level aggregation is safer.
- Cartofriches × Fonds vert "friches" × consommation d'espaces gives a strong ZAN/territorial-development story for elected officials.
- Conservatoire du littoral land (sites/parcels) is most likely obtainable through INPN's protected-area layers ("Terrains du Conservatoire du littoral") — NOT verified this session; check https://inpn.mnhn.fr (espaces protégés downloads).

### Gaps
- France 2030 / France Relance "fonds friches" project lists: not searched due to time; a "Fonds friches lauréats" dataset may exist on data.gouv.fr (unverified).
- Natura 2000 contracts/charters: no national open dataset found or searched in depth; contract data is typically held by DREAL/ASP, likely not open.
- Obligations réelles environnementales (ORE): no national public registry found (ORE are notarial acts; no open list known).
- Exact Fonds vert column names / measure labels not verified.
- Agence de l'eau aid in machine-readable form: not found.

## Q2. Public spending (collectivités budgets, environment function)

### Takeaway
**data.ofgl.fr** (OFGL, from DGFiP balances) is the national open source for local government finances by commune/EPCI/département/région, updated each summer (2024 definitive data available); a "Comptes des communes 2018-2025" dataset also exists on data.gouv.fr. Environment spending by function requires the account-detail module and the functional nomenclature (M57/M14) — not verified.

### Cited Findings
**D7 — OFGL data.ofgl.fr (comptes des collectivités / balances comptables DGFiP)**
- Covers communes, GFP, ensembles intercommunaux, départements, régions, syndicats, EPL, SDIS; a module lets users drill into each account of DGFiP balances; updated every summer after DGFiP publication — [collectivites-locales.gouv.fr](https://www.collectivites-locales.gouv.fr/index.php/actualites/les-donnees-financieres-2024-sont-pretes-etre-analysees-sur-dataofglfr)
- Definitive 2024 data available — [collectivites-locales.gouv.fr](https://www.collectivites-locales.gouv.fr/index.php/actualites/donnees-financieres-definitives-2024-disponibles-sur-dataofglfr)
- "Comptes des communes 2018-2025" on data.gouv.fr computed by OFGL from DGFiP balances — [data.gouv.fr](https://www.data.gouv.fr/datasets/comptes-des-communes-2018-2025/discussions)
- Unit: collectivity (SIREN / code commune). Normandy: national, included.
- Use: Problem 2 (public effort indicator: environment/aménagement spending per inhabitant per commune/EPCI); Problem 1 (fiscal capacity as feasibility proxy).

### Inferences
- Functional breakdown (fonction 7 "Environnement" in M57, fonction 8 in M14 for "aménagement et environnement") would need to be confirmed on data.ofgl.fr; small communes under M14 abridged may not report by function — treat as uncertain.

### Gaps
- Exact OFGL dataset name for functional presentation and its licence not verified (OFGL data are generally under Licence Ouverte — unverified).
- DGCL datasets not searched.

## Q3. Socio-economic context (population, income, economic activities, employment)

### Takeaway
INSEE **Filosofi 2021 carroyé 200 m** (published Feb 2026) is the latest fine-grid socio-economic layer; **Urssaf commune × APE** gives private employment and establishments by detailed sector (updated 29 May 2026); **SIRENE** gives establishment-level NAF, but the Etalab geolocated version was retired in April 2026 in favour of INSEE's own geolocated product.

### Cited Findings
**D8 — Revenus, pauvreté et niveau de vie en 2021 – Données carroyées (Filosofi)** (producer: INSEE)
- URL: https://www.insee.fr/fr/statistiques/8735243 (published 16 Feb 2026); 200 m file: https://www.insee.fr/fr/statistiques/8735162 — [INSEE](https://www.insee.fr/fr/statistiques/8735243); [INSEE 200m](https://www.insee.fr/fr/statistiques/8735162)
- 200 m grid, 34 variables (age structure, households, housing, 2021 income); squares with <11 fiscal households are imputed (flag i_est_200) — [INSEE](https://www.insee.fr/fr/statistiques/8735162)
- Parquet copy (2019 + 2021, EPSG:3035) on data.gouv.fr — [data.gouv.fr](https://www.data.gouv.fr/datasets/66fd2924ca43b044d55a7b74)
- Previous vintages 2015/2017/2019 also available — [INSEE 2019](https://www.insee.fr/fr/statistiques/7655515)
- Licence: INSEE open licence (Licence Ouverte; not re-verified). Normandy: metropolitan France covered.
- Use: Problem 1 (population exposed / beneficiaries of restoration, nature access deprivation, environmental justice: low-income areas lacking green space); Problem 2 (population pressure).

**D9 — Nombre d'établissements employeurs et effectifs salariés du secteur privé, par commune × APE (au 31/12 depuis 2006)** (producer: Urssaf)
- URL: https://www.data.gouv.fr/datasets/nombre-detablissements-employeurs-et-effectifs-salaries-du-secteur-prive-par-commune-x-ape-au-31-12-depuis-2006 (also on open.urssaf.fr) — [data.gouv.fr](https://www.data.gouv.fr/datasets/nombre-detablissements-employeurs-et-effectifs-salaries-du-secteur-prive-par-commune-x-ape-au-31-12-depuis-2006)
- Formats CSV + JSON; last update 29 May 2026; licence ODbL — [data.gouv.fr](https://www.data.gouv.fr/datasets/nombre-detablissements-employeurs-et-effectifs-salaries-du-secteur-prive-par-commune-x-ape-au-31-12-depuis-2006)
- Updated ~150 days after year-end; private employers under general scheme (agriculture excluded, MSA scope); apprentices included since June 2023 release; DSN source since 2021 — [search snippet of dataset description](https://www.data.gouv.fr/datasets/5efd242c72595ba1a48628f2)
- Unit: commune × APE (732 codes), annual series. Normandy: included.
- Use: "cross environment with economic/industrial activity" — employment in extraction, chemicals, tourism (hotels/restaurants), agri-food per commune; pressure indicators (Problem 2) and socio-economic stakes of restoration (Problem 1).

**D10 — SIRENE (base des entreprises et établissements)** (producer: INSEE)
- Monthly stock file + daily updates on data.gouv.fr (CSV, >8 GB uncompressed); INSEE API requires a (free) account; Etalab geolocated SIRENE retired April 2026 in favour of INSEE's — [data.gouv.fr](https://www.data.gouv.fr/datasets/62bc4b958cdb4ce3c2d86064); INSEE geolocation presented to CNIG Jan 2026 — [CNIG](https://cnig.gouv.fr/IMG/pdf/presentation_cnig_28_janvier.pdf)
- Contains personal data for sole proprietors (CNIL rules; "diffusion partielle" records) — [data.gouv.fr](https://www.data.gouv.fr/datasets/62bc4b958cdb4ce3c2d86064)
- Use: point-level mapping of activities by NAF (quarries 08.xx, campsites 55.30, ICPE-type industry) next to sensitive habitats. Aggregate before display to avoid personal data.

### Inferences
- For a datathon, D9 (commune aggregates) is easier and personal-data-free; use D10 only for specific sectors aggregated to grid/commune.

### Gaps (not verified this session; well-known national INSEE products worth adding)
- Populations légales communales (INSEE, annual, commune) — not checked.
- BPE – Base permanente des équipements (INSEE, geolocated equipment incl. tourism/sport) — not checked.
- INSEE tourism accommodation capacity by commune (hotels, campsites) — not checked.
- INSEE Flores (employment incl. public sector by commune × sector) — not checked.

## Q4. Territorial planning context (urbanism zoning, ZAN, programmes)

### Takeaway
PLU/PLUi/carte communale zoning is accessible nationally via the **API Carto – module GPU** (IGN, free, open, GeoJSON); "Petites villes de demain" lists exist mostly as regional/departmental extracts (incl. an Orne dataset), and the programme was designed to end March 2026 — flag as possibly outdated.

### Cited Findings
**D11 — API Carto – module Géoportail de l'Urbanisme (GPU)** (producer: IGN / DGALN)
- URL: https://www.data.gouv.fr/dataservices/api-carto-module-geoportail-de-lurbanisme-gpu — REST, JSON/GeoJSON WGS84, query by point/polygon intersection and attributes; covers PLU, POS, carte communale, PSMV zoning, prescriptions, SUP; open licence, free — [data.gouv.fr](https://www.data.gouv.fr/dataservices/api-carto-module-geoportail-de-lurbanisme-gpu)
- Bulk extracts exist as third-party regional datasets ("Zonages des documents d'urbanisme – GPU") — [data.gouv.fr](https://www.data.gouv.fr/datasets/zonages-des-documents-durbanisme-gpu/reuses_and_dataservices)
- Normandy: coverage depends on communes having uploaded their document to the GPU (partial coverage likely for older POS/RNU communes).
- Use: Problem 1 feasibility (restoration candidates on N/A zones vs. AU zones under urbanisation pressure; EBC/prescriptions).

**D12 — Petites villes de demain (ANCT)**
- >1,580 communes selected nationally; ANCT published lists by region/department — [Banque des Territoires](https://www.banquedesterritoires.fr/petites-villes-de-demain-la-liste-des-communes-retenues-est-publiee)
- data.gouv.fr holds regional/departmental extracts, e.g. "Petites villes de demain (PVD) dans l'Orne", which states the programme was designed to run until March 2026 — [data.gouv.fr Orne](https://www.data.gouv.fr/datasets/petites-villes-de-demain-pvd-dans-lorne)
- No single national data.gouv.fr dataset confirmed in this search.
- Use: Problem 2/territorial development (target communes with existing revitalisation engineering for "renaturation de centre-bourg" actions).

### Inferences
- ANCT also maintains national programme lists (PVD, Action cœur de ville) on its own open-data space; likely the source for a national file — unverified.

### Gaps
- ZAN data (Cerema "consommation d'espaces NAF" from fichiers fonciers, MonDiagnosticArtificialisation, OCS GE) not verified here — likely covered by another research thread on land use.
- SCoT perimeters: GPU covers SCoT documents but not verified.
- Action cœur de ville list not verified.
- Post-March-2026 status of PVD not confirmed.

## Q5. Citizen perception / participation

### Takeaway
No open microdata for a national biodiversity-perception barometer was found: OFB runs a barometer (BVA 2022, Harris Interactive 2024, ~2,000 respondents, national sample) published only as press releases/PDF reports, with no regional (Normandy) breakdown usable at local scale.

### Cited Findings
- OFB barometer 2022 (BVA, 2,000 people): >8 in 10 French feel concerned by biodiversity — [OFB press release](https://www.ofb.gouv.fr/sites/default/files/Fichiers/Presse/CP_Barometre-biodiversite.pdf)
- 2024 wave by Harris Interactive for OFB: online survey 27 Mar–2 Apr 2024, n=2,058, 15+ y.o. — [Harris/Toluna report](https://tolunacorporate.com/wp-content/uploads/2025/05/Rapport-Harris-Les-Francais-et-la-biodiversite-OFB-vague-2-Rapport-principal-sans-responsables.pdf)
- CREDOC survey for the future biodiversity agency dates from 2015 — [CREDOC](https://www.credoc.fr/download/pdf/Sou/Agence_Biodiversite_mai2015.pdf)

### Inferences
- For local participation indicators, participatory-science observation counts (e.g. Vigie-Nature / INPN data, out of this thread's scope) or ABC/TEN engagement flags (D3, D4) are better proxies than surveys.

### Gaps
- No open microdata; no wave after 2024 confirmed; national "Sentinelles"-type reporting datasets not searched.

## Summary table (for the report writer)

| # | Dataset | Producer | Access | Format | Unit | Coverage / update | Licence | Normandy | Problem |
|---|---|---|---|---|---|---|---|---|---|
| D1 | Fonds Vert – projets subventionnés | MTE | data.gouv.fr | CSV/XLSX | project × beneficiary, code commune | 2023–2025; upd. 28 Jul 2026 | Etalab 2.0 | Yes | 2 (+1) |
| D2 | Sites référencés dans Cartofriches | Cerema | data.gouv.fr | (not verified) | site | possibly upd. Jul 2026; sample, heterogeneous | not verified | Yes (partial inventory) | 1 |
| D3 | Atlas de la biodiversité communale | OFB | data.gouv.fr → abc.naturefrance.fr | links/download | project/commune | page upd. 8 Oct 2026 | CC-BY | Yes | 2 (+1) |
| D4 | Territoires engagés pour la nature | OFB | ofb.gouv.fr listing | web only | collectivity | ongoing | not open data | Yes | 2 |
| D5 | LIFE Public Database | EU CINEA | webgate.ec.europa.eu/life | export | project | 1992–present, daily | EC (unverified) | Yes | 2 |
| D6 | Aides-territoires API | ANCT | aides-territoires.beta.gouv.fr/api | JSON | aid scheme | live; v1.8.1 | Licence Ouverte 2.0 | Yes | 1 (feasibility) — ACCOUNT REQUIRED |
| D7 | Comptes des collectivités | OFGL/DGFiP | data.ofgl.fr | CSV/API | collectivity | 2024 definitive; annual summer | (unverified) | Yes | 2 |
| D8 | Filosofi 2021 carroyé | INSEE | insee.fr/8735162 | CSV/GPKG; parquet copy | 200 m grid | 2021; publ. Feb 2026 | Licence Ouverte | Yes | 1, 2 |
| D9 | Établissements & effectifs commune × APE | Urssaf | data.gouv.fr / open.urssaf.fr | CSV/JSON | commune × APE, annual | 2006–(likely 2025); upd. 29 May 2026 | ODbL | Yes (excl. agriculture) | 2 (+1) |
| D10 | SIRENE stock (+ INSEE geoloc) | INSEE | data.gouv.fr | CSV/Parquet | establishment | monthly | Licence Ouverte (personal data caveats) | Yes | 2 |
| D11 | API Carto – module GPU | IGN | apicarto.ign.fr via data.gouv.fr | GeoJSON | zone polygon | live | open | Yes (partial: uploaded docs only) | 1 |
| D12 | Petites villes de demain | ANCT | data.gouv.fr (dept extracts) | CSV | commune | programme to Mar 2026 — possibly outdated | (varies) | Yes (Orne extract found) | 2 |
