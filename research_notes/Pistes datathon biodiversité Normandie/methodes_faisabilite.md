# Pistes datathon biodiversité Normandie: methods, tooling, pitfalls and feasibility (pistes A–N), plus a sober web architecture

Scope: Datathon Normandie 2026 (deliverables due 12 Nov 2026 at noon, teams of 2–5, open data only). Notes are current as of 17 Oct 2026. Data availability comes from our own data inventory and was not re-checked. Sections 1–7 cover the cross-cutting key questions. Section 8 holds the per-piste cards (method and tooling, risks, MVP, effort, feasibility). "pd" means person-days.

## 1. Multi-criteria prioritisation: transparent index, MCDA or Zonation/prioritizr, and adjustable weights

### In short
For a 3.5-week MVP scored on feasibility and sobriety, the best trade-off is a transparent index built on percentile-normalised criteria: a weighted sum, or stakes × degradation × opportunity. Give it presets and sliders, and recompute the colours entirely in the browser with MapLibre expressions. Zonation 5 and prioritizr are credible "bonus" layers (complementarity, budget portfolios), but they are harder to explain and to validate. Whichever method is chosen, the composite-indicator discipline from the OECD/JRC handbook is what protects credibility: check correlations, justify the normalisation, state what the weights mean, and run a sensitivity analysis.

