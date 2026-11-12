# Detecting and mapping grassland → cropland conversion ("retournement de prairies") from open data: methods, pitfalls and feasibility for Normandy (Datathon Normandie 2026)

Some quoted numbers come from PDF tables whose layout was partly lost when converted to text; each such case is flagged.

---

## 1. Official methods for measuring ploughing from the RPG

### In short
The closest official template is the DRAAF/Agreste Grand Est method (Dec. 2022). It overlays RPG vintages pairwise (N vs N+1, 2015–2019), maps PAC crop codes to 4 classes and classifies each permanent-grassland (PP) parcel's fate. It reports "strict" ploughing at about 1–1.2 % of PP per year, and an upper bound of about 2.1 % once PP→PT conversions and "disappeared" parcels are included. The often-quoted Normandy "82 % to arable / 18 % to artificialisation" figure does **not** come from the RPG. It comes from **OSCOM** (the DRAAF commune-level land-use observatory) and counts permanent and temporary grassland together. The only open precomputed parcel-sequence product is INRAE's **RPG Explorer** crop-sequence dataset (2015–2024).

### Sources
**Agreste Normandie, Études n°6 (Sept. 2021): where the 82 %/18 % figure comes from**
- Normandy lost 11 % of its agricultural grassland between 2008 and 2019. The loss is concentrated in dairy systems, and conversion to arable land explains most of it — [DRAAF Normandie, Agreste Études n°6](https://draaf.normandie.agriculture.gouv.fr/agreste-etudes-no6-septembre-2021-le-retournement-de-prairies-en-faveur-de-a2696.html)
- The methods box (Encadré 3) says the source is **OSCOM (Observatoire des Sols à l'échelle COMmunale)**, produced by the DRAAF Normandie, which describes land use every year. In OSCOM, "prairies" means **permanent and temporary grassland combined**. The study also used ASP PAC surfaces, BDNI 2007–2018 and a DRAAF estimate for the farming-system analysis — [Agreste Études n°6 PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- Encadré 3 table, as extracted (layout partly lost; column reading inferred). Normandy "prairies et autres sols agricoles" changed by **−107,799 ha** over 2008–2019, of which −88,641 ha went to arable land. The split is **82 % to arable / 18 % to artificialisation**. By department (arable % / artificialisation %): Calvados 76/24, Eure 71/29, Manche 84/15, Orne 94/6, Seine-Maritime 80/20 — [Agreste Études n°6 PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- The maps smooth the commune-level losses with a Biweight kernel on a 1 km² hexagon grid, with a 7.5 km radius. A commune is shown only if its loss exceeds 1 ha/km², and a destination counts as "majority" if it takes ≥ 2/3 of the lost grassland. This is a published precedent for grid aggregation and smoothing as a display method — [Agreste Études n°6 PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- The Normandy Regional Biodiversity Strategy quotes the 2008–2019 loss as 94,500 ha — [SRB Normandie 2030](https://www.normandie.fr/sites/default/files/2023-05/srb-normandie-presentation.pdf). (This differs from the 107,799 ha OSCOM total, probably because of a different perimeter: grassland only vs "prairies et autres sols agricoles". Not reconciled.)

**Agreste Grand Est n°3 (Dec. 2022): the RPG pairwise-overlay method**
- **Method.** RPG vintages 2015–2019 are overlaid pairwise (N, N+1). For each PP parcel in year N, the method records its class in N+1 and the area in hectares. Results are then summed by area of interest. A correspondence table maps PAC codes to 4 analysis classes: PP, PT, arable (TA), and fallow (jachère). Fallow is merged with grassland, temporary or permanent depending on its age. The study states that its results cannot be used to compute the regulatory BCAE 1 ratio — [Agreste Grand Est n°3, 2022](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- **Outcome classes.** PP stays PP; PP→TA ("retournement au sens strict"); PP→PT; and "Autre" (non-agricultural codes, or parcel absent from the RPG in N+1 or N−1) — [same](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- **Results.** Strict ploughing averaged **8,700 ha/yr, about 1–1.2 % of declared PP per year**. In 2015→2016, 97.3 % of PP stayed PP, 1.2 % became TA, 0.5 % became PT and 0.9 % had an "other" fate. Adding PP→PT and "disappeared" PP gives **15,950 ha/yr, about 2.1 %/yr, which the study calls an upper bound**. It falls to 1.76 % in the last two years — [same](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- **Paradox.** Declared PP area *rose* by about 1 % over the period even though ploughing happened every year. The cause was the administrative requalification of PT into PP, with a large catch-up in 2018 when grassland declared as PT since 2014 was automatically reclassified. The study calls this an *"administrative catch-up with no real change on the parcels"*. Net stock change is therefore not a measure of ploughing — [same](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- **Stated caveats.** Not all grassland is declared to the PAC (some retired farmers, non-farmer owners, collective structures). The boundaries between PT, PP and fallow are blurry. Codes are self-declared for administrative purposes, not as scientific observation. "Disappeared" PP feeds a fuzzy stock of fallow land, buffer strips and undeclared grass, part of which later becomes artificialised — [same](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- **Crops after ploughing.** Maize (grain and silage) is over-represented, and wheat, barley and rapeseed are under-represented. The study links this to wetter, flood-prone parcels and to demand from methanisation — [same](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)

**INRAE / ODR / RPG Explorer**
- **RPG Explorer** (INRAE / AgroParisTech; Philippe Martin et al.; GPL v3, source on GitLab, binary on request). It reconstructs crop sequences, explicitly including grassland sequences and grassland ploughing. Sequences are built by spatially overlaying the parcels of successive years into "smallest common parcels" — [rpgexplorer.fr](https://rpgexplorer.fr/)
- **Precomputed open dataset:** "Crop successions 2015–2024 (France mainland) – RPG Explorer", DOI 10.57745/6G0JTJ (Girault & Martin), GeoPackage by department. Earlier versions cover 2015–2021, 2015–2022 and 2015–2023 — [Recherche Data Gouv 6G0JTJ](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/6G0JTJ); [RPG Explorer dataverse](https://entrepot.recherche.data.gouv.fr/dataverse/rpg-explorer). A Parquet national version is mentioned only in a LinkedIn post by P. Martin (unverified on the dataset page) — [LinkedIn](https://www.linkedin.com/in/philippe-martin-26271744/)
- **Pre-2015 îlot filiation (older INRAE method).** Îlots of successive years are linked by spatial correspondence through an intersection table. A further rule matches by similar crop-group areas between years, with equal-area aggregation/disaggregation and a similarity threshold in %. Several parcels can sit inside one îlot, which complicates sequences — [INRAE CIAG presentation](https://ciag.hub.inrae.fr/content/download/6088/45137?version=1)
- **ODR note on grassland in the RPG (2021).** Since 2010, a farm that receives any PAC aid must declare all its parcels, so unsubsidised grassland on aided farms is included. When sequences are built by overlaying campaigns, some parcels appear declared as **temporary grassland for more than 5 years**. ODR judges this negligible overall but possibly "frequent" locally — [ODR/INRAE, Les prairies dans le RPG](https://odr.inrae.fr/intranet/carto_joomla/index.php/ressource/documents/reseau-systeme-de-culture-systeme-de-production/rpg/3266-isop-contibution-odr-2021/file)

**European LPIS-based references (accuracy caveats)**
- **Netherlands (Friesland, BRP 2005–2021).** About 12 % of the study area was recorded as long-term grassland although it had been cropland in the previous 5 years. About 3,500 ha of recent grassland was misclassified as permanent or natural (about 15,000 ha cumulated over years). Long-term grassland was overestimated by 8 % in 2010. About 30 % of the area lacked registration in at least one year — [Craft et al. 2022, Frontiers in Env. Sci.](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2022.982925/full)
- **Flanders (Land 2023, 12(4):934).** Landsat land-cover series 2005–2019 were used to date grassland→arable conversion (grassland in 2005–2014, arable in 2015–2019), motivated by the lack of multi-annual LPIS information on grassland age — [MDPI Land 12/4/934](https://www.mdpi.com/2073-445X/12/4/934)
- **Canada (Yang et al., cited in Pouliot et al. 2021).** Change-vector analysis for grassland→cultivated conversion reached 89 % overall accuracy, but only 60 % producer's accuracy for the change class. Post-classification change from annual maps that are >80 % accurate "often results in low change accuracy" — [Pouliot et al. 2021, Remote Sens. 13(4):634](https://www.mdpi.com/2072-4292/13/4/634)

### Our reading
- For the datathon, the defensible "official-like" method is the Grand Est pairwise PP→TA flow, reported as two numbers: "strict" (PP→TA) and "upper bound" (+PP→PT +PP→Autre). This mirrors a published DRAAF approach the jury can recognise.
- The OSCOM-based 82/18 split mixes PP and PT and uses a different source from our RPG pipeline. Present it as context, not as a figure to reproduce.
- A Grand Est-like rate of about 1 %/yr would mean several thousand ha/yr of strict ploughing in Normandy. This is a plausibility check only: Normandy's reference ratio and grassland stock differ from Grand Est.

### Open points
- No Normandy-specific RPG-flow study (2015–2025) by DRAAF Normandie was found. Whether OSCOM is still published, and its current years, was not checked.
- The national SSP/Agreste method (Teruti, SAA) for grassland loss was not reviewed in detail.
- The RPG Explorer dataset page refused automated access, so file sizes, attributes and the minimum-area rule for smallest common parcels could not be read.
- No reported *accuracy* (against field truth) was found for RPG-based ploughing detection in France. Published studies give only caveats.

---

## 2. BCAE 1 rules, RPG structure and what they mean for detection

### In short
Under PAC rules, grassland becomes "permanent" after **five full years (the 6th declaration)**, *even if it was ploughed and re-sown in the meantime*. So a PP→PP sequence can hide a ploughing event, and PT that stays grass is administratively promoted to PP with no field change. The RPG has hard breaks:
- 2007–2014: îlots only, no parcel-level crop location.
- 2015 onward: parcels.
- 2022: no ID_PARCEL continuity with earlier years; ILOTS_ANONYMES removed.
- 2023: ILOTS_DE_REFERENCE added.

Parcel-ID tracking is therefore impossible, and the series must be matched geometrically.

### Sources
- **BCAE 1 definition (2025 fiche).** The grass period counts from five full years (6th PAC declaration onward). Any temporary grassland that is moved becomes permanent after five full years, even if ploughed and re-sown in between. The rule is managed collectively through a regional ratio: PP eligible area / total eligible area, compared each year with the 2018 reference ratio — [Télépac, Conditionnalité 2025, fiche BCAE 1](https://www.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2025/technique/Conditionnalite-2025_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf)
- **Thresholds since 2023.** A degradation >5 % of the reference ratio requires re-establishment of converted PP plus compensation. A degradation between 3 % and 5 % (2025 version) requires compensation grassland kept ≥5 years. **Normandy's 2018 reference ratio is 32.94 %.** For the 2025 campaign no region was under a regime, and 2026 will be assessed on the 2025 declarations — [Télépac BCAE 1 2025](https://www.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2025/technique/Conditionnalite-2025_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf)
- **2023 version.** >5 % meant a ban plus re-establishment; 2–5 % meant prior authorisation — [Télépac BCAE 1 2023](https://www.telepac.agriculture.gouv.fr/telepac/pdf/conditionnalite/2023/technique/Conditionnalite-2023_fiche-technique_BCAE1_maintien-prairies-permanentes.pdf). The arrêté of 31 Oct 2023 put Normandy at **−6.45 %**, the worst of the 4 regions with a drop (Grand Est −3.42 %, Bretagne −4.60 %, Pays de la Loire −5.20 %) — [Réussir](https://www.reussir.fr/lait/prairies-permanentes-4-regions-en-regime-dautorisation-ou-dinterdiction) (page no longer online). The exact regime applied to Normandy for 2024 was not confirmed.
- **History.** In 2017 Normandy's ratio degradation was 3.55 % (3.06 % in 2016), which put it under individual prior authorisation — [Terre-net, 2017](https://www.terre-net.fr/reglementation/article/132187/la-normandie-et-les-hauts-de-france-epingles-pour-retournement-excessif). Under the 2015–2020 greening rules, ploughing followed immediately by re-sowing grass was not a conversion — [DGPE note 2017 (Oise)](https://www.oise.gouv.fr/contenu/telechargement/40944/260309/file/20171113-Ratio%20PP%202017%20fiche%20r%C3%A9capitulative.pdf)
- **PP definition and coding.** PP are grass areas sown more than 5 years ago and not part of a crop rotation. PP is crop group 18 in the RPG (temporary grassland is a separate group) — [data.gouv RPG, to check](https://www.data.gouv.fr/datasets/rpg/discussions); [DataGrandEst record](https://dev.datagrandest.fr/geonetwork/srv/api/records/FR-25100157400010-2020-Evol10-19_PrairiesPerm_PnrFO). Code tables are in the IGN content description — [IGN DC_DL_RPG_2-0](https://geoservices.ign.fr/sites/default/files/2021-12/DC_DL_RPG_2-0.pdf)
- **2015 structural break.** Releases 2007–2014 contain only îlots. From 2015 they contain îlots and agricultural parcels, with the crop type at parcel level — [Ifremer Sextant RPG record](https://sextant.ifremer.fr/record/fbb08ca8-6246-9894-7934-b67d0db13770). Îlots are digitised at 1:5,000 on BD Ortho and updated yearly — [same](https://sextant.ifremer.fr/record/fbb08ca8-6246-9894-7934-b67d0db13770)
- **Later breaks.**
  - IGN's change log (SE_RPG) states no continuity of ID_PARCEL between the 2022 edition and earlier ones.
  - ILOTS_ANONYMES was removed from 2022 (v2.1).
  - ILOTS_DE_REFERENCE was added from 2023 (v2.2).

  Source: [IGN SE_RPG (to check; the URL now redirects to cartes.gouv.fr)](https://geoservices.ign.fr/sites/default/files/2025-11/SE_RPG.pdf)
- **Precomputed PP layer.** IGN distributes RPG 2025 and a dedicated permanent-grassland layer (IGNF_RPG_PRAIRIES-PERMANENTES_2025). The RPG 3.0 PP layer is history-based: a parcel is PP only after 5 consecutive years in grassland — secondary summaries of [cartes.gouv IGNF_RPG](https://cartes.gouv.fr/rechercher-une-donnee/dataset/IGNF_RPG) and [Lumière/monlumia](https://monlumia.fr/enr-identifiez-les-prairies-permanentes-pour-vos-projets/) (secondary source; exact WFS layer name not verified)
- **Release timing.** New vintages are usually released in Q4 — [data.gouv RPG discussion](https://www.data.gouv.fr/datasets/rpg/discussions)
- **Mass requalification in 2018.** It changed PT→PP massively with no field change; PP→PT conversions of about 350–400 ha/yr may correspond to re-seeding of degraded PP — [Agreste Grand Est 2022](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)

### Our reading
These are practical rules for our pipeline, derived from the above.

- **Count only PP(N) → arable(N+1)**, where arable means annual crops and excludes PT, fallow and leguminous forage. This avoids the classic false positive of temporary grassland rotating out.
- **Optional confirmation.** Require the parcel to be arable in N+2 as well, or arable in at least 2 of the next 3 years. This removes "PP→maize→re-sown grass" short break-ups, which are real ploughing but often reversible. Report a "persistent conversion" figure and a "ploughing event" figure separately.
- **PP→PT.** Report it as "re-sown or uncertain", not as conversion.
- **"PP→absent/non-agricultural".** Do not count it as ploughing. Cross it with OCS GE (§5) to see whether it was artificialised, and otherwise leave it as "left the PAC declarations".
- **Caveat to disclose: PP→PP hides ploughing plus re-sowing**, which BCAE permits and the RPG cannot see. Only remote sensing (§4) can catch it.
- **Starting the series in 2015.** Pre-2015 îlot data only give crop-group *areas per îlot*, not located parcels. Rasterising them would invent locations, so the RPG flow series should start in 2015, giving pairs 2015→2016 … 2024→2025. For 2010–2014, at most compare îlot-level grassland *shares* (an îlot whose PP share falls), and label it a different series.
- **No ID matching.** ID_PARCEL is not stable (explicitly broken in 2022, and parcels are redrawn yearly anyway), so the method has to be geometric: overlay, or rasterisation/grid.
- **2018 requalification spike.** Expect an artificial PT→PP spike in 2017→2018 and possibly other years. It does not affect a PP→TA count but does affect any "net PP stock" chart. Avoid net-stock charts or annotate them.

### Open points
- PAC code changes over 2015–2025 (e.g., new codes in 2023 under the new CAP) were not enumerated. The DC_DL RPG 2.x annex has to be checked per vintage.
- The exact definition, update rule and WFS name of the IGN "prairies permanentes" layer were not verified from primary IGN docs.
- The 2024 and 2026 Normandy BCAE regime was not confirmed.

---

## 3. How to compute it on the RPG

### In short
For about 845k parcels/year in Normandy, a pairwise **vector overlay restricted to PP(N) polygons** is tractable on a laptop with GeoPandas (STRtree) or DuckDB-spatial. Only about 30 % of agricultural area is PP, so only PP polygons in N need intersecting with all parcels in N+1. **Rasterisation to a 10–20 m grid** is the simplest robust alternative: redrawn boundaries stop mattering and it is directly compatible with HRL/OSO rasters. A ready-made option is the **RPG Explorer 2015–2024 crop-sequence GeoPackages**, already overlaid into common units.

### Sources
- Grand Est used a pairwise vector overlay N/N+1 and summed flows by zone — [Agreste Grand Est 2022](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)
- RPG Explorer overlays parcels across years into smallest common parcels and publishes departmental GeoPackages for 2015–2024 — [rpgexplorer.fr](https://rpgexplorer.fr/); [Recherche Data Gouv](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/6G0JTJ)
- **DuckDB spatial performance.** Bounding-box prefiltering (v1.2) and an in-memory R-tree (v1.3) cut a 58M-row × 310-polygon ST_Intersects join from about 1,800 s to about 30 s — [Simon Willison, Aug 2025](https://simonwillison.net/2025/Aug/23/spatial-joins-in-duckdb). The duckspatial R package reports about 50× faster spatial joins than sf on 1M points — [duckspatial benchmark](https://cran.nics.utk.edu/cran/web/packages/duckspatial/vignettes/benchmark.html). Users report that GeoPandas with an R-tree can be faster when data fit in memory — [duckdb_spatial issue #7](https://github.com/duckdblabs/duckdb_spatial/issues/7)
- No published head-to-head polygon *overlay* (ST_Intersection) benchmark at the million-polygon scale was found — [same search; see links above]
- **Cerema's approach to redrawn cadastral parcels.** CONSOENAF groups parcels that share the same original footprint even when split or merged between vintages, so it follows a stable perimeter. This is a useful analogy for RPG redrawing — [Cerema / data.gouv CONSOENAF 2011–2025](https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61)

### Our reading
Compute times here are our own estimates, not measured.

**A. Vector overlay (recommended for the "official-like" number)**
- Per pair (N, N+1): select the PP polygons of N (roughly 200–300k in Normandy), `gpd.overlay(pp_N, parcels_N1, how="intersection")` or DuckDB `ST_Intersection` with an `ST_Intersects` join, then classify the N+1 code and sum the area.
- Area not covered by any N+1 parcel = "absent from the RPG": compute it as PP area minus the summed intersections.
- Drop slivers below about 100–500 m², and below 5 % of the parcel area, to absorb digitising jitter from yearly redrawing.
- Rough budget: a few minutes to about 30 min per pair on a 16 GB laptop with GeoPandas 1.x/Shapely 2. That is about 10 pairs for 2015–2025, all doable in an evening. Run it per department to limit RAM.

**B. Rasterisation (robust and simple)**
- Rasterise each year's "class" (PP/PT/TA/other/absent) to a 10 m grid aligned to the HRL/OSO grid (EPSG:2154 or 3035) using `rasterio.features.rasterize`.
- Normandy is about 30,000 km², roughly 300M pixels at 10 m: about 300 MB per year as uint8, or about 19M pixels at 40 m.
- Transitions become a pixel-wise lookup. Then aggregate by EPCI with zonal statistics.
- Raster boundary error is about ±½ pixel, negligible at EPCI scale. Using 20 m reduces memory by 4×.

**C. Grid aggregation (H3 or 1 km INSPIRE / 200 m Insee grids)**
- Compute area per class per cell per year, then compare cell totals.
- Pitfall: this gives *net* change. A cell where one PP is ploughed and another PT becomes PP shows zero.
- Use grids only for **display** of results computed by A or B, not for detection.

**D. Shortcut**
- Use the RPG Explorer sequences for 14, 27, 50, 61 and 76. These already link the years 2015–2024, so you only need a code→class mapping and a PP→TA rule.
- Check the licence and attributes first. If its minimum unit or sliver rules are undocumented, say so.

**Tooling** (all open source): GeoPandas + pyogrio + Shapely 2, DuckDB spatial (reads GeoPackage/Parquet; `COPY … TO 'x.parquet'`), rasterio/rasterstats or exactextract for zonal stats, tippecanoe/PMTiles for tiles. In R: sf, terra, exactextractr, duckspatial.

**WFS caution.** Pulling about 845k features × 11 years through IGN WFS is slow and fragile (paging). Prefer the departmental GeoPackage downloads from IGN Géoservices / data.gouv for the processing run, and keep WFS for small checks. This affects how data is fetched, not the method.

### Open points
- No measured compute times for RPG-scale overlays were found. The team should benchmark one department-pair early (day 1–2).
- The RPG Explorer dataset's attributes and sliver threshold could not be read (access blocked).

---

## 4. Cross-checking with satellite products

### In short
The most useful precomputed product is the **Copernicus HRL Grasslands 2017–2024 suite** (10 m). It includes a yearly **Ploughing Indicator (PLOUGH)**, coded as years since the last ploughing or herbaceous disruption, plus Herbaceous Cover (HER) and the permanent Grassland mask (GRA). These can serve as an independent cross-check of RPG PP→TA flows without any image processing.

Its *change* accuracy is modest. The weighted user's accuracy of the "loss of grassland" class is about 49–56 %, and the 2018–21 weighted producer's accuracy is about 26 %. Status maps are about 97–98 % accurate, but the change layer is not.

Theia **OSO** confuses herbaceous classes with crops too much to be used for change detection. Direct ploughing detection (NDVI/bare-soil drops, Sentinel-1 coherence) works in research, but it is a research project in itself and not realistic as the core of a 3.5-week datathon. A small openEO sample check is feasible.

### Sources
**Copernicus HRL Grasslands (Product User Manual v2.6, 2025–2026)**
- **Layers.** HER (yearly, permanent and temporary grassland), GRA (permanent grassland), PLOUGH, GRAC (grassland change), mowing events and dates (GRAME/GRAMD), and confidence layers. Reference years are **2017–2024**. Resolution is 10 m, except GRAC at 20 m with a 1 ha MMU for the change classes. Delivery is Cloud-Optimised GeoTIFF on 100 km LAEA tiles (EPSG:3035) — [CLMS HRL Grasslands PUM](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **PLOUGH coding.** 0 = ploughing indicated in the current year; 1–6 = years since the last ploughing indication; 100 = change in herbaceous cover; 253 = no ploughing information. It tracks the time since the last time the pixel was not covered by herbaceous vegetation — [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **GRA definition.** Stable, continuously herbaceous vegetation for at least 6 years with no ploughing. All herbaceous areas with ploughing or disruption in the current or previous five years are masked out. The manual says this follows the CAP 5-year convention. The MMU was removed from PLOUGH and GRA in the current cycle, so small differences from historic layers may be artefacts — [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **Accuracy, status.**
  - GRA overall accuracy (EU27, weighted) is 98.5 % (2018), 98.6 % (2021), 98.7 % (2022) and 97.6 % (2024).
  - Grassland-class user's accuracy is about 90.6–97.6 % and producer's accuracy about 93–95 %.
  - EEA38 overall accuracy is about 97.2–97.4 %.

  Source: [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **Accuracy, change (GRAC).**
  - 2018–2021, EU27, weighted: OA 99.2 %, but "loss of GRA" user's accuracy is **55.5 %** and producer's accuracy **25.8 %**.
  - 2021–2024, weighted: loss user's accuracy is **49.0 %**.
  - The manual notes that assessing rare change classes "remains challenging" and that some sub-classes fail the 80 % threshold.

  Source: [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file). (Values come from the extracted tables; the column alignment of the producer's accuracies is partly uncertain.)
- **Targets.** 85 % OA for status layers and 80 % OA for change layers, validated on the LUCAS 2 km grid with extra change-stratum samples — [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **Access.** WEkEO/CLMS host "Ploughing Indicator 2017–present (raster 10 m)" — [WEkEO help](https://help.wekeo.eu/en/articles/16540530-hrl-datasets-transition-how-to-access-croplands-grasslands-and-tree-cover-data). The HER layer is harmonised with the HRL Croplands into an EU agricultural land-use systems dataset — [Nature Sci. Data 2026](https://www.nature.com/articles/s41597-026-07374-1)

**Theia OSO**
- OSO is an annual 10 m land-cover map of France from Sentinel-2 with a random-forest classifier. It has had 23 classes since 2018, and the vector version uses a 0.1 ha MMU — [CNES Geodes OSO](https://geodes.cnes.fr/projects/oso-occupation-des-sols-raster-l3b/); [Theia OSO 2020 product sheet](https://www.theia-land.fr/wp-content/uploads/2024/05/FicheProduit_2020-OSO.pdf)
- **Herbaceous-class accuracy.** An independent assessment of the 2023 map found 30.7 % of reference natural herbaceous vegetation classified as annual crops. That class had UA 0.541, recall 0.278 and F1 0.366 (the weakest class). Annual crops had F1 0.884, and OA was 79.5 % ± 1.4 % — [Cahiers Agricultures 2026](https://www.cahiersagricultures.fr/articles/cagri/olm/2026/01/cagri250200/cagri250200-1-olm.pdf). The ODR note on the "RPG complété" says using OSO alone for such parcel tasks would be "very delicate and uncertain" — [ODR RPG complété](https://odr.inrae.fr/intranet/carto_joomla/index.php/ressource/documents/documents-odr/notes-methodologiques/3213-note-methodologique-rpg-complete-2014/file) (to check)

**Direct remote sensing of ploughing**
- **Czech Republic.** A random forest on Sentinel-2 biophysical time series (FAPAR, canopy water content and LAI were best) detected permanent-grassland→arable change with >95 % accuracy over 8,766 km² — [Šandera & Štych 2020, Land 9(11):420](https://www.mdpi.com/2073-445X/9/11/420). An AutoML follow-up (H2O) reported OA of 93.5–96.6 % — [Eur. J. Remote Sens. 2024 (DOAJ)](https://doaj.org/article/ad2dfb4e8dda4a7bb271cc8356cc529a)
- **Sen4CAP (ESA).** Bare-soil periods and parcel-level changes between permanent grassland, permanent crop and annual crop are detected with thresholds on S-2 NDVI, NDTI, NDMI and FCOVER, confirmed by S-1 time series — [ESA Sen4CAP extension report](https://eo4society.esa.int/wp-content/uploads/2024/04/agriculture-virtual-laboratory-ccn-1-sen4cap-extension.pdf)
- **Ireland (EU Big Data Hackathon 2025).** Bare land was defined as parcel NDVI < 0.25. Parcels converted from grassland showed +50 % bare-day observations. Cloud cover was an issue, and the team noted the HRL already captures ploughed pixels — [Ireland slide deck](https://cros.ec.europa.eu/system/files/2025-03/15_IE_EU%20BigData%20Hackathon2025_slide%20deck_Final_IRELAND.pdf) (to check)
- **Slovenia (2026).** A machine-learning "Bare Soil Marker" on S-2 + Landsat (2000–2021) found about 98 % of permanent grassland unchanged, with regional losses up to 5 % — [Zenodo 20395603](https://zenodo.org/records/20395603). No accuracy figure was found.
- **Estonia, Sentinel-1.** Six-day S-1 coherence rises after both mowing and ploughing, with different dynamics. After ploughing, VV coherence reached about 0.65 and VH about 0.45 while NDVI was about 0.2 — [Remote Sens. 2020, 12(22):3784](https://www.mdpi.com/2072-4292/12/22/3784). Separability of mowing and ploughing on short-baseline coherence was studied by Aalto — [Aalto research portal](https://research.aalto.fi/en/publications/separability-of-mowing-and-ploughing-events-on-short-temporal-bas/). No standalone ploughing accuracy was found.
- **Mowing detection as a proxy for algorithm difficulty.** Sen4CAP S-1+S-2 achieved F1 ≈ 0.79 across 7 countries, but an independent Wallonia validation found F1 0.58. Germany-wide F1 was 0.55–0.74, and events near cloud gaps were missed — [RSE 2022, Mowing detection S1/S2](https://www.sciencedirect.com/science/article/abs/pii/S0034425722002590); [PMC8770799](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8770799/); [ResearchGate, Germany](https://www.researchgate.net/publication/356548630_Mapping_grassland_mowing_events_across_Germany_based_on_combined_Sentinel-2_and_Landsat_8_time_series)
- **Small parcels.** Parcels below about 0.2 ha that are narrow or irregular are hard to detect — [EUSPA resource (to check)](https://euspa-dev.drupal-y.eworx.gr/node/6819)

**Compute platforms**
- **openEO on Copernicus Data Space Ecosystem (CDSE).** There is a free monthly credit allowance, but sources conflict: 4,000 credits/month (raised from 3,000) vs 10,000 (possibly a temporary boost). Synchronous requests cost about 6–7 credits and batch jobs carry startup costs. Aggregating statistics over many polygons is a core feature — [CDSE credit usage](https://documentation.dataspace.copernicus.eu/APIs/openEO/credit_usage.html); [CDSE forum](https://forum.dataspace.copernicus.eu/t/clarification-on-openeo-free-tier-credit-calculation-unexpected-quota-exhaustion/5037); [CDSE NDVI time-series notebook](https://documentation.dataspace.copernicus.eu/notebook-samples/openeo/NDVI_Timeseries.html)
- The JRC "CbM" parcel time-series API is another parcel-statistics option — [JRC CbM docs](https://jrc-cbm.readthedocs.io/en/latest/api_time_series.html)

### Our reading
- **Realistic role for remote sensing in the datathon is validation and confirmation, not primary detection.**
  - (a) Download only the HRL PLOUGH and GRA tiles covering Normandy. That is about 4–6 LAEA 100 km tiles per year, COGs readable by windowed access. This is a one-off and modest in size, but it is still a download, so check volume first.
  - (b) For each RPG PP→TA parcel or pixel in year N+1, check whether PLOUGH = 0 in N or N+1. This gives an "RPG and satellite agree" rate.
  - (c) Map RPG-PP pixels that HRL flags as ploughed but where the RPG still says PP. These are candidates for ploughing plus re-sowing hidden by declarations.
- **HRL time window.** HRL covers 2017–2024 only, so validation is limited to the RPG pairs 2017→2018 … 2023→2024.
- **Do not treat HRL GRAC "loss" as truth.** Its user's accuracy is only about 50 %. Use agreement statistics rather than claiming accuracy.
- **OSO** is unsuitable for herbaceous change. At most it can be used as visual context.
- **Direct NDVI/bare-soil detection.**
  - Feasible as a **sample check**: e.g., 200–300 random PP→TA parcels and 200–300 PP→PP parcels.
  - Pull median NDVI per parcel per 10-day period through openEO `aggregate_spatial` on CDSE, or Google Earth Engine under non-commercial terms. A bare-soil event is NDVI < about 0.25 over 2+ clear dates between autumn N and spring N+1.
  - This fits in the free credits. Region-wide parcel time series for about 250k PP parcels × several years would likely exceed free quotas and the time available.
- **Sentinel-1 coherence** is the most cloud-robust signal (relevant to Normandy's cloudiness), but it is too complex to process for this timeframe.

### Open points
- No France-specific accuracy of HRL PLOUGH was found. The PUM validates GRA and GRAC, not PLOUGH directly.
- Exact Normandy tile list and file sizes for HRL were not checked.
- The current CDSE free-tier credit figure is unconfirmed because sources conflict.
- No published per-class OSO "prairies" F-score for 2022/2023 was retrieved; the Theia validation report was not reached.
- Google Earth Engine non-commercial quota specifics were not researched.

---

## 5. Combining with OCS GE and CONSOENAF without double counting

### In short
The two processes must be counted on a **single, mutually exclusive land-accounting basis**, with a priority rule: **artificialisation takes precedence over ploughing**. Any area that OCS GE flags as artificialised between its two vintages is removed from the RPG ploughing count for overlapping years, even if it passed through "arable" or "absent from the RPG" first. Because OCS GE vintages differ by department (2019→2022 vs 2020→2023), the cleanest move is to express everything as **mean ha/yr over each department's own OCS GE interval**. Then sum EPCIs, with an explicit "period" label, rather than forcing a common calendar.

### Sources
- **OCS GE.** For each department produced, IGN delivers two vintages plus the differential between them. The differential (v1.1) is the reference for computing artificialisation — [IGN webinar OCS GE, Nov 2025](https://artificialisation.developpement-durable.gouv.fr/sites/artificialisation/files/inline-files/20251113_webinaire_OCSGE_pour_diffusion.pdf); [OPenIG IGN presentation, Dec 2025](https://www.openig.org/sites/default/files/2025-12/4A_Pre%CC%81sentation_OCSGE_IGN.pdf). As of 16 June 2025, 94 departments had been distributed — [same](https://www.openig.org/sites/default/files/2025-12/4A_Pre%CC%81sentation_OCSGE_IGN.pdf)
- **Artificialised status.** Each cover × use combination (CS × US) gets its status from a crossing table translating décret n° 2023-1096. Cultivated land counts as non-artificialised under the Code de l'urbanisme — [data.gouv OCS GE Artificialisation](https://www.data.gouv.fr/datasets/ocs-ge-artificialisation/informations)
- **CONSOENAF (Cerema)** is based on the Fichiers fonciers (DGFiP tax data at 1 January each year). It compares consecutive vintages as flows and groups split or merged parcels into stable footprints. Annual flows are available 2011→2025. Ambiguous spaces (golf courses, quarries, rural paths) are classified inconsistently across sources — [CONSOENAF 2011–2025, data.gouv](https://www.data.gouv.fr/datasets/6a01b9280dd2d45907e5fc61); [Cerema webinar 2023](https://artificialisation.developpement-durable.gouv.fr/sites/artificialisation/files/inline-files/2023_09_01_WebinaireConso_Methode.pdf)
- **Overlap between grassland loss and artificialisation.** Grand Est notes that part of the "disappeared" PP (left the PAC or became non-agricultural) eventually feeds artificialisation as building land or non-agricultural activity zones — [Agreste Grand Est 2022](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf). In Normandy OSCOM, 18 % of grassland/agricultural-land loss went to artificialisation in 2008–2019, 6–29 % depending on department — [Agreste Normandie 2021](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)

### Our reading
**Recommended accounting**, done spatially and pixel- or polygon-exclusive.

1. **Define the window per department** as the OCS GE interval [t0, t1], e.g. 2019→2022 or 2020→2023.
2. **Artificialisation A** = OCS GE differential polygons flagged non-artificialised → artificialised within [t0, t1]. Split A by the t0 cover/use (agricultural herbaceous vs crop vs forest, etc.), and also by RPG status in year t0 (PP / PT / TA / not declared) via overlay.
3. **Ploughing P** = Σ over RPG pairs inside [t0, t1] of PP(N)→TA(N+1) areas, **minus any part intersecting A**. Artificialisation wins.
   - Count each location at most once per window. Union the PP→TA geometries across pairs before summing, so a parcel ploughed, re-sown and ploughed again is not counted twice.
   - Optionally require the parcel to still be TA at t1.
4. **Indicator** "ce que le béton et la charrue ont pris" = A_grass (artificialised land that was RPG-PP, or OCS GE herbaceous, at t0) + P. Report the components separately (stacked bar), plus a "left the PAC, fate unknown" grey component that is not added.
5. **Annualise** as (A + P) / (t1 − t0) ha/yr per EPCI.
   - For EPCIs straddling two departments (with different OCS GE windows), compute each part with its own window, sum the ha/yr, and flag "période mixte".
   - Use CONSOENAF only as the longer-period (2011–2025) context series for artificialisation. **Do not add CONSOENAF to OCS GE**: they measure overlapping phenomena with different definitions (cadastral consumption vs land-cover artificialisation).
6. **Reference denominators.** Use per-EPCI PP stock at t0 from the RPG, so you can display "% of permanent grassland lost per year". This is comparable to the Grand Est ≈1 %/yr and to the BCAE ratio logic.

### Open points
- The exact OCS GE vintages for Normandy departments were taken from our project notes (2019/2022 vs 2020/2023). IGN's naming in late 2025 lists layers as OCSGE.ARTIF.2016-2017 (M0), 2017-2020 (M1) and 2021-2023 (M2), which does not obviously match — [OPenIG IGN presentation](https://www.openig.org/sites/default/files/2025-12/4A_Pre%CC%81sentation_OCSGE_IGN.pdf). Verify per department on Géoservices.
- The CS2.2.1 × US1.1 status in the décret crossing table was not retrieved.

---

## 6. Validation and expected accuracy

### In short
Validation has three layers:
- (i) **internal consistency**: reproduce the Grand Est-style flow table and check that Normandy rates are of the right order;
- (ii) **independent cross-check** with HRL PLOUGH/GRA;
- (iii) **a small manual photo-interpretation sample** (IGN BD ORTHO / historic orthophotos, Sentinel-2 browser) to estimate a commission rate with a confidence interval.

Realistically, expect the "strict" RPG PP→TA count to be a good *lower bound* for persistent conversion, with false positives mainly from code errors and sliver artefacts. Expect satellite change products to agree only partially, since loss user's accuracy is about 50 % in HRL.

### Sources
- HRL change validation uses stratified samples on the LUCAS grid with change strata added, because changes are rare. That is the design we should use: stratify by "RPG says ploughed" vs "RPG says stable" — [CLMS HRL Grasslands PUM](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- Accuracy reporting for change should follow good practice (area-adjusted estimates with CIs; Olofsson et al. 2013 is cited in the HRL PUM) — [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file)
- **Change-detection pitfalls.**
  - High OA with low change-class accuracy appears in HRL (OA 99 % vs loss UA 49–56 %) — [same](https://land.copernicus.eu/en/technical-library/product-user-manual-grasslands-2017-present/@@download/file).
  - Yang et al. (Alberta) reported OA 89 % but change producer's accuracy of 60 % — [Pouliot et al. 2021](https://www.mdpi.com/2072-4292/13/4/634).
- **LPIS administrative error rates** can be large: about 12 % of the area was misclassified as long-term grassland in Friesland — [Craft et al. 2022](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2022.982925/full)
- A research-grade S-2 classifier reached >95 % for PP→arable in Czechia, giving an upper benchmark for what a dedicated remote-sensing pipeline can achieve — [Šandera & Štych 2020](https://www.mdpi.com/2073-445X/9/11/420)

### Our reading
**Minimal validation protocol** (about 1–1.5 person-days):
- Draw 100 random PP→TA patches (> 0.5 ha) and 100 PP→PP patches, stratified by department.
- Two team members label each patch on ortho or Sentinel-2 imagery: ploughed / not ploughed / uncertain.
- Report the commission rate (share of PP→TA not actually ploughed) with a 95 % Wilson interval. With n = 100, the interval is about ±6–10 points.
- Compute RPG vs HRL agreement on all PP→TA area for 2017–2024: the % of PP→TA area with PLOUGH = 0 in N or N+1.
- Sanity checks:
  - The per-year Normandy PP→TA rate should sit in the same order as Grand Est (≈1 %/yr) and be consistent with the BCAE ratio degradation of −6.45 % vs 2018 (2023).
  - Department totals should be consistent with the OSCOM pattern of strongest arable conversion in the Manche/Orne/Calvados dairy areas.
  - There should be no artificial spike in 2017→2018 for PP→TA. A spike in PT→PP is expected.

### Open points
- No published accuracy of RPG-based PP→TA flows against field truth in France was found. Any accuracy claim will be our own sample estimate.

---

## 7. Display rules, sobriety and minimum viable version

### In short
Publish **EPCI-level** (and at most commune- or grid-level) aggregates, never parcel polygons coloured by "ploughed". Show uncertainty as ranges ("strict" to "upper bound") plus an RPG/HRL agreement score. Precompute everything offline. The web product should ship a small JSON (one record per EPCI, about 70 EPCIs in Normandy) plus, optionally, one PMTiles file of an aggregated grid. A minimum viable version is achievable in about 6–9 person-days.

### Sources
- **Precedent for confidentiality.** The Agreste Normandie study shows results only as a smoothed 1 km² hexagon surface (7.5 km radius) and commune maps above a 1 ha/km² threshold, not parcels — [Agreste Études n°6](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- RPG public releases are anonymised by the ASP before IGN distributes them — [Ifremer Sextant RPG record](https://sextant.ifremer.fr/record/fbb08ca8-6246-9894-7934-b67d0db13770)
- Grand Est published flows aggregated by zone and notes that its results are not the regulatory ratio — [Agreste Grand Est 2022](https://draaf.grand-est.agriculture.gouv.fr/IMG/pdf/2022-03-prairies_permanentes.pdf)

### Our reading
**Display rules**
- **EPCI as the main unit.** Commune as a drill-down, only if area ≥ a threshold (e.g., ≥ 5 ha ploughed and ≥ 3 distinct parcels in the period; otherwise show "< seuil").
- If you add a map texture, use a 1 km or 2 km grid (INSPIRE/Insee) or kernel smoothing like Agreste, never parcel outlines. Even anonymised, parcel-level "this field was ploughed" maps can be cross-referenced with the Télépac or cadastre context.
- **Uncertainty.** Show bars with three stacked parts: strict PP→TA (solid), PP→PT plus "left the PAC" (hatched, "upper bound"), and artificialisation of grassland (another colour). Add a badge for satellite agreement (%) and the sample-based commission rate.
- Label every figure with its period ("2019–2022, Calvados OCS GE window").
- Avoid net-stock charts of PP, which are distorted by the 2018 requalification.
- **Wording.** "ploughed according to PAC declarations" rather than "destroyed". PP→TA ploughing can be legal under BCAE when ratio thresholds are not exceeded.

**Digital sobriety**
- Do all GIS work offline (Python/DuckDB) and publish only:
  - `epci_indicateurs.json`: about 70 EPCIs × ~10 fields × ~10 periods, under 100 KB gzipped;
  - one simplified EPCI boundary file (TopoJSON or PMTiles, a few hundred KB after simplification);
  - optionally one `grid_2km.pmtiles` (Normandy is about 30k km², so about 7.5k cells, < 1 MB).
- No WFS calls from the client and no raster tiles. A static site (no server) with PMTiles via HTTP range requests in MapLibre. Precompute charts as data, not images.
- Document the processing energy (one laptop, a few hours) as a sobriety argument versus cloud remote sensing.

**Recommended MVP** (our own estimates; team of 3, about 3.5 weeks)
1. **Days 1–2 (1 person).** Get RPG 2015–2025 GeoPackages for the 5 departments, or the RPG Explorer sequences. Build the code→class table (PP / PT / TA / fallow / other) from the IGN DC_DL annexes, following the Grand Est Annexe 1 logic. Benchmark one pair.
2. **Days 3–5.** Pairwise PP(N)→class(N+1) overlay for all 10 pairs: area by EPCI and year for strict, PP→PT and absent. Add the "persistent" variant (still TA at N+2).
3. **Days 5–7.** OCS GE differential overlay with the precedence rule; annualisation per department window; the combined indicator.
4. **Days 7–9 (parallel, 1 person).** HRL PLOUGH cross-check for 2017–2024 (tiles for Normandy only) and the 200-patch photo-interpretation sample.
5. **Days 9–12.** JSON export, PMTiles, front-end charts with uncertainty, and the methods page listing caveats: 2015 break, ID break in 2022, the 5-year rule, ploughing plus re-sowing invisible, the PAC-coverage gap, and the 82/18 figure coming from OSCOM.
- **Stretch goals.** An openEO NDVI bare-soil check on a few hundred parcels. Îlot-level 2010–2014 grassland-share trend as a separate, clearly labelled series.
- **Not recommended within 3.5 weeks.** Region-wide S-1/S-2 ploughing detection, or OSO-based change.

### Open points
- No official guidance was found on a minimum aggregation threshold for publishing RPG-derived results; the threshold above is a proposal. Agreste's statistical-secrecy rules (e.g., the ≥3 holdings rule used for agricultural statistics) were not verified for RPG-derived maps.
- The number of EPCIs in Normandy (about 70) is approximate and should be checked against the current Banatic/INSEE list.