### Sources
- The OECD/JRC *Handbook on Constructing Composite Indicators* is the reference guide for building composites. It sets out the steps: multivariate analysis before aggregation, treatment of missing data, normalisation of heterogeneous indicators to a common unit, alternative weighting and aggregation methods, and robustness testing by uncertainty and sensitivity analysis — [OECD handbook page](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html); [JRC handbook PDF](https://knowledge4policy.ec.europa.eu/sites/default/files/jrc47008_handbook_final.pdf); [JRC working paper EUR 21834](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC32434/EUR%2021834%20EN.pdf)
- Weighting methods fall into two families. Statistical methods include principal components and Benefit-of-the-Doubt. Participatory methods include budget allocation and AHP — [secondary summary of the Handbook](https://ictlogy.net/bibliography/reports/projects.php?idp=2308)
- Munda & Nardo (JRC) argue there is a theoretical inconsistency between what weights mean in composite construction and the meaning standard practice gives them — [JRC31473](https://publications.jrc.ec.europa.eu/repository/handle/JRC31473)
- AHP: the usual rule of thumb is that the pairwise-comparison consistency ratio (CR) should be below 0.1 — [PyLUSAT documentation/paper](https://arxiv.org/pdf/2107.01674). A sensitivity analysis is needed to test how robust GIS-MCDM outputs are to weight changes. Stakeholders often cannot reach consensus on weights — [Chen et al., MODSIM 2009](https://www.mssanz.org.au/modsim09/I2/chen_y.pdf)
- prioritizr supports the Gurobi, IBM CPLEX, CBC, HiGHS, Rsymphony and lpsymphony solvers, and picks the best one installed. Preliminary benchmarks found CBC the fastest open-source solver. Gurobi is by far the fastest but is commercial (academic licences are free) — [prioritizr solvers doc](https://search.r-project.org/CRAN/refmans/prioritizr/html/solvers.html); [solver benchmarks vignette](https://mirror.linux.duke.edu/pub/cran/web/packages/prioritizr/vignettes/solver_benchmarks.html); [add_highs_solver](https://rdrr.io/cran/prioritizr/man/add_highs_solver.html)
- Zonation 5 offers the marginal-loss rules CAZ1, CAZ2 (the default in the ZonationR interface), ABF, CAZMAX, LOAD and RAND. It runs from the command line (e.g. `--mode=ABF`). The methods reference is Moilanen et al. 2022 (*Methods in Ecology and Evolution*) — [ZonationR manual](https://thiago-cav.r-universe.dev/ZonationR/doc/manual.html); [CSC Zonation docs](https://docs.csc.fi/apps/zonation/)
- CAZ cell value is the maximum across features, which emphasises rarity. ABF sums across features, which emphasises richness. The rank priority map is not a final product on its own — [Lehtomäki, "Tools for spatial conservation prioritization" slides](https://www.slideshare.net/jlehtoma/tools-for-spatial-conservation-prioritization)
- A Zonation 5 output ranks each pixel from 0 to 1 (Midwest Conservation Blueprint) — [ScienceBase record](https://sciencebase.gov/catalog/item/download/64e7a84bd34eeb681137f585.json). The Southeast Conservation Blueprint 2024 moved to Zonation 5 — [SECAS](https://secassoutheast.org/2024/06/26/Balancing-priorities-across-subregions-in-Blueprint-2024.html)
- French public-sector precedent for a transparent overlay: Cerema built a geomatic method that ranks artificialised urban spaces for renaturation. It crosses an "Enjeux" component (heat islands, biodiversity, lack of green space, flooding) with a second component — [Cerema](https://www.cerema.fr/fr/print/pdf/node/15052)
- MapLibre style-spec expressions include the math operators `+`, `*`, `-`, `/`, `%`, `^`, `min`, `max`, `round`, `abs` and others, which can take inputs from `get`. Data expressions are allowed in filters and "for most paint and layout properties". `feature-state` expressions are allowed only on paint properties. If a property value has the wrong type, the property's default value is used — [MapLibre style spec, expressions](https://maplibre.org/maplibre-style-spec/expressions/)

### Our reading
- **Recommended default model ("explainable first"):**
  - Use three sub-indices: Enjeux/Stakes (biodiversity value), Dégradation/Pressure, and Opportunité/Feasibility. Each is the mean of 2–4 criteria.
  - Normalise each criterion to a 0–100 percentile rank. Ranks are robust to outliers such as land-take hotspots and are easy to explain.
  - The headline score is a weighted sum (simple to drive with sliders). Also offer an "S × D × O" (multiplicative) preset, which limits compensation: a cell must score on all three axes to rank high.
- **Normalisation choice:**
  - Percentile ranks are the default.
  - Use log + min–max for strongly skewed quantities when the magnitude matters.
  - Use "distance to target" normalisation for indicators that have a policy target, such as the ZAN envelope or Pacte haie km.
  - Report in the methods page how the top-decile cells change under a second normalisation.
- **Double counting:** compute the correlation matrix of the criteria. Drop or merge pairs with |ρ| > ~0.7 (for example land take vs population density, or arable share vs pesticide purchases).
- **Missing data:** "no data" is not 0. Example: CarHab is absent in Eure and Orne. Either drop the criterion region-wide, or compute a partial score with renormalised weights, hatch those cells, and say so. Renormalising weights is itself an implicit imputation.
- **Weights and the meaning of weights:** in a linear sum, weights are trade-off rates, not "importance" (Munda & Nardo's point). Show this in the UI with a sentence such as "1 point of X compensates 1 point of Y".
  - Avoid full AHP matrices in the UI. If AHP is used, derive one weight set offline (in a team or stakeholder workshop), publish the CR, and keep the sliders for exploration.
- **Robustness layer (strong jury argument):** offline, draw ~1,000 random weight vectors (Dirichlet), recompute, and map the share of draws in which each unit is in the top 10%. The result is a "robust priority" layer that answers "is this priority an artefact of my weights?". Cost: a few seconds in DuckDB or numpy for ~30k cells.
- **prioritizr as a bonus:**
  - Setup: ~30,000 1-km planning units (Normandy ≈ 30,000 km²), 10–30 features (HIC habitats, species groups, wetlands, hedge density) and a cost (e.g. land-take pressure).
  - Run a minimum-set problem with 30% representation targets, using CBC or HiGHS. It will probably solve in seconds to minutes; test this, since no benchmark at this size was found.
  - Output: a binary "portfolio" map plus selection frequency over repeated solves.
  - Zonation 5 gives a rank map but adds a separate install and learning curve. Marxan was not researched.
- **Web UI pattern (no server):**
  - Store integer sub-scores (0–100) as attributes in the vector tiles.
  - On slider input, rebuild an expression such as `["interpolate",["linear"],["+",["*",w1,["get","c1"]],["*",w2,["get","c2"]],…],0,"#f7f7f7",100,"#00441b"]` and call `map.setPaintProperty(...)`. Confirm in the SDK support table that `fill-color` accepts data expressions.
  - Keep the weights in the URL hash so a configuration can be shared.
  - Add presets ("Biodiversité d'abord", "Eau", "Sobriété foncière").
  - Add an "explain this unit" popup with a stacked bar of contributions.
  - For the ranking table, compute in JS from a compact JSON/Parquet table: 30k rows × 10 small ints is roughly 1–2 MB uncompressed and much less gzipped (estimate).
- **Pitch line:** "transparent > optimal". This fits the RGESN requirement to justify any algorithmic choice (§7).

### Open points
- No runtime benchmark was found for prioritizr with CBC or HiGHS on ~30k planning units; test before promising it.
- Marxan was not researched. Zonation 5 install and licensing on Windows were not checked.
- No source compares weighted-overlay outputs with complementarity-based outputs in a French regional TVB context.

## 2. Connectivity and fragmentation: tools, hedge network metrics and computing cost

### In short
Wall-to-wall density and length metrics on a 1 km grid are cheap, and they follow the official DSB (Dispositif national de suivi des bocages) logic. They are feasible for 2.7 M segments with DuckDB spatial (v1.3 or later) or GeoPandas on a laptop. Graph and least-cost connectivity (Graphab) and circuit theory (Omniscape) should be limited to pilot landscapes or coarse rasters. meff is the standard fragmentation indicator for barrier-type fragmentation (roads, urban areas), not a hedgerow metric as such. The standard simplifications are gridding at 1 km, sampling (survey circles or stratified 1 km² cells), pilot areas, coarser rasters, and block-based solving.

### Sources
- **Graphab, what it is:**
  - Open source (GPL), developed at ThéMA (Univ. Franche-Comté/CNRS) by G. Vuidel and J.-C. Foltête.
  - Graphs link patches by Euclidean distance or least-cost paths.
  - Metrics are computed at global, component and local levels, and patch metrics can be extrapolated with a distance function to compare with species observations — [Foltête et al., HAL](https://hal.archives-ouvertes.fr/hal-00736536)
  - Metrics include PC, IIC, F, IF, Dg, CCe, CF and dPC. The R package graph4lg interfaces with Graphab — [graph4lg vignette](https://psavary3.r-universe.dev/graph4lg/doc/landscape_graph_3.html)
- **Graphab, inputs and versions:**
  - Input is a raster with discrete codes. Contiguous habitat cells (8-neighbourhood) form patches above an optional minimum area — [Graphab 2.2 manual](https://thema.univ-fcomte.fr/productions/software/graphab/download/manual-2.2-en.pdf)
  - Graphab 3.0 is the latest version. It supports multiple habitat types in one project, older projects are incompatible, it needs Java 11+, and it is free (GPL; citation required). The home page says nothing about performance or memory limits — [Graphab home](https://thema.umlp.fr/productions/software/graphab/en/home.html)
  - The French 3.0 manual is dated 02/12/2024 — [manual 3.0 FR](https://thema.univ-fcomte.fr/productions/software/graphab/download/manual-3.0-fr.pdf)
  - Graphab is used in French TVB practice, for example to model grassland, woodland and wetland sub-networks in a Grand Est study — [nature-en-ville](https://www.nature-en-ville.com/print/pdf/node/1719)
- **Omniscape:**
  - It applies Circuitscape iteratively in a moving window: one solve per target pixel, with the current maps summed. It "evaluates connectivity between every possible pair of pixels" — [Omniscape.jl, How it works](https://docs.circuitscape.org/Omniscape.jl/latest/algorithm/)
  - `block_size` > 1 "can significantly reduce compute times": in the docs' example, solves drop from 81 to 9 with `block_size = 3`, and total injected current is preserved.
  - It runs in parallel by default (Julia threads).
  - `precision = single` reduces memory use but is less accurate — [Omniscape.jl usage](https://docs.circuitscape.org/Omniscape.jl/latest/usage/)
  - One example Omniscape run (radius 10) took ~490 s, raster size unstated — [enerscape vignette](https://archive.linux.duke.edu/cran/web/packages/enerscape/vignettes/enerscape.html)
- **meff (effective mesh size):**
  - Defined by Jaeger (2000), it expresses the probability that two randomly chosen points are connected. Smaller values mean more fragmentation.
  - The cross-boundary connections (CBC) procedure accounts for unfragmented areas that extend beyond the reporting unit.
  - For flying species and good dispersers, man-made structures may not be barriers — [EEA indicator assessment](https://www.eea.europa.eu/data-and-maps/indicators/mobility-and-urbanisation-pressure-on-ecosystems-2/assessment); [EEA/FOEN "Landscape fragmentation in Europe"](https://www.ilpoe.uni-stuttgart.de/files/Landscape_Fragmentation_in_Europe.pdf)
- **DSB (OFB + IGN, since 2017):**
  - Phase 1 produced a reference hedge map from BD TOPO (2004–2015) and RPG (2011–2014). On a 1 km grid (INPN referential) it computes hedge density (m/ha, total hedge length / area), the number of hedge–forest connections, and closed-forest edge length.
  - A "coherence index" complements density by describing hedge functionality through topology.
  - Phase 3 uses field surveys on 1 km² cells stratified by bocage density. Surveys in Normandy run in 2025–2026 — [OFB DSB (Pays de la Loire page)](https://ofb.gouv.fr/pays-de-la-loire/dispositif-nationale-de-suivi-des-bocages-dsb); [OFB news, DSB field surveys in Normandy 2025–2026](https://ofb.gouv.fr/actualites/dispositif-national-de-suivi-des-bocages-des-releves-de-terrain-en-normandie-en-2025-et); [OFB "Réseaux de haies et biodiversité"](https://trameverteetbleue.fr/sites/default/files/references_bibliographiques/34997_ofb_rencontres_reseaux_de_haies_et_biodiversite_web.pdf); [IGN haies 2021](https://www.ign.fr/publications-de-l-ign/institut/evenements/evenement-haies_20211208.pdf)
- **Pacte en faveur de la haie (Sept 2023):** a net gain of 50,000 km of hedges by 2030, with 24 measures including an IGN-run observatory — [Banque des Territoires](https://www.banquedesterritoires.fr/le-gouvernement-presente-un-pacte-pour-planter-50000-km-de-nouvelles-haies-dici-2030)
  - CGAAER (April 2023) figures as relayed in parliamentary documents: ~23,500 km/yr lost in the recent period vs ~11,500 km/yr in 2006–2014, and plantations of only ~3,000 km/yr. A net target of 7,000–8,000 km/yr is mentioned — [AN written question QE6686](https://questions.assemblee-nationale.fr/dyn/17/questions/QANR5L17QE6686.pdf); [AN amendment CE2458](https://www.assemblee-nationale.fr/dyn/16/amendements/2436/CION-ECO/CE2458.pdf). The figures vary by period and source.
- **DuckDB spatial joins:**
  - From v1.3.0, the `SPATIAL_JOIN` operator builds an in-memory R-tree on the fly, like a hash join.
  - Benchmark: 58,033,724 points × 310 polygons took 1,799.6 s (nested loop), 107.6 s (piecewise merge) and 28.7 s (spatial join) on an M3 Pro laptop with 36 GB RAM.
  - Limits: the right side is buffered in memory, and the join condition can only be a single spatial predicate — [DuckDB blog, spatial joins](https://duckdb.org/2025/08/08/spatial-joins)

### Our reading
- **2.7 M hedges on a laptop is feasible for density metrics:**
  - Join the hedge segments to ~30k 1-km cells; each segment touches 1–2 cells. Clip with `ST_Intersection` + `ST_Length` (DuckDB ≥1.3), or use GeoPandas/shapely 2 vectorised overlay. Process by department, in Lambert-93 (EPSG:2154), with GeoParquet as the intermediate format.
  - Expected runtime is minutes to tens of minutes on 16 GB RAM. This is an estimate extrapolated from the point-in-polygon benchmark; test on one department first.
  - Cheaper alternative: assign each segment's full length to the cell that contains its midpoint, with no clipping. At 1 km the error is small because most segments are far shorter than 1 km.
- **Network metrics:**
  - Snap endpoints with a 1–5 m tolerance and build an undirected graph. igraph handles 2.7 M edges comfortably; networkx is memory-hungry at this size.
  - Per-cell or per-commune metrics: number of components, share of length in the largest component, junction density (degree ≥ 3), and hedge–forest connections (DSB-like, using OCS GE woodland).
  - Planting candidates (useful for piste L): pairs of endpoints belonging to different components, ≤ 20–50 m apart.
- **"Maille bocagère" metrics:**
  - Polygonise hedges + roads + watercourses into enclosed field meshes, then compute mean mesh area or the meff of open-field meshes.
  - This is much heavier (polygonize on millions of lines), and roads and hydrography are not in the established inventory. Restrict it to sample communes or pilot areas.
- **Graphab / Omniscape at regional scale:**
  - Normandy (~30,000 km²) at 10 m is ~300 M pixels, which is unrealistic for Omniscape within the time box. Graphab at 25–50 m with a minimum patch area may run.
  - The bottleneck is parameterisation: resistance values per land-cover class and dispersal distances per species group need expert justification.
  - Recommendation: run 1–3 pilot landscapes (~20 × 20 km, e.g. a dense bocage area vs an open-field area), use `block_size` and coarser resolution in Omniscape, and in Graphab use delta metrics (dPC) for candidate plantings.
- **meff use:** use it for "fragmentation by transport and urban areas" per commune or EPCI (with the CBC variant) as a negative-interaction indicator for P2. It needs a roads layer (not in the established inventory) and OCS GE artificial classes.
- **Communication:** a mapped line is not a functional hedge (height, gaps and management are unknown). That is why DSB phase 3 runs field surveys. Say this explicitly.

### Open points
- No published memory or performance limits were found for Graphab 3.0 on large regions. No regional-scale Omniscape benchmark was found.
- No benchmark was found for line–polygon overlay of millions of lines in DuckDB or GeoPandas (only point-in-polygon).
- The exact formula of the DSB "coherence index" was not retrieved.
- The 2024 Normandy hedge-linear study PDF (DREAL/ANBDD, `lineaireshaies-normandie-2024_anbdd.pdf`) returned HTTP 403 and could not be read.

## 3. Prioritising barrier removal

### In short
The realistic MVP is a simple, explainable proxy: the river length reconnected if an obstacle is removed (leave-one-out ΔDCI). Weight it by drop-height class (as a passability proxy), relevance for migratory fish and water-body status. The R package riverconn computes DCI and ΔDCI directly. Full OptiPass-style budget optimisation needs passability and cost data that are largely missing. French practice indicators (taux d'étagement, taux de fractionnement) are easy to compute where drop heights are known, and they speak the regulators' language. The EU Nature Restoration Regulation's target of 25,000 km of free-flowing rivers is the policy hook.

### Sources
- **riverconn:**
  - Provides DCI, PCI, RFI, PC and IIC.
  - Its dCCI measures how much the network index changes when a barrier is removed or its passability changes. Leave-one-out is the default and "add-one" is the alternative, via `d_index_calculation()`.
  - Built on igraph and available on CRAN — [riverconn tutorial](https://www.stats.bris.ac.uk/R/web/packages/riverconn/vignettes/Tutorial.html); [riverconn reference manual](https://cran.nics.utk.edu/cran/web/packages/riverconn/refman/riverconn.html)
  - In the Ebro case study, prioritisations "vary considerably" with organism class and dispersal traits — [Baldan et al. 2022, Environmental Modelling & Software](https://ricerca.ogs.it/handle/20.500.14083/26292)
- **OptiPass:**
  - Combines barrier passability (upstream and downstream), mitigation cost and potential habitat gain for one or more target species.
  - Uses a mixed-integer linear programme with "probability chain" linearisation. A batch mode runs over ranges of budgets and species weights and can force barriers in or out — [Oregon State University decision-support page](https://fwcs.oregonstate.edu/fwcs/decision-support-and-prioritization-frameworks-river-restoration-and-barrier-removal); [O'Hanley 2011 overview](https://people.wou.edu/~taylors/g407/restoration/OHanley_2011_barrier_removal_overview.pdf)
- **Taux d'étagement (%):** (sum of artificial drop heights / natural elevation drop) × 100. It is not computed on Strahler ranks 1–2. Provisional classes run from 0–20% (very good) to 80–100% (bad) — [SDAGE Loire-Bretagne fiche](https://www.centre-val-de-loire.developpement-durable.gouv.fr/IMG/pdf/sdage_fiche7_1c2_1d4_etagement_fractionnement.pdf); [ONEMA synthesis note](https://www.migrateurs-loire.fr/telechargement/documentation/guides/ONEMA_Note_synthese_taux_d_etagement_cle12f751.pdf)
- **Taux de fractionnement:** (sum of drop heights / reach length) × 1000, in m/km, using low-flow heights. A 0.4 m/km threshold has been used to flag degraded continuity. Obstacles with a fish pass judged efficient are excluded from fractionnement (not from étagement). Denominators differ between documents (reach length, hydrographic length, main drain) — [Centre-Val de Loire method](https://www.biodiversite-centrevaldeloire.fr/sites/default/files/content/ressources/pdf/indicateurs/m%C3%A9thodo%20indic%20CE.pdf); [SAGE Vilaine report](https://www.observatoire-poissons-migrateurs-bretagne.fr/images/pdf/Bassin-versant/2.État_davancement_du_rétablissement_de_la_continuité_écologique_et_de_la_réduction_du_taux_détagement_sur_le_territoire_du_SAGE_Vilaine.pdf)
- **ROE:** drop height is a complementary attribute, given as a low-flow class from <0.5 m to ≥10 m, with an "Indéterminée" option. The ROE is neither a business database on structures nor, for now, an exhaustive census — [ROE user manual](https://www.eaufrance.fr/sites/default/files/2019-04/roe-referentiel-des-obstacles-a-l-ecoulement-manuel-d-utilsation.pdf)
- **ICE:** assesses each obstacle's passability for fish with an upstream score between 0 and 1 and identifies the limiting parameters. ICE data are linked to the ROE and stored in the ICE bank. The protocol is not legally opposable — [ICE field guide](https://www.trameverteetbleue.fr/sites/default/files/references_bibliographiques/guide-terrainice.pdf); [OFB ICE document](https://ofb.gouv.fr/sites/ofb-gouv-fr/files/import/pro/pdf/documentation/CPA2019_ICE%20DOM_Partie%20C.pdf)
- **EU Nature Restoration Regulation (2024/1991):**
  - Barriers must be removed so that at least 25,000 km of rivers are free-flowing by 2030.
  - Draft National Restoration Plans were due by 1 Sept 2026, after which the Commission has six months to comment.
  - Plans run to 2050 and must include financing needs and how they interact with the CAP strategic plans — [Garrigues legal summary](https://www.garrigues.com/en_GB/new/eu-bolsters-nature-restoration-here-new-legislative-framework-2030-and-2050); [European Commission NRR page](https://environment.ec.europa.eu/topics/nature-and-biodiversity/nature-restoration-regulation_en); [Dam Removal Europe](https://damremoval.eu/call-to-action-get-your-barrier-removal-projects-into-national-restoration-plans/)

### Our reading
- **MVP algorithm (Python + igraph, or R + riverconn):**
  1. Get a topologically correct hydrographic network. **Dependency:** none is listed in our data inventory. BD TOPAGE or Carthage would be needed.
  2. Snap ROE points to the nearest reach within ~25–50 m and split the reaches.
  3. For each obstacle, compute the functional river length between it and the next obstacles upstream, plus the downstream path to the sea for diadromous species. This gives "km reconnected if removed", a ΔDCI proxy.
  4. Weight by: height class (a proxy for passability when ICE is absent), distance to the sea and migratory-fish presence (Hub'Eau fish), WFD status of the water body, and regulatory listing (if available).
  5. Rank, and offer a greedy "remove the top N" scenario that returns cumulative km.
- **Indicators:** show taux d'étagement per water body only where heights are known. Show the % of obstacles with "Indéterminée" height as a data-quality badge.
- **Framing:** removing obstacles touches heritage, water rights and social acceptability (e.g. mills). ROE statuses (existing, removed, in project) may be outdated. Present the output as a "dialogue list", not a demolition list.
- **Why not OptiPass:** without cost data and species-specific passability, a budget optimisation would be fake precision. Say so and show the proxy ranking instead.

### Open points
- The share of Normandy ROE obstacles with known drop heights or ICE scores was not checked (data profiling was out of scope).
- No French OptiPass-like tool and no open obstacle-removal cost data were identified.
- Whether France submitted its draft National Restoration Plan by 1 Sept 2026, and what it contains, was not found.

## 4. Restorable wetlands and protection gaps

### In short
Both questions are overlay problems. (Potential wetlands) ∩ (crops or artificial land) gives restoration candidates. (Habitat or species layers) ∩ (protected areas), compared with a representation target, gives the protection gaps. The main risk is not computation. It is over-interpreting probabilistic layers (the potential-wetland model at 1:100,000; CarHab is predictive) and observer-biased species data.

### Sources
- **MPH (INRA/Agrocampus Ouest, 2014):**
  - Models envelopes that, on geomorphological and climatic criteria, are likely to contain wetlands as defined by the arrêté of 24 June 2008. Scale 1:100,000, three probability classes (assez forte, forte, très forte).
  - It does **not** account for drainage or infilling, land use (crops, urbanisation), or local soil and hydrological processes — [Notice MPH](https://geosas.fr/metadata/pdf/Notice_MPH_France-1.pdf); [Pôle-relais lagunes](https://pole-lagunes.org/les-milieux-potentiellement-humides-de-france-modelises)
  - A parliamentary amendment argued that a restoration policy based on this map would mean acting on more than 25% of French territory — [AN amendment 1382](https://www.assemblee-nationale.fr/14/amendements/2064/AN/1382.pdf)
  - R&D on a newer national pre-localisation of wetlands began in January 2021 — [INPN document](https://inpn.mnhn.fr/docs-web/docs/download/416298)
- **Gap-analysis practice:** set a target per unit, overlay the protected areas, and list the shortfalls.
  - An EU study set per-habitat targets from European Red List threat status. It found 6 ecoregions and 101 habitat types below target, then simulated a cost-efficient expansion — [JYX, Natura 2000 representation](https://jyx.jyu.fi/handle/123456789/61751)
  - "Mind the gap!": Natura 2000 plus national protected areas leave 1 total-gap and 121 partial-gap terrestrial vertebrate species — [Gruber et al.](https://researchprofiles.canberra.edu.au/en/publications/mind-the-gap-how-well-does-natura-2000-cover-species-of-european-/)
- **SNAP 2030 (French protected-areas strategy):**
  - Targets at least 30% of the territory protected, including at least 10% under strong protection (art. L.110-4 Code de l'environnement). The 2020 baseline was 23.8% protected and 1.76% strongly protected — [DREAL Pays de la Loire SNAP presentation](https://www.pays-de-la-loire.developpement-durable.gouv.fr/IMG/pdf/20211217_snap.pdf); [SNAP mid-term evaluation synthesis](https://www.ecologie.gouv.fr/sites/default/files/documents/synthese_evaluation_intermediaire_SNAP.pdf)
  - PNR count toward the 30% — [Fédération des PNR](https://parcs-naturels-regionaux.fr/print/pdf/node/22650)
  - The President was reported as saying strong protection went "from 2 to 4%" — [Reporterre](https://reporterre.net/Les-aires-protegees-protegent-mal-la-biodiversite-selon-une-etude-scientifique)
- **CarHab:**
  - A national predictive habitat map at 1:25,000, combining machine learning with expert review by the botanical conservatories (CBN).
  - Three stages: a biotope map, a vegetation-physiognomy map, and a habitat map made by crossing the two. EUNIS and Habitat-Directive correspondences are set by expert judgement.
  - About 91% of mainland France and Corsica is mapped, across 88 departments, per the 2026 programme page — [CarHab programme page](https://www.ecologie.gouv.fr/politiques-publiques/carhab-programme-cartographie-nationale-predictive-habitats-naturels); [CarHab methodology](https://www.ecologie.gouv.fr/sites/default/files/documents/Me%CC%81thodologie_CarHab.pdf); [CBN Brest CarHab sheet](https://www.cbnbrest.fr:/geonetwork/srv/api/records/b4ab7106-5626-4a2c-b1ac-e3653eec479f/attachments/Fiche_carhab.pdf); [AMI CarHab](https://www.ecologie.gouv.fr/sites/default/files/AMI-utilisation_donnees_CarHab.pdf)
  - This national figure contrasts with the 3-of-5-department availability in our data inventory for Normandy. If Eure or Orne are published before 12 Nov, pistes H and B gain coverage.

### Our reading
- **Piste G overlay:**
  - Candidate = MPH (forte/très forte) ∩ (RPG arable crop codes, i.e. not permanent or temporary grassland) ∪ (MPH ∩ OCS GE artificial classes).
  - Restorability score = probability class + current use (temporary grassland > arable > artificial unsealed > sealed, which is very low) + adjacency to existing protected or inventoried sites + flood-zone overlap + parcel or cluster size.
  - Aggregate in ha per sub-basin or EPCI. "Low-regret" = very high probability + flood zone + arable + adjacent to a ZNIEFF or Natura 2000 site.
- **Guarding against over-interpretation:**
  - Display at 1 km or parcel-cluster level, labelled "pré-localisation probabiliste, non réglementaire".
  - Never name farms. The RPG is anonymous, but parcel-level targeting can still be socially sensitive.
  - Present results as "zones de dialogue".
- **Piste H overlay (3 CarHab departments only):**
  - Keep only HIC polygons above a probability threshold, and show sensitivity at two thresholds (e.g. ≥0.5 and ≥0.7).
  - For each HIC type compute total area, % in Natura 2000 and % under strong protection, and flag types below 30% or 10% (SNAP), or below type-specific targets.
  - Species: map heritage-species hotspots only in well-sampled cells (low ignorance score, §6) that lie outside protected areas. Output a ranked list of "unprotected hotspots".
- **CarHab pre-processing:** do it once. Use pyogrio/ogr2ogr to write GeoParquet with only the HIC code, probability and geometry. This should cut the 3.4 GB Manche archive drastically; budget 1–2 days for the three departments.
- **Optional:** use prioritizr to propose the smallest set of additional cells that reaches the targets (§1).

### Open points
- No published CarHab accuracy metrics and no quantified MPH over-estimation were found.
- Whether a newer national wetland pre-localisation has been released (2023–2026) was not verified (dataset searching was out of scope).

## 5. Indicator frameworks for human–nature interactions (P2)

### In short
Tag every indicator with DPSIR/PSR so it is explicitly a driver or pressure (negative interaction), a state, or a response (positive interaction or good practice). Document each indicator ONB-style: definition, source, scale, update frequency and limits. Normalise by the denominator that matches the mechanism: utilised agricultural area (UAA) for farm pressures, area for land take, km of river for obstacles, inhabitants for public spending. Prefer trends and distance-to-target over raw levels to "value good practices". Do not rely on one opaque composite.

### Sources
- DPSIR (Drivers–Pressures–State–Impact–Response) was developed by the EEA in 1999 from the OECD's Pressure–State–Response model. It provides a structure for presenting indicators that feed back to policy-makers — [EEA, Environmental indicators: typology and overview (TEC25)](https://www.eea.europa.eu/publications/TEC25/download); [DPSIR overview](https://en.wikipedia.org/wiki/DPSIR)
- **ONB (Observatoire national de la biodiversité):**
  - Coordinated by OFB with the SDES. It reports on the state and trends of biodiversity, the pressures and the responses.
  - Indicators draw on multiple data sources, are updated at regular intervals, and are produced "at the finest and most relevant scale possible", each with documentation on sources and methods.
  - Work is discussed collegially and independently evaluated by scientists — [ONB brochure 2023](https://www.ofb.gouv.fr/sites/default/files/Fichiers/Plaquettes%20et%20rapports%20instit/plaquette-onb-2023.pdf)
  - A 2025 FRB/OFB call requires new indicators to meet the ONB criteria and add value to the existing set (~119 indicators) — [FRB/OFB call](https://fundit.fr/fr/calls/appel-projets-frb-ofb-onbnouveaux-indicateurs-pour-lobservatoire-national-biodiversite-onb)
  - An indicator is a "spokesperson of reality, not reality itself" and must come with qualitative commentary on its limits — [FRB 2012–2013 critical analysis of ONB indicators](https://www.fondationbiodiversite.fr/wp-content/uploads/2019/05/FRB-Mission-indicateurs-ONB-rapport-2012-2013.pdf)
- **EFESE:** launched in 2012 as a science–policy–society interface. It is consistent with the EU MAES framework but explicitly includes ecosystem disservices, covers terrestrial and marine ecosystems of metropolitan France, and highlights the multiple values of biodiversity — [MTE, EFESE](https://www.ecologie.gouv.fr/levaluation-francaise-des-ecosystemes-et-des-services-ecosystemiques); [EFESE agricultural ecosystems summary](https://hal.inrae.fr/hal-02990793v1/file/efese-services-ecosystemiques-rendus-par-les-ecosystemes-agricoles-resume-francais-3.pdf)
- **COP régionales (ecological planning):**
  - Launched in September 2023 to produce regional action plans. The SGPE and CGDD are consolidating a national monitoring dashboard — [Banque des Territoires](https://www.banquedesterritoires.fr/planification-ecologique-une-circulaire-organise-le-deploiement-territorial); [COP Normandie document](https://www.prefectures-regions.gouv.fr/normandie/normandie/normandie/irecontenu/telechargement/112182/840566/file/2023%2012%2015_COP-regionales_Normandie_valide-1.pdf)
  - Biodiversity was mostly treated in a siloed "natural resources" group rather than as a cross-cutting issue — [Iddri 2024](https://iddri.org/sites/default/files/PDF/Publications/Catalogue%20Iddri/Propositions/202412-PB0624-planification%20ecologique.pdf)
  - The 2025 COP season was refocused on climate adaptation (PNACC), per a Prime Minister's instruction of April 2025 as reported in press summaries. The exact source page was not opened; likely [Banque des Territoires, "acte 2 des COP régionales"](https://www.banquedesterritoires.fr/territorialisation-de-la-planification-ecologique-les-modalites-de-lacte-2-des-cop-regionales-sont)
- Composite-index pitfalls (normalisation, the meaning of weights, robustness): see §1 — [OECD/JRC Handbook](https://www.oecd.org/en/publications/handbook-on-constructing-composite-indicators-methodology-and-user-guide_9789264043466-en.html); [Munda & Nardo](https://publications.jrc.ec.europa.eu/repository/handle/JRC31473)

### Our reading
- **Proposed P2 indicator grid (each tagged with DPSIR, unit, normalisation and scale):**
  - *Negative interactions (pressures):*
    - NAF consumption (Cerema; ha/yr per 1,000 ha)
    - Hedge-density loss (DREAL sample circles; m/ha/yr)
    - Permanent-grassland conversion (RPG; % of UAA)
    - Pesticide purchases (BNV-D; kg active substance per ha UAA, at EPCI or basin level only)
    - Water withdrawals (Hub'Eau; m³/yr per km² or per capita, by use)
    - Obstacle density or taux d'étagement (per km of river)
    - Dry-river frequency (ONDE; % of observations with flow interruption)
  - *State:*
    - WFD good-status share
    - Hydrobiology and fish indices
    - Hedge density
    - Grassland share
    - HIC habitat area (CarHab, 3 departments)
    - Effort-corrected species indicators
  - *Positive interactions (responses / good practices):*
    - Fonds vert biodiversity/renaturation € per capita and per ha (at EPCI level)
    - Protected and strongly protected area share
    - HVE farm share (aggregated)
    - Brownfield renaturation projects
    - Hedge planting and restored wetlands, if data exist
- **Valuing good practices fairly:**
  - Use progress against a territory's own baseline and distance to target (Pacte haie, ZAN, SNAP 30/10), not levels alone, so naturally rich territories are not the only ones rewarded.
  - Compare within peer groups (e.g. urban / peri-urban / bocage / open-field EPCI typology).
- **Small numbers:** suppress or flag values below thresholds (mirroring statistical secrecy) and use multi-year means.
- **One headline score (if the jury wants one):** show it as a secondary "synthèse" with a visible decomposition, never on its own.
- **Normalisation rule:**
  - Per area for land-based pressures.
  - Per UAA for agricultural ones.
  - Per inhabitant for spending.
  - Per km of river for continuity.
  - Ratios of sums (not means of ratios) when aggregating communes to EPCI.

### Open points
- The exact ONB indicator selection-criteria text was not retrieved.
- The Région's list of 68 COP indicators and its EPCI-level availability were not retrieved (out of scope here). This is critical for piste D.
- No EFESE indicator list was retrieved.

## 6. Data-quality pitfalls

### In short
The biggest credibility risks are:
1. Mapping observer effort instead of biodiversity (GBIF/OpenObs).
2. Mixing vintages and definitions (OCS GE vintage offsets; NAF consumption vs artificialisation).
3. Treating probabilistic layers as truth (CarHab, MPH).
4. Location semantics (a BNV-D purchase postcode is not the place of use; statistical secrecy).
5. Aggregation effects (MAUP; grid totals vs commune totals).

Each has a cheap, explainable mitigation, and showing those mitigations is itself a jury argument.

### Sources
- **Occurrence sampling bias:**
  - Records cluster near roads, cities, protected sites and research institutions — [Conservation (MDPI) 2026](https://www.mdpi.com/2673-7159/6/2/40)
  - Bias correction often requires filtering that reduces record numbers — [Ecological Indicators 2022 (HAL INRAE)](https://hal.inrae.fr/hal-03833433/document)
  - Road-biased sampling affects species differently — [Ecological Informatics 2026](https://cris.unibo.it/retrieve/f5b21ae2-5109-41ae-9b48-a3711ad5e987/ECOLINF_2026_Rocio.pdf)
  - The R package *sampbias* quantifies bias from gazetteers of cities, airports, roads and rivers, and recommends custom gazetteers at fine resolution — [sampbias vignette](https://azizka.r-universe.dev/sampbias/doc/Using_the_samp_bias_rpackage.pdf)
- **Ignorance scores (Ruete 2015):** a reference taxonomic group serves as the proxy for sampling effort. The score per cell runs from 0 (confidence) to 1 (ignorance); the "half-ignorance" form is G = O₀.₅ / (N + O₀.₅). It needs raw occurrences only — [Ruete 2015, Biodiversity Data Journal](https://pmc.ncbi.nlm.nih.gov/articles/PMC4549634/). It has been applied to GBIF data in the Caatinga — [GBIF data-use story](https://www.gbif.org/data-use/12bdsqxopJZQ1SQKBsJBTx/assessing-sampling-effort-in-the-caatinga-using-ignorance-scores)
- **MAUP:** summary values (totals, rates, proportions, densities) depend on the shape and scale of the units. MAUP is a special case of the ecological fallacy — [MAUP overview](https://en.wikipedia.org/wiki/Modifiable_areal_unit_problem); [PMC glossary](https://pmc.ncbi.nlm.nih.gov/articles/PMC7151983). Different aggregation methods can misrepresent indicator data — [Esri proceedings](https://proceedings.esri.com/library/userconf/proc07/papers/abstracts/a1026.html)
- **NAF consumption vs artificialisation:**
  - Cerema measures NAF consumption from the Fichiers fonciers (tax data). IGN measures artificialisation from OCS GE, which is to be used for artificialisation from 2031 — [ADEME ZAN seminar](https://experimentationsurbaines.ademe.fr/territoires-zero-artificialisation-nette/wp-content/uploads/sites/6/2025/07/202606SEMINAIREZANRISORANGIStableronde2.pdf)
  - The Fichiers fonciers cover only cadastral parcels, so part of the public domain (roads, water) is missing — [Fichiers fonciers definition note](https://artificialisation.developpement-durable.gouv.fr/sites/artificialisation/files/inline-files/definition%20artificialisation%20FF%20V3.pdf)
  - Differences in definitions explain most of the numerical gaps between sources — [Cerema](https://datafoncier.cerema.fr/sites/datafoncier/files/inline-files/chat_zan_2.pdf)
  - **Gridded data only contain surfaces geolocated to a parcel, so grid totals are lower than commune totals. Use commune data for reliable territorial statistics** — [Cerema documentation](https://doc-datafoncier.cerema.fr/doc/export/505)
  - Local mismatches can arise between the year consumption is recorded and the year permits were approved — [La Ferté-Alais local report](https://lafertealais.fr/uploads/ANNEXE%20DELIB%2004%20-%20Rapport%20LOCAL%20DIAGNOSTIC.pdf)
- **BNV-D:**
  - The buyer postcode gives the place of purchase, not the place or date of use, and purchased quantities do not reflect applied quantities or timing. There is no parcel location.
  - After audits, some distributors revised their sales without correctly re-spatialising them.
  - Only active substances are counted (no adjuvants). Postcodes with ≤5 farms are secret — [data.gouv BNV-D postcode dataset](https://www.data.gouv.fr/datasets/achats-de-produits-phytosanitaires-a-lechelle-du-code-postal); [SDES methodological note](https://www.statistiques.developpement-durable.gouv.fr/media/9573/download?inline)
- **Predictive habitat maps:** CarHab's EUNIS and Habitat-Directive correspondences are set by expert judgement — [CBN Brest CarHab sheet](https://www.cbnbrest.fr:/geonetwork/srv/api/records/b4ab7106-5626-4a2c-b1ac-e3653eec479f/attachments/Fiche_carhab.pdf). For the MPH limits, see §4.
- **ZAN legal uncertainty (Oct 2026):**
  - The Senate adopted the "TRACE" bill on 18 March 2025 (260–17). It removes the intermediate −50% target for 2031, and was transmitted to the Assemblée nationale.
  - A resolution proposing to put it on the AN agenda was filed on 29 Jan 2026. A competing cross-party bill to keep the ZAN course was filed in May 2025.
  - No AN vote or promulgation was found — [Banque des Territoires](https://www.banquedesterritoires.fr/trajectoire-de-reduction-de-lartificialisation-feu-vert-du-senat-pour-un-nouveau-round); [Acteurs publics](https://acteurspublics.fr/articles/le-senat-adopte-le-remplacement-du-zan-par-une-trajectoire-de-reduction-de-lartificialisation-le-senat-adopte-lassouplissement-du-zero-artificialisation-nette/); [AN resolution l17b2411](https://www.assemblee-nationale.fr/dyn/17/textes/l17b2411_proposition-resolution.pdf); [Banque des Territoires, competing bill](https://www.banquedesterritoires.fr/zero-artificialisation-nette-une-proposition-de-loi-lassemblee-en-contre-pied-du-texte-vote-au)

### Our reading
- **GBIF/OpenObs:**
  1. Never map raw species richness. Publish "records per cell" as an explicit effort layer.
  2. Compute ignorance scores per taxonomic group, and restrict hotspot claims to cells with G < 0.5.
  3. Use "residual richness" (richness regressed on log(records)) or presence of target species rather than richness.
  4. Deduplicate GBIF vs OpenObs. INPN-sourced data are probably present in both; verify on a sample.
  5. Aggregate blurred sensitive species to 10 km or commune.
- **MAUP:**
  - Show key indicators at two scales (1 km and EPCI) and state whether the rankings hold.
  - Build EPCI values from communes as ratios of sums.
  - Use commune-level Cerema data for EPCI totals and the 1 km data only for maps.
- **Vintages:**
  - OCS GE: express change as an annual rate over each department's own 3-year interval (2019→2022 or 2020→2023), label the vintage on every map, and avoid a stitched "regional 2022" map.
  - For cross-department comparisons of land take, use the homogeneous Cerema annual series.
- **Postcode → commune:** one postcode can cover several communes, and some communes have several postcodes. Allocate by UAA (from RPG) or by area weights, then aggregate to EPCI or basin. Treat secret postcodes as missing, not zero, and show a "n postcodes secret" counter.
- **Commune vs EPCI over time:**
  - Use the current INSEE geography and remap historical commune codes (communes nouvelles mergers) before building 2010–2025 time series.
  - Rebuild histories on today's EPCI boundaries.
- **HVE directory and other named records:** aggregate to commune or EPCI with a minimum-count rule. Never display farm names.
- **Predictive maps:** show probability classes, run results at two thresholds, and label CarHab-dependent outputs "pilote 3 départements".
- **ZAN:** present the Climat & Résilience −50% reference trajectory with a visible note that TRACE could modify it. Do not present EPCI "compliance" verdicts.

### Open points
- A possible RPG structural change around 2015 (îlots vs parcelles) was not verified here. Check it before any 2010–2025 grassland trend.
- The degree of GBIF/OpenObs duplication was not verified.
- No primary source was retrieved for the "target-group background" bias-correction method; only a patent text surfaced.

## 7. A sober web stack, and how to show it to the jury (RGESN)

### In short
The recommended stack is fully static: HTML/JS + MapLibre GL JS + PMTiles vector tiles (built offline with tippecanoe) + small precomputed JSON/Parquet tables on static hosting. It is serverless, transfers little data, needs little maintenance, and works for every piste. DuckDB-WASM is optional and should load only on an "explorer" page. Demonstrate sobriety with an RGESN 2024 self-declaration (official template) plus measured EcoIndex, page weight and request counts, and a documented data-transfer budget per session.

### Sources
- **PMTiles:**
  - A single-file tile archive. Readers use HTTP range requests to fetch only the tiles they need, with no tile server ("serverless").
  - It is read-only: updating means rewriting the file. The spec is at v3.
  - MapLibre reads it via a `pmtiles://` source — [Protomaps PMTiles docs](https://docs.protomaps.com/pmtiles/); [MapLibre PMTiles](https://maplibre.org/flutter-maplibre-gl/advanced/pmtiles/)
  - Cloud storage: Cloudflare R2 is recommended (no egress fees, per-request billing). Cross-origin hosting needs CORS that allows the `range` and `if-match` headers and exposes `etag` — [Protomaps cloud storage](https://docs.protomaps.com/pmtiles/cloud-storage)
- **GitHub Pages:** a secondary guide warns that files over 100 MB are not recommended and mentions a ~100 GB/month soft bandwidth limit — [DEV Community guide](https://dev.to/ronitjadhav/how-to-host-and-test-pmtiles-on-github-pages-the-easiest-way-to-serve-maps-without-a-server-2ei8)
- **tippecanoe (Felt fork):** useful flags are `--drop-densest-as-needed`, `--extend-zooms-if-still-dropping`, `-zg` and `--coalesce-densest-as-needed`. It writes `.pmtiles` directly with `-o`, and `tile-join` converts MBTiles to PMTiles — [felt/tippecanoe](https://github.com/felt/tippecanoe); [palewi.re PMTiles tutorial](https://palewi.re/docs/first-pmtiles-map/build-tiles.html)
- **DuckDB-WASM:**
  - The extension list includes `spatial`, `parquet` and `json`, autoloading is on by default, and community extensions such as `h3` can be loaded (`INSTALL h3 FROM community`).
  - The native httpfs is not compiled in; a JavaScript reimplementation follows browser security rules. Requests are upgraded to HTTPS, and data hosts must allow CORS — [DuckDB-WASM extensions](https://duckdb.org/docs/current/clients/wasm/extensions.html)
  - DuckDB reads only the bytes a query needs from remote Parquet — [DuckDB-WASM overview](https://www.duckdb.org/docs/current/clients/wasm/overview)
- **H3 average cell areas:** res 7 ≈ 5.16 km², res 8 ≈ 0.737 km², res 9 ≈ 0.105 km² — [H3 resolution table](https://h3geo.org/docs/core-library/restable/)
- **RGESN 2024 (official template):**
  - Published by Arcep and Arcom with ADEME, DINUM, CNIL and Inria.
  - Four objectives: extend device lifespan, promote environmental sobriety, reduce the computing resources used, and increase transparency on environmental footprint.
  - Nine chapters: 1 Stratégie, 2 Spécifications, 3 Architecture, 4 UX/UI, 5 Contenus, 6 Frontend, 7 Backend, 8 Hébergement, 9 Algorithmie. Chapter 9 covers justification, learning phase, data collection, updates, compression and inference.
  - The declaration lists validated, non-validated and non-applicable criteria, an optional progress score, an action plan, the critical paths and functional units assessed, and a named référent — [Arcep RGESN 2024 declaration template](https://www.arcep.fr/fileadmin/user_upload/nos-sujets/environnement/rgesn_2024_exemple_declaration_ecoconception.html); [ODT template on ecoresponsable.numerique.gouv.fr](https://ecoresponsable.numerique.gouv.fr/docs/2024/rgesn-mai2024/rgesn_2024_exemple_declaration_ecoconception.odt)
  - 78 criteria in 9 themes, each rated for difficulty, priority and applicability. The referential stems from the REEN law of 15 Nov 2021; the first version dates from 2022 — [ISIT RGESN wiki](https://en.wiki.isit-europe.org/nr/RGESN)
  - Example public-service declarations: [DiaLog (beta.gouv) declaration](https://dialog.beta.gouv.fr/files/2025-03-06%20-%20D%C3%A9claration%20%C3%A9coconception%20DiaLog%20-%20D%C3%A9tail.pdf); [Ville de Nîmes self-assessment](https://www.nimes.fr/fileadmin/mediatheque/nimes/pages-transversales/ecoconception-numerique/DOSSIER-AUTO-EVALUATION-RGESN-Nimes-20240324.pdf)
- **EcoIndex:**
  - Uses DOM size, page weight and number of requests, weighted ~3/2/1, and gives an A–G grade plus GHG and water estimates.
  - It does not model the user's device or network, nor page rendering — [Cerin et al., GreenDays 2023](https://perso.ens-lyon.fr/laurent.lefevre/greendayslyon2023/slides/GreenDays2023_Cerin.pdf); [Centreon, differences with EcoIndex](https://docs-preview-int.centreon.com/previews/pr-5393/next/experience-monitoring/digital-sobriety/differences-with-eco-index/)
  - Reference implementation: [GreenIT-Analysis ecoIndex.js](https://github.com/cnumr/GreenIT-Analysis/blob/master/script/ecoIndex.js). The Lighthouse "Green IT" plugin adds a flat +10 points — [plugin README](https://unpkg.com/lighthouse-plugin-green-it@2.0.1/README.md)
- MapLibre math expressions make client-side reweighting possible (§1) — [MapLibre style spec](https://maplibre.org/maplibre-style-spec/expressions/)

### Our reading
- **Reference architecture, common to all pistes:**
  1. *Offline pipeline (laptop, run once):*
     - Python (pyogrio, GeoPandas, shapely 2) + DuckDB spatial ≥1.3, plus optional R for riverconn, prioritizr and graph4lg.
     - Flow: raw open data → GeoParquet (EPSG:2154) → indicator tables (Parquet/CSV) → web exports.
     - One `make`/script entry point and a README with runtimes. Reproducibility is part of "feasibility".
  2. *Web exports:*
     - (a) Thematic PMTiles: 1 km grid; communes and EPCI with integer indicator attributes; brownfield points; candidate polygons.
     - (b) Per-entity JSON (commune or EPCI sheets, a few KB each), or one compact table.
     - (c) Static methods, data-dictionary and sobriety pages.
  3. *Frontend:*
     - Vanilla JS or a light framework, MapLibre GL JS + the pmtiles protocol.
     - No third-party basemap: build a minimal basemap from your own PMTiles (admin boundaries, main hydrography), or use a Normandy extract of a Protomaps basemap.
     - System fonts, no trackers, no third-party calls.
  4. *Hosting:*
     - Static host (GitHub Pages / Netlify / any French static host) for HTML/JS.
     - PMTiles under ~100 MB can sit next to the site. Larger files go to object storage with CORS (range / if-match / etag).
     - Hashed filenames with long cache lifetimes.
- **Size budgets (estimates to validate):**
  - The 1 km grid (~30k cells × ~10 integer attributes) should be a few MB of PMTiles across zooms.
  - The 5,068 brownfields should be well under 1 MB as GeoJSON.
  - Communes should be a few MB of simplified tiles.
  - 2.7 M hedges are the outlier. Don't ship raw lines at low zooms: show a density grid below z11 and hedges only at z ≥ 12–13 with simplification, or only for pilot areas. Otherwise the archive could reach hundreds of MB.
- **DuckDB-WASM:** worth it only if users need ad-hoc filtering of tables larger than a few MB. Otherwise JSON + JS is lighter. If used, lazy-load it on demand.
- **Grid choice:** prefer a square 1 km grid aligned with the INPN/national referential (used by DSB) and with the Cerema 1 km grid (check alignment). H3 res 8 (~0.74 km²) only makes sense if hexagons are wanted for aesthetics, at the cost of misalignment with official grids.
- **How to demonstrate sobriety to the jury:**
  1. Publish an RGESN 2024 declaration using the official template, with the % of applicable criteria met and N/A criteria justified (chapter 7 Backend is mostly N/A for a static site, and that is a selling point).
  2. Report EcoIndex grades for the 3–4 key pages (target A/B), with page weight, requests and DOM size, before and after optimisation.
  3. State a "transfer budget" for a typical 3-minute session (e.g. ≤ 1–2 MB, tiles on demand), measured in devtools with network throttling.
  4. Report the pipeline's compute time on a laptop and that it runs once (no server, no database, no continuous compute).
  5. Justify the choice of transparent indices over ML (RGESN chapter 9, "justification").
  6. Test on an old phone or low bandwidth (RGESN objective 1, device lifespan).
  7. Open code and data so a public body can re-run it.

### Open points
- The current DuckDB-WASM bundle size (with spatial) was not verified. An unverified secondary page quoted ~2.5 MB brotli WASM for an older synchronous build. Measure in devtools.
- GitHub Pages support for byte-range requests was not confirmed by a primary source; test with the pmtiles viewer.
- MapLibre GL JS bundle size was not checked.
- Which 1 km grid (INSPIRE LAEA or a Lambert-93 national grid) the Cerema land-take series uses was not verified.

## 8. Feasibility in 3.5 weeks and minimal demo per piste

### In short
The most feasible pistes are **A (Friches → Nature), G (restorable wetlands) and I (what concrete ate)**. Each rests on single-overlay or single-table logic, has a strong policy hook (ZAN, the Nature Restoration Regulation, SNAP) and produces a small web payload. **K** is technically easy but should be a citizen front-end on top of another piste. **Medium:** B, C (scoped), D (15–20-indicator subset), F (if a river network is available), H (3-department pilot), E, J (as an add-on), L (arithmetic scenarios only). **Low:** M and N. Every MVP should follow the demo script "question → map → explain this score → actionable list/export → sobriety page".

### Sources
- **Policy hooks that strengthen a "decision-support" pitch:**
  - Draft National Restoration Plans were due 1 Sept 2026, with the 25,000 km free-flowing rivers target — [Garrigues](https://www.garrigues.com/en_GB/new/eu-bolsters-nature-restoration-here-new-legislative-framework-2030-and-2050)
  - Pacte haie: +50,000 km net by 2030 — [Banque des Territoires](https://www.banquedesterritoires.fr/le-gouvernement-presente-un-pacte-pour-planter-50000-km-de-nouvelles-haies-dici-2030)
  - SNAP: 30% protected / 10% strongly protected — [DREAL PdL](https://www.pays-de-la-loire.developpement-durable.gouv.fr/IMG/pdf/20211217_snap.pdf)
  - ZAN / TRACE uncertainty — [Banque des Territoires](https://www.banquedesterritoires.fr/trajectoire-de-reduction-de-lartificialisation-feu-vert-du-senat-pour-un-nouveau-round)
- **Benchmarks for piste A:**
  - ADEME's Mutafriches is a decision tool that identifies the most suitable potential uses of a given brownfield. Bénéfriches quantifies and monetises the environmental, social and economic impacts of a project — [ADEME foncier & friches](https://agirpourlatransition.ademe.fr/collectivites/conseils/urbanisme/foncier-friches)
  - Cerema has inventoried 15,000 brownfields totalling 60,000 ha (Cartofriches) — [Les EPL](https://www.lesepl.fr/2025/09/le-cerema-inventorie-plus-de-60-000-hectares-de-friches-en-france/?pdf=132551)
  - A "Référentiel Renaturation" was published in May 2026 by the Institut de la Transition foncière with ADEME support — [Référentiel Renaturation PDF](https://www.novabuild.fr/wp-content/uploads/2026/05/Referentiel-Renaturation.pdf)
  - Cerema's method for ranking artificialised spaces for renaturation — [Cerema](https://www.cerema.fr/fr/print/pdf/node/15052)
- **Method and data facts used in the cards below:** see §1–§7. Key ones are the DuckDB spatial-join performance ([DuckDB](https://duckdb.org/2025/08/08/spatial-joins)), the MPH 1:100,000 limits ([Notice MPH](https://geosas.fr/metadata/pdf/Notice_MPH_France-1.pdf)), Cerema grid totals being lower than commune totals ([Cerema](https://doc-datafoncier.cerema.fr/doc/export/505)), the BNV-D limits ([SDES](https://www.statistiques.developpement-durable.gouv.fr/media/9573/download?inline)), the ROE "Indéterminée" heights ([ROE manual](https://www.eaufrance.fr/sites/default/files/2019-04/roe-referentiel-des-obstacles-a-l-ecoulement-manuel-d-utilsation.pdf)) and the Omniscape and Graphab cost levers ([Omniscape](https://docs.circuitscape.org/Omniscape.jl/latest/usage/); [Graphab](https://thema.umlp.fr/productions/software/graphab/en/home.html)).

### Our reading

#### Planning assumptions (all pistes)
- **Calendar:** 17 Oct → 12 Nov 2026 at noon is about 26 days. 11 Nov is a public holiday in France. Plan a code and data freeze on 9–10 Nov and keep 11 Nov for packaging.
- **Capacity:** with 2–5 people at partial availability, assume roughly 20–60 pd in total. Reserve about 25% for packaging: README, code and data deposit, data dictionary, RGESN declaration, EcoIndex measurement, pitch and demo video.
- **Shared base, spent once whatever the piste:**
  - Common keys (current communes/EPCI, 1 km grid, Lambert-93): 2–3 pd
  - Static web skeleton (MapLibre + PMTiles + methods/sobriety pages): 3–5 pd
  - Packaging: 3–5 pd
  - Total ≈ 8–13 pd. The piste efforts below come on top of this.
- **Standard "convincing demo" (3 minutes):**
  1. A policy question, such as "Où renaturer en priorité dans mon EPCI ?".
  2. The map answers it, with presets.
  3. Click a unit to see "why": the criteria contributions plus data caveats.
  4. Export an action list (CSV) or a fact-sheet.
  5. Show the sobriety page (EcoIndex, transfer budget, RGESN %).

#### A. Friches → Nature: rank the 5,068 EPF brownfields by renaturation potential vs constraints
- **Method and tooling:**
  - Score each site on two transparent axes.
    - *Ecological potential:* distance to or overlap with ZNIEFF, Natura 2000 and TVB reservoirs/corridors; MPH potential-wetland and flood-zone flags; hedge density and grassland share within 500 m–1 km; site area; urban green-space deficit.
    - *Constraints:* pollution flag, built footprint, zoning, access, existing project.
  - Show a 2 × 2 matrix whose "quick wins" are high-potential, low-constraint sites, plus a slider-weighted score. Use percentile normalisation and an offline weight-robustness check (§1).
  - Tooling: DuckDB spatial or GeoPandas (`ST_DWithin`, buffers derived from the surface field if geometries are points). Web: MapLibre circle layer (well under 1 MB), a sortable table and a site card.
  - Cite Mutafriches, the Cerema renaturation method and the 2026 Référentiel Renaturation as the lineage.
- **Main risks:**
  - Attribute completeness: an "unknown" pollution status is not "unpolluted".
  - Point vs polygon geometry.
  - Renaturation feasibility depends on remediation cost, ownership and land value, which are not in the data.
  - "Black-box ranking" perception and subjective weights.
  - ZAN accounting nuance for renaturation (désartificialisation).
- **MVP by 12 Nov:**
  - A map and table of all 5,068 sites, each with its score, class and top-3 reasons.
  - 3–4 presets (biodiversité, eau/inondation, nature en ville, sobriété foncière) plus sliders.
  - EPCI filter and CSV export.
  - 3 fact-sheets for top sites.
  - A methods page with a sensitivity chart.
- **Effort:** ~10–13 pd.
- **Feasibility: HIGH.** Main risk: EPF attribute completeness and the credibility of the weights (mitigate with visible contributions and sensitivity analysis).

#### B. Multi-criteria restoration priority map per 1 km cell or commune (stakes × degradation × opportunity)
- **Method and tooling:**
  - 6–9 criteria in 3 sub-indices.
    - *Stakes:* ZNIEFF/Natura share, MPH probability, effort-corrected heritage-species presence, CarHab HIC share (3 departments only, or excluded).
    - *Degradation:* land-take rate (Cerema), hedge-density deficit vs the department median, arable share or grassland loss (RPG), WFD status, obstacle density.
    - *Opportunity:* brownfields (A), potential wetlands under crops (G).
  - Percentile normalisation, correlation pruning, a weighted sum with sliders plus an S × D × O preset, and a Monte-Carlo "robust priority" layer.
  - Optional prioritizr minimum-set portfolio with CBC or HiGHS.
  - Tooling: DuckDB/GeoPandas gridding, MapLibre expression recolouring, a JSON table for rankings.
- **Main risks:**
  - Indicator redundancy and double counting.
  - Partial coverage (CarHab 3/5) and OCS GE vintage offsets.
  - MAUP, and Cerema grid totals below commune totals.
  - Jury fatigue with "yet another composite".
  - Time spent wrangling 6–9 sources.
- **MVP:**
  - Grid choropleth with the three sub-index layers, presets and sliders.
  - "Explain this cell" popup and an EPCI summary.
  - Robustness map.
- **Effort:** ~15–20 pd, plus 3–5 pd for the prioritizr bonus.
- **Feasibility: MEDIUM.** Main risk: heterogeneous coverage and vintages plus indicator redundancy undermining credibility (cap at ≤9 well-documented criteria).

#### C. Normandy bocage over 70 years: loss, fragmentation/connectivity, resilient communes, planting targeting
- **Method and tooling:**
  1. *Current state, wall-to-wall:* DSB-style density (m/ha) per 1 km cell and per commune, hedge–forest connections (OCS GE woodland), and graph metrics on the snapped network (components, largest-component share, junction density) using DuckDB/GeoPandas and igraph.
  2. *70-year trend:* only from the DREAL sample circles (300 m radius; 1947/1972/2006/2010/2016). Compute mean density per date and stratum (department or landscape unit) with bootstrap confidence intervals. Call communes "resilient" only where enough circles exist; otherwise work at landscape-unit level.
  3. *Planting targeting:* rule-based. Select gap-bridging candidates ≤ 20–50 m between components, adjacent to woodland or reservoirs, in arable-dominated cells with low density. Add slope and watercourse criteria only if a DEM or hydro network is added.
  4. *Optional Graphab 3.0 pilot:* a woodland + hedge habitat, resistance by land cover, and dPC of candidate plantings, all in one ~20 × 20 km landscape.
  - Copernicus SWF 2021 serves only as a cross-check. Different methods mean no change detection between products.
- **Main risks:**
  - Temporal comparability across sources (IGN Haie vs SWF vs DREAL photo-interpretation): there is no valid wall-to-wall 70-year change map.
  - Topology cleaning of 2.7 M segments.
  - "A line is not a functional hedge".
  - Over-claiming "resilience".
  - Tile size for the hedge lines.
  - Graphab and Omniscape parameterisation and compute (§2).
- **MVP:**
  - Density map (1 km and commune) with department benchmarks.
  - Sample-based trend chart for 1947 → 2016 with confidence intervals.
  - Planting-priority layer and a top-communes list.
  - A Pacte haie gauge (km needed to reach a target density).
  - One Graphab case study, optional.
- **Effort:** ~15–22 pd, or ~12–16 pd without the Graphab pilot.
- **Feasibility: MEDIUM.** Main risk: multi-source temporal comparability and topology cleaning (keep the 70-year story sample-based).

#### D. Biodiversity bulletin per EPCI built on the Région's 68 COP ecological-planning indicators (+ others)
- **Method and tooling:**
  - Triage the 68 COP indicators into three groups: computable per EPCI from open data, regional only, or not computable.
  - Implement 15–20 computable indicators as ONB-style sheets with DPSIR tags, peer-group comparison (EPCI typology), trend arrows and caveats.
  - Generate one static, printable HTML page per EPCI (~100 KB each) with Python/Jinja.
  - Add 2–3 rule-based "priority messages" per EPCI (largest negative gaps vs peers).
- **Main risks:**
  - Many COP indicators may exist only at regional level and cannot be meaningfully downscaled.
  - Breadth of ingestion across many sources.
  - Vintage heterogeneity and small-number instability.
  - The normalisation choice changes rankings.
  - Becoming a "dashboard without decision".
- **MVP:**
  - Pages for every Normandy EPCI covering 15–20 indicators.
  - A regional overview map.
  - A methodology appendix that maps the 68 COP indicators to their status.
- **Effort:** ~13–18 pd.
- **Feasibility: MEDIUM** (HIGH for a 15–20-indicator subset; LOW for all 68). Main risk: EPCI-level availability of the COP indicators.

#### E. Water × agriculture pressure–impact by river basin
- **Method and tooling:**
  - Unit: water-body catchment or sub-basin. **Dependency:** catchment polygons are not in the established inventory.
  - *Pressures:* arable and maize share and grassland loss (RPG); pesticide purchases apportioned postcode → commune → catchment by UAA weights (flagged); withdrawals by use (Hub'Eau); obstacle density and taux d'étagement (ROE).
  - *State:* WFD ecological status (2019), hydrobiology and fish indices (Hub'Eau), ONDE dry-flow frequency.
  - Analysis: quadrant plots, Spearman correlations and simple stratified comparisons. Make no causal claims.
- **Main risks:**
  - Spatial mismatch (postcodes vs catchments), and purchases are not use.
  - Temporal mismatch (status in 2019 vs pressures in the 2020s).
  - Station representativeness and confounders (geology, urban discharges).
  - API ingestion volume and paging.
  - Ecological fallacy.
- **MVP:**
  - Catchment map of a pressure index vs status.
  - A scatter plot.
  - Station drill-down with the latest indices.
  - A caveat panel.
- **Effort:** ~14–18 pd.
- **Feasibility: MEDIUM-LOW.** Main risk: spurious pressure–impact relations driven by spatial and temporal mismatches.

#### F. River continuity: prioritise obstacle removal
- **Method and tooling:** use the "km reconnected if removed" ΔDCI proxy weighted by height class, migratory-fish relevance and WFD status (riverconn in R, or igraph in Python). Add taux d'étagement and taux de fractionnement where heights are known, and a greedy "remove top N" scenario (§3).
- **Main risks:**
  - **A topologically correct hydrographic network is needed but not in the established inventory.**
  - Snapping errors.
  - "Indéterminée" heights and sparse ICE passability data.
  - Outdated obstacle statuses.
  - Social and heritage sensitivity (mills, water rights).
  - No cost data, so no true OptiPass.
- **MVP:**
  - Ranked obstacle map and list with km gains and reasons.
  - Per-basin étagement where computable.
  - "Top N" scenario.
  - Framing against the NRR 25,000 km target.
- **Effort:** ~13–17 pd, of which 5–8 pd for the network.
- **Feasibility: MEDIUM.** Main risk: building a clean river network and the incompleteness of ROE heights and passability.

#### G. Restorable wetlands: potential wetlands now under crops or artificial land
- **Method and tooling:**
  - MPH (forte / très forte) ∩ RPG arable crops ∪ (MPH ∩ OCS GE artificial classes).
  - Restorability score: probability class, current use, adjacency to protected or inventoried sites, flood-zone overlap, cluster size.
  - Aggregate in ha per EPCI and sub-basin, and list "low-regret" clusters (§4).
  - Tooling: DuckDB/GeoPandas raster-to-vector or zonal overlays; PMTiles for candidate clusters.
- **Main risks:**
  - Over-interpreting a 1:100,000 pre-localisation that ignores drainage and land use; the 50 m pixels suggest false precision.
  - The "25% of the territory" controversy and farmer acceptability.
  - RPG only covers CAP-declared land.
  - OCS GE vintage offsets.
- **MVP:**
  - Candidate map filterable by current use and probability.
  - EPCI and sub-basin statistics.
  - Top-20 low-regret clusters with fact-sheets.
  - "Non-regulatory pre-localisation" disclaimer.
- **Effort:** ~8–11 pd.
- **Feasibility: HIGH.** Main risk: over-interpretation of the MPH model at parcel scale and social acceptability.

#### H. Blind spots of protection: gap analysis of probable HIC habitats and protected-species hotspots outside protected areas
- **Method and tooling:**
  - Pre-process CarHab once into GeoParquet keeping HIC code, probability and geometry.
  - Per HIC type, compute % inside Natura 2000 and inside strong protection vs the 30%/10% SNAP references or type-specific targets, at two probability thresholds.
  - Map heritage-species hotspots in well-sampled cells (ignorance score) outside protected areas.
  - Optional prioritizr minimum-set to fill the gaps (§4, §6).
- **Main risks:**
  - CarHab covers only 3 of 5 departments, so frame it as a "3-department pilot".
  - Predictive uncertainty, with HIC correspondences set by expert judgement.
  - Observer bias and the blurring of sensitive species.
  - Defining "protection forte" (which designations count).
  - Heavy CarHab files (3.4 GB unzipped for Manche).
- **MVP:**
  - Table and map of HIC types with their protection rates and gap flags (3 departments).
  - Map of unprotected hotspots in well-sampled cells.
  - Uncertainty toggles.
- **Effort:** ~13–16 pd, including 3–5 pd for CarHab pre-processing.
- **Feasibility: MEDIUM.** Main risk: partial CarHab coverage and predictive uncertainty, compounded by sampling bias.

#### I. "What concrete ate": recent artificialisation over hedges, grasslands, ZNIEFF, wetlands; losses per EPCI vs the ZAN trajectory
- **Method and tooling:**
  1. *ZAN trajectory per EPCI:* Cerema NAF consumption, commune-level summed to EPCI. Compare 2011–2021 (reference) with 2021–2025 (actual pace) and with the 2021–2031 envelope (−50% reference).
  2. *What was consumed:* intersect OCS GE change polygons (each department's own interval, annualised) with RPG grassland vs arable in the start year, the IGN hedges (km intersected; the layer's date is a caveat), ZNIEFF and MPH.
  3. *Map:* change polygons as PMTiles.
- **Main risks:**
  - Department vintage offsets.
  - Consumption vs artificialisation definitions.
  - Grid totals below commune totals.
  - Hedge-layer dating (did the hedge exist before the change?).
  - ZAN legal uncertainty (TRACE).
- **MVP:**
  - An EPCI dashboard with a trajectory chart and a stacked "what was consumed" bar.
  - Change map and methods page.
  - Optional link to A: "brownfield hectares available vs hectares consumed".
- **Effort:** ~11–13 pd.
- **Feasibility: HIGH.** Main risk: vintage and definition mismatches, plus ZAN legal uncertainty (present it as a "reference trajectory").

#### J. Coherence of public action: needs × efforts matrix per EPCI
- **Method and tooling:**
  - A needs index (reused from B or D) vs an efforts index: Fonds vert biodiversity/renaturation € per capita and per ha (aggregated to EPCI because commune codes are missing), protected-area share, and HVE share (aggregated).
  - Show a 2 × 2 quadrant and a scatter plot with peer groups, plus a rank correlation.
- **Main risks:**
  - "Efforts" cover only some funding streams (Fonds vert 2023–2025; water-agency, Région, EU and LIFE funding are absent), so "under-investment" labels can be wrong.
  - Time lags.
  - Political sensitivity of naming EPCI.
  - Normalisation choice.
  - Privacy (HVE names).
- **MVP:**
  - Interactive needs-vs-efforts scatter and quadrant map.
  - EPCI drill-down with explicit coverage caveats.
- **Effort:** ~7–10 pd if B or D exists; otherwise add 10–15 pd.
- **Feasibility: MEDIUM-LOW (standalone) / MEDIUM (as an add-on to B or D).** Main risk: incomplete effort data producing misleading judgements.

#### K. Citizen interface "Ma commune et sa nature"
- **Method and tooling:**
  - Static commune pages generated from the indicators of D, I and C: hedge density vs peers, land take, protected areas, water status, observation effort plus notable species (flagged as effort-dependent), good practices, and "what you can do".
  - Plain language, accessibility (RGAA), a few KB of JSON per commune, and a search box.
- **Main risks:**
  - The public may misread biased indicators (species counts mostly reflect observation effort).
  - Small-number and secrecy rules.
  - Weak decision-support value on its own for this jury.
  - Scope creep.
- **MVP:** commune search → a page with 8–10 indicators, a mini-map and a "compare with similar communes" panel.
- **Effort:** ~6–10 pd on top of an indicator piste.
- **Feasibility: HIGH technically / LOW as a standalone entry.** Main risk: limited decision value and misinterpretation, so pair it with A, C, D, G or I.

#### L. Scenario simulator ("what if" hedges planted / brownfields renatured → connectivity and land-take indicators)
- **Method and tooling:**
  - Use precomputed deltas with an additive approximation.
    - *Brownfields:* renatured ha feed into the EPCI land-take/ZAN balance (simple arithmetic, robust).
    - *Hedges:* km planted update density and Pacte haie progress per commune.
  - Connectivity deltas only for a pilot area (Graphab dPC of candidate plantings), with a greedy precomputed order.
  - The UI selects N candidates and sums their deltas client-side.
- **Main risks:**
  - Connectivity gains are not additive (interactions between candidates).
  - Recomputation cost (Graphab and Omniscape cannot run in the browser).
  - Over-promising "simulation".
  - UI complexity.
- **MVP:** two sliders ("ha renatured", "km planted") with instant indicator changes per EPCI or commune, plus one pilot connectivity case.
- **Effort:** ~6–8 pd (arithmetic only) or ~12–18 pd with the connectivity pilot, on top of A or C.
- **Feasibility: MEDIUM (arithmetic) / LOW (connectivity).** Main risk: non-additive connectivity metrics and their compute cost.

#### M. Coast & Seine estuary pressures
- **Method and tooling:**
  - A coastal strip (coastal communes or a 1–2 km buffer) with land take and artificialisation of coastal habitats.
  - CarHab dunes and salt marshes: the three CarHab departments are the coastal ones (Calvados, Manche, Seine-Maritime), but the estuary's Eure bank would lack CarHab.
  - Obstacles on small coastal rivers (diadromous fish) and WFD transitional/coastal water status.
- **Main risks:**
  - Marine and coastal pressure data (erosion, bathing and shellfish water quality, port activity) are largely outside the established open-data inventory.
  - Likely overlap with existing estuary observatories (not researched).
  - Wide scope.
- **MVP:** coastal-strip dashboard of 6–8 indicators plus a habitat-loss map for the 3 departments.
- **Effort:** ~12–18 pd.
- **Feasibility: LOW.** Main risk: missing coastal and marine pressure data within the established inventory.

#### N. Horses & grasslands (equine sector as a driver of grassland/bocage maintenance)
- **Method and tooling:** correlate equine density (only if open data exist) with permanent-grassland share and trends (RPG 2010–2025) and hedge density per commune or canton, and build a typology of grassland systems.
- **Main risks:**
  - Equine open-data availability is uncertain.
  - Correlation is not a driver: there are strong regional confounders (soils, dairy systems, tradition).
  - Ecological fallacy.
  - Possible RPG structural break around 2015 (to verify, §6).
- **MVP:** commune-level permanent-grassland map and trend (feasible regardless), with the equine overlay only if data are found.
- **Effort:** ~6–10 pd, plus the data risk.
- **Feasibility: LOW.** Main risk: equine data availability and causal attribution. Better folded into C or I as a "grassland" sub-story.

#### Suggested combinations for a 2–5 person team
- **"Renaturer sans artificialiser"** = I + A + L (arithmetic), with an optional K front-end. It answers P1 (where to renature: brownfields) and P2 (negative interaction: land take; positive: renaturation) and shares one stack. ≈ 30–40 pd including the shared base. This is the best feasibility-to-impact ratio.
- **"Eau & zones humides"** = G + F (if a river network is available), or G + E-lite. ≈ 30–40 pd.
- **"Bocage"** = C (scoped) + L (hedge arithmetic) + K. ≈ 30–40 pd.
- **"Intégrateur"** = B with presets + J as a quadrant add-on. ≈ 30–35 pd; higher credibility risk.

### Open points
- Feasibility depends on attributes not profiled here: EPF field completeness, the share of ROE heights known, availability of a hydrographic network and catchment polygons, equine data, and EPCI-level availability of the 68 COP indicators.
- No information was found on the jury's detailed scoring grid beyond the organisers' published brief (sobriety and feasibility explicitly scored).
- The effort estimates are expert inferences, not benchmarks. Validate them against a one-day spike on the riskiest step of the chosen piste: the hedge overlay for C, CarHab pre-processing for H, the river network for F.
