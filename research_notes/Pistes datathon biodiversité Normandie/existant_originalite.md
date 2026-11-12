# Existing tools, studies and past projects vs. the candidate pistes A–N: an originality assessment for Datathon Normandie 2026

Normandy first, then France, then Europe for comparison. Each piste section gives the closest existing equivalents, what a team could add, and an originality rating. Figures marked \"(to check)\" come from documents we could not open in full. The remaining gaps are listed at the end.

---

## Piste A: Friches → Nature (ranking the EPF Normandie brownfields by renaturation potential)

### In short
The core of this piste already exists. Cerema's **Cartofriches** computes a **"mutability index" that includes a renaturation index** for every brownfield without a project nationwide. Its inputs include ZNIEFF, Natura 2000 and nature-reserve zonings, the green-blue infrastructure (TVB), natural risks, tree cover from OCS GE, and an OFB/Cerema "ecological gain potential". The **EPF Normandie observatory** also has a per-site decision-support tool that suggests vocations, renaturation among them. Originality is low to medium.

### Sources
- **Cartofriches mutability indices.** One index is proposed for each of 6 reconversion types: residential, public facility, tertiary, industrial, **renaturation** and ground-mounted PV. It covers **all brownfields without a project**, and is not computed for sites that already have a project or have been reconverted. 22 indicators are computed automatically, including TVB (from the Géoportail de l'urbanisme), environmental zonings (Géoportail de l'urbanisme + INPN), natural and technological risks, plant cover (OCS GE), soil pollution (local observatories + SIS) and "potentiel de gain écologique" (the POGEIS method developed by OFB and Cerema). 6 indicators are entered by the user only, among them **presence of a wetland** and **presence of a protected species**. 3 more can be corrected by the user. — [Cerema, "Les indices de mutabilité" documentation](https://doc-datafoncier.cerema.fr/doc/export/511)
- **Renaturation scoring rules in that documentation:**
  - Nature reserve: "très positif". Natura 2000 or ZNIEFF: "positif". Within 5 km of a zone: "positif" (weight 1).
  - TVB present: "très positif" (weight 1).
  - Strong POGEIS ecological gain: "très positif" (weight 2).
  - Strong natural risk: "très positif".
  - Woody vegetation: "très positif".
  - Wetland present, or protected species present (both user-entered): "très positif".
  - N or A zoning: "très positif".
  - Proven pollution: neutral for renaturation. — [Cerema documentation](https://doc-datafoncier.cerema.fr/doc/export/511)
- **Cartofriches as of March 2026:** it aggregates **27 local observatories** (+2 being added), about **72,000 ha** of brownfields, and adds more than 30 variables computed by Cerema (ZNIEFF/Natura 2000/RN zonings, OCS GE cover, risks, POGEIS potential, etc.). The mutability method was adapted from work by the Ardennes DDT and ADEME's **Mutafriches**, and is documented at cartofriches.cerema.fr/?mutabilite. The surrounding ecosystem includes UrbanSIMUL and **UrbanVitaliz** (Cerema), ADEME's **Mutafriches/Bénéfriches**, the Fonds vert and Friches+ (Banque des Territoires). — [Cerema slides, CPDT colloquium, 14 Apr 2026](https://cpdt.wallonie.be/wp-content/uploads/2026/02/3_CEREMA-Cartofriches-Olivier-Dupre.pdf)
- **National inventory 2026 (published 3 Sept 2026):** 20,250 brownfields as of 1 July 2026. The lead gives about 61,000 ha, while the body gives 115,000–155,000 ha, so the article is internally inconsistent. Of about 1,700 brownfields already reconverted, only 50 (about 3%) became green spaces. For the ~13,200 sites without a project, Cerema's estimate of likely uses is 58% housing, 35% industry, 7% other. — [Banque des Territoires/Localtis](https://www.banquedesterritoires.fr/plus-de-20000-friches-recensees-en-2026-selon-linventaire-national-publie-par-le-cerema)
- **Inventory 2025:** 15,000 sites and ~60,000 ha. Cerema estimated that 18% of brownfields without a project (~1,500 sites) could be candidates for renaturation; the method is not stated. — [Banque des Territoires, 22 Sept 2025](https://www.banquedesterritoires.fr/inventaire-national-des-friches-2025-60000-hectares-de-foncier-recenses)
- **EPF Normandie "Observatoire des friches normandes":** developed by EPFN with the State and the Région under the Climate & Resilience law. It lists about **5,100 brownfields / 3,319 ha**. Each site has a detailed sheet (typology, constraints, projects) and a **decision-support tool on possible vocations (economic activity, housing, tourism, renaturation)**. About 270 sites were updated since early 2026. — [COP Normandie "Info COP" (to check)](https://www.prefectures-regions.gouv.fr/irecontenu/telechargement/141551/1029345/file/Info%20Cop)
- EPFN brownfields are also republished as open data, e.g. for the Orne (updated 10 Mar 2026). — [data.gouv.fr](https://www.data.gouv.fr/datasets/friches-issues-de-l-epfn-dans-lorne-en-2026)
- **Île-de-France analogue:** the REGREEN method and the "Où renaturer en Île-de-France" map (ARB ÎdF + Institut Paris Region, 2022) found ~30,535 ha of mineral surfaces that could be renatured (2.54% of the region). Of these, ~7,017 ha would bring a clear benefit for biodiversity, climate and health. — [Institut Paris Region, Note rapide 966](https://data.iau-idf.fr/fileadmin/NewEtudes/000pack3/Etude_2865/NR_966_web.pdf). Institut Paris Region also advertised work on a GIS analysis of the ecological potential of the brownfields in its own observatory, sorting them into build / renature / protect; publication of results was not confirmed. — [job posting](https://listes.georezo.net/hyperkitty/list/job@ml.georezo.net/message/2XN6NVXQMV3HED3KF2QLEDZ4JSXV66A4/)
- Cerema mission for the La Rochelle agglomeration (2024–2025): it adapted the ARB ÎdF method to find priority zones and then the sites with the highest renaturation potential, partly based on mutability. — [Cerema](https://www.cerema.fr/fr/print/pdf/node/15866)
- **Regulatory hook:** SCoTs can delimit **"zones préférentielles pour la renaturation" (ZPR)** in their DOO, and PLU(i)s can do so through OAPs and zoning. — [Banque des Territoires](https://www.banquedesterritoires.fr/lutte-contre-lartificialisation-des-sols-vers-des-zones-de-renaturation-preferentielle-dans-les); [nature-en-ville.com](https://www.nature-en-ville.com/print/pdf/node/1870). The FédéSCoT guide "Renaturer" (2024) gives a method: "carte verte" diagnosis, crossing of stakes, objectives under ZAN, then arbitration. — [FédéSCoT](https://www.planif-territoires.logement.gouv.fr/IMG/pdf/fedescot-renaturer.pdf)

### Our reading
- A "renaturation potential score per brownfield" largely re-implements Cartofriches (national, and probably fed by EPFN data) and EPFN's own tool. Experts from EPFN, DREAL or the Région would likely spot this immediately.
- **What a team could add:**
  1. A **regional comparative ranking** of all ~5,068 sites with transparent, adjustable weights. Cartofriches gives qualitative per-site indices, not a Normandy-wide shortlist.
  2. **Automatic computation of the criteria Cartofriches leaves to users or omits:** potential or effective wetlands, protected-species proximity (OpenObs), floodplain, distance to SRADDET reservoirs and corridors, and the brownfield's **contribution to connectivity** (graph metric).
  3. **Cluster/network logic:** groups of brownfields that would reconnect a corridor if renatured together.
  4. **Benchmarking** of the EPFN, Cartofriches and team scores, with disagreements flagged.
  5. Outputs packaged as **ZPR candidates per SCoT/PLUi**, the planning act where this information is needed.
- Renaturation is still marginal in practice (3% of reconversions nationally), so a "renaturation pipeline" framing fits the theme. The differentiator would be the ecological depth and the territorial prioritisation, not the scoring itself.

### Open points
- EPFN's decision-tool method and URL were not found. Whether EPFN data are among Cartofriches' 27 observatories is likely but unverified.
- The POGEIS method and the Mutafriches/Bénéfriches pages were not read directly.
- Whether Cartofriches' open-data export includes the mutability indices was not checked.

### Originality
**LOW–MEDIUM.** Renaturation scoring of brownfields from ecological zonings, TVB, risks and pollution is already built into Cartofriches (national) and EPFN's tool (regional). Originality would only come from a regional network-level prioritisation with richer automated ecological criteria and outputs geared to ZPR.

---

## Piste B: Multi-criteria restoration priority map (score = stakes × degradation/pressure × opportunity, adjustable weights)

### In short
No public, interactive, weight-adjustable restoration-priority map for Normandy at 1 km or commune scale was found. Regional restoration priorities do exist, in the SRADDET TVB ("secteurs d'actions prioritaires", "corridors d'intérêt régional à restaurer"). The regional TVB map is being remodelled in 2026, with a new dark-sky network (trame noire). ANBDD publishes fragmentation indicators per EPCI. National and EU priority mapping is under way: the Nature Restoration Regulation, France's draft national restoration plan, and NaturaConnect. Originality is medium.

### Sources
- **Normandy SRADDET:** a regional TVB with reservoirs and corridors, plus **"secteurs d'actions prioritaires"** and **"corridors écologiques d'intérêt régional à restaurer"**. The SRADDET plans online diffusion (e.g., Géonormandie) so that maps can be updated without revising the SRADDET. — [Région Normandie, AAP Travaux TVB 2026 (to check)](https://rn136.normandie.fr/sites/default/files/2025-12/aap_travaux_tvb_2026_vf.pdf); [SRADDET annexes 4, 29 Mar 2024](https://www.prefectures-regions.gouv.fr/normandie/irecontenu/telechargement/117234/874029/file/2024-03-29%20(DT)%20-%20SRADDET%20annexes%204.pdf)
- **Regional call for TVB restoration works 2026** (FEDER 2021–2027, specific objective 2.7), open 1 Dec 2025–15 Apr 2026 (now closed). It funds habitat restoration, functional corridors, resolving breaks at infrastructures, and preliminary studies (rivers, pond networks, hedgerow mesh, wildlife crossings). — [Région Normandie (to check)](https://rn136.normandie.fr/sites/default/files/2025-12/aap_travaux_tvb_2026_vf.pdf)
- **Ongoing study: "Mise à jour de la cartographie de la trame verte et bleue normande et identification de la trame noire régionale".** A note dated **11/06/2026** accompanies a QGIS project of modelling results and zonings; the method starts from sub-networks and associated species guilds. No published results were found. — [normandie-a-la-carte.normandie.fr note (to check)](https://normandie-a-la-carte.normandie.fr/tvb/tvb_note_accompagnement_donnees.pdf)
- **Stratégie régionale pour la biodiversité (SRB) Normandie 2030**, voted 17 Oct 2022: 6 strategic challenges and 56 operational objectives, including "100% of Normandy EPCIs have a TVB action plan by 2030". — [SRB objective sheets (to check)](https://rn136.normandie.fr/sites/default/files/2023-05/srb-normandie-fiches-objectifs.pdf). The CESER found its protection targets clearly less ambitious than the national protected-areas strategy (SNAP). — [CESER opinion](https://ceser.normandie.fr/sites/default/files/2024-04/7%20Avis%20STRATEGIE%20REGIONALE%20POUR%20LA%20BIODIVERSITE%20NORMANDIE%202030.pdf)
- DREAL Normandie maps potential biodiversity restoration sectors locally, e.g. on the banks of the Orne and the Caen–sea canal. — [DREAL Normandie (to check)](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/rives_de_l_orne_et_canal_de_caen_a_la_mer.pdf)
- ANBDD's EPCI indicator app includes **"Fragmentation des espaces naturels et semi-naturels terrestres"** and **"Fragmentation des cours d'eau"**. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **EU Nature Restoration Regulation (EU 2024/1991)**, in force 18 Aug 2024: restoration measures on at least 20% of EU land and sea by 2030, and on all ecosystems in need by 2050. — [ERA Malta summary](https://era.org.mt/topic/nature-restoration-regulation/). The Commission adopted a standard national restoration plan template, developed with the EEA, to guide Member States in **identifying and mapping areas for restoration**. — [NetworkNature](https://networknature.eu/networknature/article/commission-adopts-standardised-tool-support-national-restoration-plans-across-eu)
- **France's plan "Agir pour la restauration de la nature":**
  - national consultation until 31 July 2026; first version due to the Commission before 1 Sept 2026;
  - an arrêté of 27 Aug 2026 (JO 3 Sept 2026) subjects it to environmental assessment by the IGEDD Ae;
  - planned next steps: Commission comments Feb 2027, final adoption Aug 2027, revisions 2032 and 2042.
  - Sources: [AIDA/INERIS, arrêté](https://aida.ineris.fr/node/46395); [DREAL Corse presentation (to check)](https://www.corse.developpement-durable.gouv.fr/IMG/pdf/23_06_presentation_rrn.pdf); [OFB article](https://ofb.gouv.fr/sites/ofb-gouv-fr/files/2026-04/biodiversite-ndeg11-article-rrn.pdf)
  - Formal submission to Brussels was not confirmed.
- **NaturaConnect** (Horizon Europe, July 2022–June 2026, IIASA-led) does spatial prioritisation for the Trans-European Nature Network: corridor-priority maps and protected-area gaps. — [EUROPARC](https://www.europarc.org/horizoneurope-naturaconnect/); [IEEP](https://ieep.eu/news/establishing-a-true-coherent-trans-european-nature-network/). Spatial priority maps built on NaturaConnect (Nature-3B project) were published on Zenodo in Feb 2026, with **files embargoed until 31 Dec 2026**. — [Zenodo](https://zenodo.org/records/18699015)
- **Global reference:** Strassburg et al. 2020 (Nature 586:724–729) used a multicriteria optimisation to map restoration priorities. Restoring 15% of converted lands in priority areas could avoid 60% of expected extinctions and sequester 299 Gt CO2. — [WUR record](https://research.wur.nl/en/publications/global-priority-areas-for-ecosystem-restoration/). The authors noted the maps were not meant to guide local implementation. — [Mongabay](https://news.mongabay.com/2022/11/who-decides-on-priorities-for-ecosystem-restoration/)

### Our reading
- The concept is well established in research and EU/national planning. What seems missing in Normandy is an **open, transparent, sub-regional (1 km/commune) and weight-adjustable** tool that turns SRADDET priorities and Nature Restoration Regulation logic into local targets.
- **What a team could add:**
  - adjustable weights with a **robustness analysis** showing hotspots that stay on top whatever the weights;
  - explicit pressure layers (artificialisation, pesticides, fragmentation);
  - outputs per EPCI/SCoT that feed the TVB action plans the SRB requires of 100% of EPCIs, and the ZPR;
  - alignment with the habitat categories of the national restoration plan.
- **Timing risk:** the Région's new TVB/trame noire model (note dated June 2026) may soon become the official reference. Presenting the MVP as a prioritisation layer on top of the TVB, rather than a competing map, seems safer.

### Open points
- The exact content and maps of the SRADDET "secteurs d'actions prioritaires" were not read.
- Whether the 2026 TVB update includes a restoration-priority zoning is unknown.
- The regional breakdown of France's national restoration plan is unknown.

### Originality
**MEDIUM.** Priority-setting exists (SRADDET, the EU/national restoration framework, NaturaConnect), but no open, adjustable, fine-grained multi-criteria tool for Normandy was found. The originality lies in transparency and sensitivity analysis, not in the idea itself.

---

## Piste C: Normandy bocage over 70 years (hedge loss, fragmentation, "resilient" communes, targeting of planting)

### In short
Description and monitoring of Normandy's hedgerows are already well covered:
- DREAL's statistical bocage indicator, running since 2002;
- ANBDD's hedge density and connectivity indicator per EPCI;
- the national bocage monitoring scheme (DNSB) and the IGN BD Haie;
- the Normandie-Maine regional park's multi-date BD Bocage.

The national "Observatoire de la haie" is still not live. Two angles are less covered: a commune-level "resilience" typology, and spatial targeting of plantings for the Région's 2026 "zero net loss" scheme. Originality is low for the history, medium for the targeting.

### Sources
- **DREAL dataset "Analyse statistique de la dynamique bocagère – cercles statistiques – Normandie":** an indicator set up by the DIREN in 2002 with the Université de Caen (CRESO). Hedges are photo-interpreted in a sample of **300 m-radius circles**, giving a linear index (km/km²) and a coherence index (hedge intersections and free ends). Linked reports cover 1972, 1984, 1997–98, 2006, 2010 and 2012. Last update 15 Nov 2024. — [data.gouv.fr](https://www.data.gouv.fr/datasets/analyse-statistique-de-la-dynamique-bocagere-cercles-statistiques-normandie)
- DREAL also digitised hedges for **1947, 2010 and 2016**, with the year each hedge appeared or disappeared, on the Natura 2000 site FR2502014 (Pays d'Auge). — [data.gouv.fr](https://www.data.gouv.fr/datasets/haies-et-zones-boisees-du-site-natura-2000-fr2502014-bocages-et-vergers-du-sud-pays-dauge-normandie)
- **ANBDD 2024 update** (bocage monitoring data 2004–2022): Normandy has **53 m of hedge/ha against 27 m/ha** for metropolitan France, and the Manche is the densest department at 96 m/ha. — [ANBDD via DREAL (to check)](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/lineaireshaies-normandie-2024_anbdd.pdf)
- Since 1947, total hedge length fell by 790 km in the Orne, 1,200 km in the Manche and 640 km in the Calvados. These figures seem low and may refer to the sample circles. — [OFB "Rencontres réseaux de haies et biodiversité" (to check)](https://trameverteetbleue.fr/sites/default/files/references_bibliographiques/34997_ofb_rencontres_reseaux_de_haies_et_biodiversite_web.pdf). A Rencontres normandes workshop cited 180,000 km lost between 1947 and 2016, with an unclear perimeter (unverified).
- **PNR Normandie-Maine bocage observatory:** about 17,000 km of hedges lost in 60 years (1950–2010). Its BD Bocage has the vintages 1947/2001/2010/2020 (Orne) and 1947/2002/2010/2019 (Manche). — [Fédération des PNR](https://www.parcs-naturels-regionaux.fr/sites/federationpnr/files/document/centre_de_ressources/Normandie%20Maine%20bocage.pdf); [data.gouv.fr BD Bocage PNRNM](https://www.data.gouv.fr/datasets/bd-bocage-pnr-normandie-maine)
- **ANBDD EPCI indicator "Densité et connectivité des haies"** (one of the 3 indicators at the Oct 2022 launch) gives a report per EPCI with PDF/Excel export. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/); [ANBDD launch, 13 Oct 2022](https://www.anbdd.fr/lanbdd-lance-ses-indicateurs-de-la-biodiversite-des-epci-normands/)
- **DNSB (OFB + IGN, since 2017):**
  - phase 1 produced a national hedge map (BD TOPO + RPG); phase 2 characterised bocage landscapes; phase 3 is a field phase;
  - the Normandy field surveys run in 2025–2026 on 48 one-km² cells, and the scheme feeds the Observatoire de la haie.
  - Sources: [OFB Normandie](https://ofb.gouv.fr/actualites/dispositif-national-de-suivi-des-bocages-des-releves-de-terrain-en-normandie-en-2025-et); [BD Haie](https://www.data.gouv.fr/datasets/bd-haie); [IGN content description](https://geoservices.ign.fr/sites/default/files/2025-06/Descriptif_de_contenu_et_limite_DSB_v2.pdf)
- **Pacte en faveur de la haie** (2 Mar 2024): 25 actions, a net gain of 50,000 km of hedges between 2020 and 2030, €110M in 2024, and a planned "observatoire de la haie" giving a national map reference. — [info.gouv.fr](https://www.info.gouv.fr/actualite/les-25-actions-du-pacte-en-faveur-de-la-haie)
  - A 2025 parliamentary amendment said the observatory "never saw the light of day". — [Assemblée nationale](https://www.assemblee-nationale.fr/dyn/17/amendements/2632/CION-DVP/CD314)
  - A CNIG "Haies" working group (IGN + agriculture ministry) met on 23 Apr and 16 Jun 2026 to define the data to exchange: an AI-based IGN base layer, the "Guichet unique de la haie", planting data, and LiDAR later. **No national map publication was found as of Oct 2026.** — [CNIG GT Haies minutes](https://cnig.gouv.fr/IMG/pdf/20260423_gt_cnig_haies_-_crvf.pdf); [CNIG GT2](https://cnig.gouv.fr/IMG/pdf/20260616_oh_cnig_gt2_vf.pdf)
- **Région Normandie "Opération Normandie Haies" call 2026** (FEDER), open 9 Feb–30 Jun 2026, funds 3-year EPCI-level action plans (preserve, plant, add value to hedge wood). The goal is **zero net loss of hedge length in Normandy by 2030**, and Normandy is the 3rd densest hedge region in France. — [Région Normandie](https://www.normandie.fr/sites/default/files/2026-02/aap_operation_normandie_haie_2026_0.pdf). A 2024 DRAAF Pacte-haie call targeted 320 km of planting in Normandy in 2024. — [DRAAF Normandie](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/2024-aap-animation_pactehaie.pdf)
- COP Normandie roadmap: an action on hedge management with a multi-year, cross-cutting action plan at EPCI scale. — [COP Normandie pages (to check)](https://www.prefectures-regions.gouv.fr/normandie/Grands-dossiers/COP-Normandie/Cop-Normandie-penser-et-agir-pour-la-planification-ecologique-regionale)
- **Brittany comparator:** the Breizh Bocage programme (since 2007) and OEB open data on hedge length **per EPCI for 2015 and 2020**. — [data.gouv.fr](https://www.data.gouv.fr/datasets/lineaire-bocager-en-bretagne). Finistère "Observatoire de la haie" field inventories run June 2026–Dec 2027. — [press release](https://www.telgruc-sur-mer.bzh/wp-content/uploads/2026.05.27-CP-Observatoire-de-la-haie-des-inventaires-menes-dans-le-departement-du-Finistere-a-partir-de-juin-2026.pdf)

### Our reading
- A "70 years of loss" storytelling map would mostly repackage DREAL, ANBDD and PNR work. The jury may know these sources.
- **What a team could add:**
  - a **commune-level typology of "resilient" vs "eroding" bocage**, crossing hedge retention, connectivity, permanent grassland and livestock;
  - **graph-based targeting of new plantings** where they would reconnect the network most;
  - a **"hedge debt" per EPCI** against the 2030 zero-net-loss goal and the Pacte's +50,000 km;
  - packaging as a planning aid for the EPCI action plans funded by Opération Normandie Haies (a concrete user and a concrete timing).
- Because the national observatory is still not live, a regional "where to plant next" tool would fill a real gap. It must not claim to be a monitoring reference.

### Open points
- The full DREAL 1947–2016 statistical report (department figures) was not read.
- The ANBDD 2024 hedge document could not be opened.
- Afac-Agroforesteries tools (Label Haie, carbon tools) were not checked (not checked for lack of time).

### Originality
**MEDIUM.** Hedge trends are well documented (DREAL, ANBDD per EPCI, DNSB, PNR NM). A commune "resilience" typology combined with network-based planting targets for the Région's zero-net-loss plan was not found.

---

## Piste D: Biodiversity bulletin per EPCI (COP indicators + land take, organic/HVE farming, Fonds vert, ABC atlases, pesticides, water)

### In short
This is the **most pre-empted piste**. Since Oct 2022, **ANBDD's web app** generates an illustrated report per EPCI, with PDF/Excel download, for 8 biodiversity indicators, and pesticide and coastal-artificialisation indicators are announced. The State's **Observatoire normand des transitions** (Oct 2023) already offers portraits for every Normandy EPCI. SGPE/CGDD publish the **regional COP indicators** as open data. Originality is low unless the bulletin focuses on what is missing (response/effort indicators, COP indicators at EPCI scale).

### Sources
- **ANBDD "Indicateurs territoriaux de la biodiversité"**: the user picks an EPCI and an indicator, clicks "Générer le rapport", and downloads a PDF or raw data in Excel. The 8 current indicators are:
  1. change in main land-cover types;
  2. land consumed annually;
  3. ecological status of surface water bodies;
  4. hedge density and connectivity;
  5. change in permanent grassland within farmland (UAA);
  6. wetlands and areas likely to hold wetlands;
  7. fragmentation of terrestrial natural areas;
  8. river fragmentation.
  - **Planned:** coastal artificialisation, change in pesticide consumption, and "key figures of all indicators". Screenshots are dated July 2025; no data update date is shown. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
  - The app launched on **13 Oct 2022** with 3 indicators, funded by the Seine-Normandie water agency (AESN) and FEDER, for EPCI decision-makers (e.g., PLUi, local biodiversity strategies). — [ANBDD launch article](https://www.anbdd.fr/lanbdd-lance-ses-indicateurs-de-la-biodiversite-des-epci-normands/)
- ANBDD's site has separate sections: "Les indicateurs normands de la biodiversité" (regional), "Les indicateurs de biodiversité des EPCI", the regional SINP, scientific monitoring, and regional red lists. — [ANBDD](https://www.anbdd.fr/biodiversite/). The **Observatoire de la Biodiversité de Normandie** describes itself as a decision-support tool: it pools data through the ODIN platform and chooses and monitors regional indicators. — [Observatoire des territoires partner page](https://www.observatoire-des-territoires.gouv.fr/partenaires/lobservatoire-de-la-biodiversite-normandie-obn)
- **Observatoire normand des transitions** (State/DREAL, online Oct 2023): dynamic maps, **territorial portraits for every Normandy EPCI**, and a project catalogue. It is hosted at ssm-ecologie.shinyapps.io; a source mentions 41 indicators including a biodiversity domain. — [Préfecture press kit, 18 Oct 2023 (to check)](https://www.prefectures-regions.gouv.fr/normandie/irecontenu/telechargement/110191/827440/file/2023%2010%2018%20Transition%20%C3%A9cologique.pdf); [DREAL presentation, Jul 2023](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/observatoiretransitions_dossierpresentation_100723-1.pdf); [app](https://ssm-ecologie.shinyapps.io/observatoire-normand-des-transitions/accueil) (the app did not load; current update status unknown)
- **"Indicateurs régionaux de planification écologique"** (SGPE + CGDD): 6 themes including "mieux préserver et valoriser nos écosystèmes". These are outcome indicators made available for regional COP dashboards, at **regional scale**; last update 17/10/2025. — [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/indicateurs-regionaux-de-planification-ecologique/)
- **COP Normandie:** "Mieux préserver et valoriser nos écosystèmes" is one of 6 working groups. The 2025 roadmap had 47 actions, with an interim progress review in June 2025. The 2026 roadmap (Nov 2025) renames the group "…nos ressources" and has a "Modalités de suivi" section. — [COP Normandie page](https://www.prefectures-regions.gouv.fr/normandie/Grands-dossiers/COP-Normandie/Cop-Normandie-penser-et-agir-pour-la-planification-ecologique-regionale); [2026 roadmap (to check)](https://www.prefectures-regions.gouv.fr/normandie/irecontenu/telechargement/135545/992061/file/2026COP%20Normandie_FDR.pdf); [interim review 2025](https://www.prefectures-regions.gouv.fr/normandie/irecontenu/telechargement/133056/976084/file/COP%20-%20bilan%20interm%C3%A9diaire%202025.pdf)
- "Territoires engagés pour la nature" (TEN) in Normandy is run by ANBDD for communes and EPCIs; the next application window was Mar–Sept 2026. — [OFB](https://ofb.gouv.fr/territoires-engages-pour-la-nature-en-normandie)
- The **Fonds vert project list** is open data (CSV/XLSX for 2023, 2024, 2025) and includes the three "Fonds vert Biodiversité" measures. No official interactive map was found. — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/)
- DREAL Normandie published a "Profil biodiversité 2026" (file dated 10 Apr 2026); its content could not be opened. — [DREAL](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/20260410_profil_biodiversite2026-v20web.pdf)

### Our reading
- A generic "biodiversity bulletin per EPCI" would duplicate ANBDD's app, which already covers land take, water, hedges, grassland, wetlands and fragmentation, and the State's EPCI portraits. Both are well known to the regional biodiversity community.
- **What a team could add:**
  - **response/effort indicators** missing from ANBDD (Fonds vert biodiversity projects, ABC atlases, TEN labels, organic/HVE farming, protected-area share and type);
  - pressure indicators that ANBDD has announced but not published (pesticide purchases);
  - the **regional COP indicators computed at EPCI scale** (the SGPE dataset is regional only);
  - peer benchmarking, trend alerts, and **P2-style "good practice" indicators**.
- Presenting it as an extension of ANBDD's app (reusing its indicators) would improve credibility. Competing with it would hurt.

### Open points
- The figure of 68 COP indicators in our project notes could not be verified; the "Modalités de suivi" content was not read.
- The current indicator list of the Observatoire normand des transitions is unknown (the Shiny app did not load).
- The data vintages behind ANBDD's indicators are not stated on the page.

### Originality
**LOW** as an EPCI biodiversity dashboard (ANBDD and the Observatoire normand des transitions already do it). **MEDIUM** if refocused on effort/response and "good practice" indicators and on COP indicators at EPCI scale.

---

## Piste E: Water × agriculture (pressure–impact by river basin: where hedges or wetlands would help most)

### In short
The building blocks exist separately but were not found integrated:
- AESN's basin "état des lieux" (pressure → risk per water body);
- ANBDD's water ecological status per EPCI, with a pesticide indicator planned;
- Géophyto pesticide purchases, by department only;
- AREAS and CATER erosion/runoff diagnostics with hedge and fascine programmes;
- AESN's 12th programme priorities.

No public Normandy tool was found that combines pesticide purchases, crops, hedges/buffer strips, biological and dry-river observations and WFD status to target the levers per sub-basin. Originality is medium to high.

### Sources
- The Seine-Normandie basin has 1,782 water bodies, of which about 400 remain degraded by pressures. — [Banque des Territoires](https://www.banquedesterritoires.fr/bassin-seine-normandie-letat-ecologique-des-cours-deau-progresse-mais-trop-lentement)
- WFD "état des lieux" method: pressures with impact level 3 are "significant", and the risk of not meeting objectives (RNAOE) is assessed per water body. — [AESN EDL 2019 method](https://rapportage.eaufrance.fr/sites/default/files/DCE/2022/documents/FRH_Methodologie_generale_EDL2019.pdf)
- AESN's scientific council recommended that the next état des lieux distinguish pesticide types and toxicity and present results as a share of surface. — [HAL](https://hal-lara.archives-ouvertes.fr/hal-05505501v1)
- SDES: northern France, notably the Seine-Normandie basin, was the most exposed to pesticides in groundwater over 2021–2023. — [SDES 2025](https://www.statistiques.developpement-durable.gouv.fr/eaux-superficielles-et-souterraines-en-france-etat-des-connaissances-en-2025)
- **Géophyto** (Générations Futures) maps pesticide purchases from the national sales database (BNV-D) **by department**, 2015–2022, in tonnes and kg/ha of farmland, with filters by substance and hazard. A postcode-level refinement was planned, and purchase location may differ from use location. — [data.gouv.fr reuse](https://www.data.gouv.fr/reuses/geophyto-la-carte-des-achats-de-substances-pesticides); [Banque des Territoires](https://www.banquedesterritoires.fr/achat-de-pesticides-generations-futures-peaufine-sa-cartographie-par-departement)
- **ANBDD per-EPCI indicators** cover "État écologique des masses d'eau de surface", with **"Évolution de la consommation de produits phytosanitaires" announced**. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **AESN 12th programme 2025–2030:** a "Restaurer la nature" axis with F.1 (restore river dynamics) and F.2 (protect and restore wetlands and coastal environments). — [AESN programme](https://ecoentreprises-france.fr/app/uploads/2024/12/AESN_12EPROGRAMME_PROGRAMME.pdf)
- **Normandy runoff/erosion actors:**
  - AREAS states that Normandy is highly exposed to runoff and erosion, and that local authorities have proposed hedges, fascines and buffer zones for 20+ years with varying strategies. — [AREAS 2026 internship offer](https://www.gesteau.fr/sites/default/files/content_files/annonce_emploi/Proposition%20stage%20AREAS%202026.pdf)
  - The CATER Calvados-Orne-Manche runs full erosion–runoff diagnostics leading to large-scale soft-hydraulics programmes. — [Cingal-Suisse Normande offer](https://www.suisse-normande.com/wp-content/uploads/2026/01/STAGE-EROSION-ET-RUISSELLEMENT-2026.pdf)

### Our reading
- What is missing is an **integrated, open "pressure → impact → lever" view per sub-basin**. Such a view would allocate pesticide purchases by postcode to basins, overlay crop types and hedge/buffer deficits, relate them to biological indices and dry-river frequency, and rank where hedges, buffers or wetlands would intercept the most pressure.
- It answers P1 (where to restore) and P2 (negative interactions plus good-practice levers) at once. The main risks are methodological (purchase ≠ use; attributing causality), so honest caveats are needed.
- **Overlap to avoid:** AESN's official pressure assessment, and AREAS/CATER local diagnostics, which are field-based and finer.

### Open points
- The AESN "état des lieux 2025" maps and their availability were not found.
- The AESN 12th-programme priority zoning (e.g., priority catchments) was not checked.
- INRAE buffer-zone tools and Brittany "bocage anti-érosif" targeting tools were not checked (not checked for lack of time).

### Originality
**MEDIUM–HIGH.** All the layers exist separately and the official pressure assessment exists per water body, but no public Normandy tool integrating them into lever targeting (hedges/wetlands) per sub-basin was found. The difficulty is analytic credibility, not novelty.

---

## Piste F: River continuity (prioritising removal of obstacles to flow)

### In short
River continuity is heavily institutionalised and already prioritised:
- the OFB's national obstacle referential (ROE) and fish-passability protocol (ICE);
- an official **list of priority works for the Seine-Normandie basin** to treat by 2027 (open data);
- the migratory-fish plan PLAGEPOMI 2022–2027 with its maps of priority works;
- ANBDD's river fragmentation indicator per EPCI;
- the Sélune dam removals as the flagship case.

Originality is low to medium.

### Sources
- The OFB runs the ROE, the BDOe and the ICE protocol. ICE scores each obstacle from 0 (no obstacle) to 5 (impassable), to identify the most impactful works and prioritise interventions. — [OFB](https://ofb.gouv.fr/hydromorphologie-et-continuite-ecologique); [ICE protocol (2014)](https://trameverteetbleue.fr/sites/default/files/references_bibliographiques/cpa-ice-integralite-juillet2014.pdf)
- **"Ouvrages prioritaires sur le bassin Seine-Normandie":** works to be treated by 2027 under the national continuity action plan (PAPARCE), in shapefile/WMS/WFS. Last update Sept 2023. — [data.gouv.fr](https://www.data.gouv.fr/datasets/ouvrages-prioritaires-sur-le-bassin-seine-normandie)
- The draft **PLAGEPOMI Seine-Normandie 2022–2027** contains maps of the basin's priority works under PAPARCE and of the eel-plan priority sectors. — [PLAGEPOMI 2022–27](https://www.drieat.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/projet_plagepomi_complet_2022-27.pdf)
- ANBDD per-EPCI indicator "Fragmentation des cours d'eau". — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **Sélune:** a multi-component scientific monitoring programme (fish, crayfish, socio-geography), documented in a 2021 report for AESN. — [INRAE/HAL](https://hal.inrae.fr/hal-03352893/document); [OFB Rencontres n°70](https://bassinversant.org/wp-content/uploads/2020/02/Les-rencontres-OFB-n70-La-S%C3%A9lune.pdf). Secondary press reports Vezins lowered in 2019 and La Roche-qui-Boit in 2022, with salmon recolonisation upstream. — [Demotivateur (secondary)](https://www.demotivateur.fr/environnement/la-france-rase-deux-barrages-de-16-et-36-metres-pres-du-mont-saint-michel-des-le-printemps-suivant-des-saumons-naissent-la-ou-l-espece-avait-disparu-depuis-un-siecle-50637)
- **Comparator:** Corsica has a formal programme prioritising continuity restoration, built with the OFB and validated by the basin committee in 2021. — [DREAL Corse](https://www.corse.developpement-durable.gouv.fr/IMG/pdf/priorisation_des_actions_de_restauration_de_la_continuite_ecologique_corse_vf.pdf)
- **Europe:** the AMBER project estimated at least 1.2 million barriers in 36 countries and produced a European barrier atlas. — [Dam Removal Europe report 2021](https://damremoval.eu/wp-content/uploads/2022/05/0.-REPORT_Dam-Removal-Progress-2021-WEB-SPREADS.pdf). A record 487 barriers were removed in 15 countries in 2023; sources conflict on whether France ranked 1st or 2nd. — [Water Power Magazine](https://www.waterpowermagazine.com/news/record-breaking-surge-as-nearly-500-dams-removed-across-europe-in-2023-report-reveals-11683553/); [Earth.org](https://earth.org/all-time-record-removal-of-river-barriers-in-2023-marks-step-forward-in-european-ecosystems-restoration-report/)

### Our reading
- A datathon "priority list of obstacles" would re-derive official lists (PAPARCE, the regulatory "liste 2" rivers, PLAGEPOMI). It also enters a politically sensitive area (mill owners, the "politique apaisée" debate).
- **Possible added value:**
  - a transparent **re-ranking by expected gain** (accessible river length × fish presence × ecological status × ICE score);
  - progress tracking since the Sept 2023 list;
  - a public-facing "Sélune effect" narrative.
- Feasible, but only marginally original.

### Open points
- The current AESN and DREAL continuity priority maps (post-2023) were not checked.
- A Seinormigr prioritisation product was not found.
- Dam Removal Europe 2024–2025 figures for France were not found.

### Originality
**LOW–MEDIUM.** Obstacle prioritisation is an official, mature exercise in the Seine-Normandie basin (ROE/ICE, PAPARCE list, PLAGEPOMI), and ANBDD already gives river fragmentation per EPCI.

---

## Piste G: Restorable wetlands (potential wetlands now under crops or artificial land)

### In short
The inputs exist: the national "milieux potentiellement humides" model, the Seine-Normandie pre-localisation, and **ANBDD's per-EPCI indicator "Zones humides et milieux prédisposés"**. Other regions have already crossed potential wetlands with land use to find restoration targets; the Forum des Marais Atlantiques found that **47% of Brittany's potential-wetland surface** is altered. **No Normandy-wide public "restorable wetlands" layer** was found. Originality is medium to high.

### Sources
- The **national map of potential wetlands** (metropolitan France, 1:100,000) models envelopes from geomorphological and climatic criteria. It **ignores drainage and land use (crops)**, so it must be crossed with land cover to locate converted wetlands. — [zones-humides.org fact sheet (2014)](https://www.zones-humides.org/sites/default/files/fichiers/Fiche_milieux_et_zones_humides_vf_14042014_cle79515d.pdf)
- ANBDD per-EPCI indicator "Zones humides et milieux prédisposés à la présence de zones humides". — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **Brittany analogue (Forum des Marais Atlantiques, 2021):** crossing potential-wetland envelopes with uses that alter wetland functions showed that on average **47% of the potential-wetland surface** is occupied by urban areas, transport infrastructure, cropping or forestry, or ponds. The work also aimed to determine where to restore wetlands first. — [FMA/OiEau presentation (to check)](https://www.oieau.fr/sites/www.oieau.fr/files/jt_mesures_naturelles_retention_deau_-_zones_humides_bretagne_-_fma.pdf)
- The Loire-Bretagne water agency (AELB) prioritises wetland restoration plans (SDAGE 2022–2027, chapter 8) in areas where water bodies are at risk of missing their objectives. — [AELB strategy](https://www.biodiversite-centrevaldeloire.fr/sites/default/files/content/evenements/PDF/Journ%C3%A9e%20interpoles%20ZH/8-%20strategie%20AELB.pdf). This matters because part of south-west Normandy lies in the Loire-Bretagne basin (from basin geography).
- The national biodiversity strategy (SNB 2030) targets the **restoration of 50,000 ha of wetlands**. — [Assemblée nationale amendment (secondary)](https://www.assemblee-nationale.fr/dyn/17/amendements/0856/CION-DVP/CD488.pdf)
- AESN's 12th programme has action F.2 on wetlands. The basin committee of 3 Apr 2025 adopted a motion on wetland knowledge and its integration in planning documents, with inventory and protection ambitions for 2030. — [AESN programme](https://ecoentreprises-france.fr/app/uploads/2024/12/AESN_12EPROGRAMME_PROGRAMME.pdf); [CEN Bourgogne-Franche-Comté newsletter, Nov 2025](https://www.cen-bourgogne.fr/wp-content/uploads/2025/11/1000_lieux_humides_2025_bfc8.pdf)
- The COP Normandie roadmap includes a regional action programme to preserve and restore peatlands. — [COP Normandie (to check)](https://www.prefectures-regions.gouv.fr/normandie/Grands-dossiers/COP-Normandie/Cop-Normandie-penser-et-agir-pour-la-planification-ecologique-regionale)
- **Mediterranean comparator:** Tour du Valat maps lost wetlands to assess restoration potential using Earth observation. — [Tour du Valat](https://tourduvalat.org/dossier-newsletter/la-cartographie-au-service-de-la-restauration-des-zones-humides-mediterraneennes)

### Our reading
- **A Normandy-wide layer would be new.** It would cross potential wetlands (INRAE model + AESN pre-localisation + CarHab soil-moisture biotopes) with current crops or artificial land, then prioritise by function (flood buffering, water quality, connectivity) and by EPCI/sub-basin.
- It ties directly to the SNB target (50,000 ha), AESN action F.2 and the planning-integration motion. The Brittany FMA approach gives methodological legitimacy.
- **Caveats for the pitch:** a "potential" envelope is not a confirmed wetland (field validation needed), drainage data are rarely open, and AESN/DREAL wetland pre-localisation teams would want to be cited.

### Open points
- Whether DREAL Normandie or AESN already publish a "zones humides dégradées / restaurables" layer for Normandy could not be confirmed (not checked for lack of time).
- No details were found on ZHIEP/ZSGE designations in Normandy, or on CEN Normandie's wetland action plan.

### Originality
**MEDIUM–HIGH.** The inputs and an ANBDD wetland indicator exist, and Brittany has done the crossing, but no Normandy-wide prioritised "restorable wetlands" product was found.

---

## Piste H: Blind spots of protection (probable habitats of Community interest and protected-species hotspots outside ZNIEFF/Natura 2000/reserves)

### In short
Gap analysis of protected areas exists **nationally**: PatriNat's protected-areas diagnostics of 2019, 2020 and 2023. Normandy has a regional SNAP action plan (2022–2024, due for update for 2025–2027) with lists of planned strict-protection zones (ZPF). No public Normandy-specific gap map combining CarHab habitats and protected-species hotspots was found. CarHab coverage of Normandy is uncertain: Normandy is not among the 8 fully mapped regions as of June 2026. Originality is medium to high, depending on data availability.

### Sources
- **PatriNat diagnostic (2020, "Représentativité et lacunes"):**
  - it assessed 1,298 species and 114 Natura 2000 habitats with over 5 million occurrence records, using representativeness thresholds of 2–100%;
  - the strict-protection network is **not ecologically representative**, and the rarest stakes are the least covered;
  - **about 9% of assessed species are covered by no strict-protection area**;
  - a 2019 SCAP update and a **Feb 2023 study crossing biodiversity stakes with pressures** also exist.
  - Sources: [INPN/PatriNat documents (to check; exact attribution between documents uncertain)](https://inpn.mnhn.fr/docs-web/docs/download/370549); [INPN doc 355009](https://inpn.mnhn.fr/docs-web/docs/download/355009)
- Habitats Directive sites cover about 29.2% of the range of habitats and 24.6% of that of species. — [PatriNat, "L'efficacité du réseau Natura 2000 terrestre français" (to check)](https://inpn.mnhn.fr/docs-web/docs/download/361309)
- **Normandy SNAP regional action plan 2022–2024**, to be updated during 2025. About **0.5% of Normandy is under strict protection and 21% under protected areas** (undated figure). — [Aides-territoires (Fonds vert sheet)](https://aides-territoires.beta.gouv.fr/aides/proteger-et-restaurer-les-espaces-naturels-25/)
  - DREAL per-department lists of planned creations and extensions (Nov 2021) are "révisable pour le plan d'action pour les aires protégées en Normandie 2025-2027". — [DREAL, Calvados list](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/extension_du_reseau-ap_14.pdf)
  - In June 2025 the regional scientific council (CSRPN) approved a case-by-case procedure to recognise terrestrial strict-protection zones. — [CSRPN opinion](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/avis_csrpn_2025-06-02_labellisation_zpf.pdf)
- **CarHab:** 91% of metropolitan France and Corsica is now mapped (88 departments), with 8 regions at 100%. Normandy is not in that list, so it is not fully covered. Maps are shown in the INPN viewer; the page was updated 26 June 2026. — [Ministère, CarHab (to check)](https://www.ecologie.gouv.fr/politiques-publiques/carhab-programme-cartographie-nationale-predictive-habitats-naturels)
- The CESER criticised the low protection ambition of the regional biodiversity strategy compared with the SNAP. — [CESER](https://ceser.normandie.fr/sites/default/files/2024-04/7%20Avis%20STRATEGIE%20REGIONALE%20POUR%20LA%20BIODIVERSITE%20NORMANDIE%202030.pdf)
- **EU level:** NaturaConnect models biodiversity distributions to find protected-area gaps and corridors. — [IEEP](https://ieep.eu/news/establishing-a-true-coherent-trans-european-nature-network/)

### Our reading
- With strict protection at about 0.5% against a national target of 10%, a **Normandy gap map** would be highly policy-relevant. It would show probable habitats of Community interest (CarHab) and protected-species hotspots (OpenObs) outside ZNIEFF/Natura 2000/RN/APPB, plus a shortlist of candidate ZPF.
- PatriNat's analyses are national and not published as a regional interactive tool, as far as found.
- **Risks:**
  - CarHab coverage in Normandy (check per department);
  - observation bias in species data (hotspots of observers);
  - sensitivity of locating protected species (data blurring).
- The DREAL owns the regional plan, so the tool should be framed as decision support for it.

### Open points
- Which Normandy departments have CarHab maps was not confirmed.
- Whether DREAL or ANBDD produced a regional SCAP/SNAP gap analysis map is unknown.
- The text of the 2025–2027 plan was not found.

### Originality
**MEDIUM–HIGH.** National gap analyses exist, but no public Normandy gap map combining predicted habitats and species hotspots was found. Originality depends on data coverage (CarHab) and careful handling of sensitive species data.

---

## Piste I: "What concrete ate" (recent artificialisation overlaid on hedges, grasslands, ZNIEFF and wetlands, against the ZAN trajectory per EPCI)

### In short
**How much** land has been taken is well covered:
- the beta.gouv tool Mon Diagnostic Artificialisation (MDA);
- the national artificialisation observatory;
- the Région's land-consumption app (2011–2020, EPCI and parcel);
- ANBDD's land-consumption and land-cover-change indicators per EPCI.

**What ecological features were lost** (hedges, grasslands, ZNIEFF, wetlands) per EPCI, against ZAN, was not found in these Normandy tools. Similar "natural areas lost within ZNIEFF" indicators exist elsewhere, from ONB-type work in Auvergne-Rhône-Alpes (AURA) and Nouvelle-Aquitaine (ARB NA). Originality is medium to high.

### Sources
- **Mon Diagnostic Artificialisation:**
  - consumption of natural, agricultural and forest land by destination, crossed with population, households and jobs, with comparison between territories;
  - customisable local reports, including the **triennial local report**, covering artificialisation and soil sealing;
  - levers: housing vacancy, **brownfields without a project**, a land-sobriety trajectory;
  - data from Cerema, IGN and INSEE.
  - The page does **not mention biodiversity, wetland, TVB or ZNIEFF overlays**. — [mondiagartif.beta.gouv.fr](https://mondiagartif.beta.gouv.fr/)
  - It was built as a beta.gouv startup. — [Acteurs publics (title)](https://acteurspublics.fr/articles/une-start-up-detat-va-aider-agents-et-elus-a-mesurer-lartificialisation-des-sols)
- ANBDD per-EPCI indicators "Évolution de l'aire occupée par les principaux types d'occupation des sols" and "Surfaces consommées annuellement par le foncier", with "artificialisation du littoral" planned. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **SRADDET objective 49 (Région):** artificialisation was about 1,200 ha/yr over 2011–2020, and Normandy ranks among the most land-consuming regions per inhabitant. — [normandie-a-la-carte](https://normandie-a-la-carte.normandie.fr/sobriete_fonciere/objectif_sraddet/o49.pdf). A regional app shows land consumption 2011–2020 at EPCI and parcel scale. — [Région Normandie (to check; attribution likely)](https://www.normandie.fr/print/pdf/node/4256)
- **ONB-type indicator, natural areas lost within ZNIEFF (Corine Land Cover 1990–2012):**
  - metropolitan France lost 36,750 ha (0.2% of ZNIEFF surface), and losses outside ZNIEFF were twice as high;
  - AURA lost about 5,000 ha, mostly grasslands. — [DREAL AURA](https://www.auvergne-rhone-alpes.developpement-durable.gouv.fr/IMG/pdf/e2_evolution_milieux_znieff.pdf)
  - In AURA, 785 ZNIEFF (about a quarter) showed artificialisation dynamics, mostly wetlands and dry slopes; 1.2% of ZNIEFF surface was artificialised against 4.8% regionally. — [DREAL AURA](https://www.auvergne-rhone-alpes.developpement-durable.gouv.fr/IMG/pdf/20200310_pub_a4znieff.pdf)
  - ARB Nouvelle-Aquitaine published a similar indicator in 2020. — [ARB NA](https://www.biodiversite-nouvelle-aquitaine.fr/wp-content/uploads/2021/02/2020_ARBNA_indicateur_EvolutionMilieuxRemarquablesZNIEFF_VF.pdf)
- A 2015 ministry report listed an ONB wetland indicator "Artificialisation du territoire métropolitain (à décliner pour les milieux humides)" as under construction; its current status is unknown. — [MEDDE 2015 report](https://www.zones-humides.org/sites/default/files/pdf/rapport_medde_2015_-_vf.pdf)

### Our reading
- **Added value:**
  - a per-EPCI **"ecological loss balance"**: hectares of permanent grassland, hedge length, wetland and ZNIEFF surface consumed by artificialisation, using recent OCS GE and Cerema series;
  - a **quality-weighted land-take indicator** alongside the ZAN quantity trajectory.
- This complements MDA, which is quantity-focused, and ANBDD's land-cover change, by answering "what did we lose" in elected officials' ZAN language. It is a P2-style indicator of a negative interaction.
- **Recent change layers make it timely**, but OCS GE change availability per department should be checked by us (out of scope here).

### Open points
- Whether ANBDD's "évolution de l'occupation des sols" report already shows transitions such as grassland → artificial was not checked.
- Whether the national observatory or Cerema publishes "artificialisation of natural/wetland areas" per commune was not confirmed.

### Originality
**MEDIUM–HIGH.** Land-take quantity tools abound (MDA, the Région, ANBDD), but an ecological-quality balance of recent artificialisation per EPCI against ZAN was not found in Normandy. Comparable indicators exist only in other regions or on old data (CLC 1990–2012).

---

## Piste J: Coherence of public action (needs/pressures × efforts per EPCI, to find under-served territories)

### In short
No tool or study was found that matches biodiversity needs (pressures, stakes) with efforts per EPCI: Fonds vert biodiversity projects, ABC atlases, organic/HVE farming, protected areas, TEN labels. Fonds vert projects are open data without an official map, and financing studies quantify gaps only at national level. Originality is high, with strong P2 relevance; the framing is politically sensitive.

### Sources
- The **Fonds vert project list** is open data (2023–2025 files) and includes the three "Fonds vert Biodiversité" measures. These were funded under budget programme 380 in 2023 and transferred to programme 113 in 2024. — [data.gouv.fr](https://www.data.gouv.fr/datasets/fonds-vert-liste-des-projets-subventionnes/). The Fonds vert biodiversity measure funds communal biodiversity atlases (ABC) and nature-restoration actions. — [Aides-territoires](https://aides-territoires.beta.gouv.fr/aides/agir-pour-la-biodiversite-des-atlas-de-la-biodiversite-communale-a-la-restauration-de-la-nature/)
- **National financing (IGF-IGEDD 2022 report):**
  - the State and its operators account for €1.3bn of biodiversity spending (57%);
  - local authorities spent about €900M in direct favourable spending in 2021, of which departments €430M (47%);
  - additional needs for the State and operators: €619M in 2023, up to €890M in 2027. — [vie-publique.fr](https://www.vie-publique.fr/sites/default/files/rapport/pdf/287780.pdf)
- A 2026 finance-bill amendment argued that the €110M "dotation biodiversité" falls short of the estimated €689.5M needs of communes and EPCIs, and called for territorialised measures. — [Sénat](https://www.senat.fr/enseance/2025-2026/138/Amdt_II-1858.html)
- Effort-type programmes exist but are not mapped against needs: TEN in Normandy (run by ANBDD) [OFB](https://ofb.gouv.fr/territoires-engages-pour-la-nature-en-normandie), and the FEDER calls for TVB works and Normandie Haies (see B and C).
- Nouvelle-Aquitaine noted that local biodiversity policies are implemented without coherence between levels of government, and proposes territorial agreements. — [SRB Nouvelle-Aquitaine sheet](https://srb.biodiversite-nouvelle-aquitaine.fr/wp-content/uploads/2023/02/E43_CTEC.pdf)

### Our reading
- A needs × efforts matrix (quadrants such as "high pressure / low effort") is a genuinely new decision view for the Région and the State. It directly serves P2's "guide public policy", and it reuses existing indicators (ANBDD pressures, the protected-area share) instead of duplicating them.
- **Framing advice:** present it as "where to focus support and engineering", not as a ranking of "bad" EPCIs, since the jury includes regional elected officials.
- **Methodological risks:** effort data are partial (Fonds vert is only one source), and population or surface normalisation choices drive the results.

### Open points
- Regional or departmental biodiversity funding datasets (Région FEDER beneficiaries, AESN aid) were not checked.
- An existing Fonds vert map reuse on data.gouv was not checked (reuses page not opened).

### Originality
**HIGH.** No needs × efforts biodiversity tool per EPCI was found, in Normandy or nationally; financing studies are national and non-spatial.

---

## Piste K: Citizen interface "Ma commune et sa nature" (plain-language commune sheet)

### In short
Species-centred commune information exists:
- the INPN Espèces app's commune lists;
- the **Atlas d'ODIN** (ANBDD) with species lists per commune and 5 km maps;
- the Lobelia platform for flora (Conservatoire botanique national de Normandie);
- ABC atlas PDFs for some communes;
- ANBDD resource sheets for communes.

EPCI portraits exist in the Observatoire normand des transitions. No plain-language, commune-level sheet for the general public was found that combines state, pressures, trends and "what you can do". Originality is medium: the innovation is in format and audience rather than data.

### Sources
- **Atlas d'ODIN** (ANBDD, fauna part of the regional SINP): species distribution maps on a 5 km × 5 km grid, **lists of species observed per commune**, and the 500 latest observations (dates up to 14/10/2026). It states it is not an exhaustive inventory. Flora, fungi and habitats are in **Lobelia** (Conservatoire botanique national de Normandie). — [odin.anbdd.fr](https://odin.anbdd.fr/)
- The **INPN Espèces** app (free, nationwide) lets users choose a commune and see the species known there, or extend to the department. INPN also gives species lists by commune, protected area or 10 km grid cell. — [INPN documentation (to check)](https://inpn.mnhn.fr/docs-web/docs/download/402801); [INPN presentation](https://inpn.mnhn.fr/accueil/presentation-inpn)
- ABC atlases exist for several Normandy communes, e.g. Le Havre (2023 edition), Rouen (2021, LPO Normandie), Grand-Quevilly (CEN + LPO Normandie). They are distributed as PDF reports. — [Le Havre ABC 2023](https://lehavre.fr/sites/default/files/fichier/atlas_de_la_biodiversite_communale_edition_2023.pdf); [Rouen ABC](https://Rouen.fr/sites/default/files/download/2022/inventaire_biodiversite_abc_rouen_2021_-_lpo_normandie_-_2022.pdf); [Grand-Quevilly synthesis](https://grandquevilly.fr/app/uploads/2025/12/synthese-ABC-vf.pdf)
- ANBDD publishes resource sheets for communes, e.g. "La connaissance de la biodiversité communale" and "Favoriser la biodiversité dans ma commune". — [ANBDD](https://www.anbdd.fr/publication/fiche-ressources-la-connaissance-de-la-biodiversite-communale/); [ANBDD](https://www.anbdd.fr/publication/fiche-ressources-favoriser-la-biodiversite-dans-ma-commune-1/)
- The Observatoire normand des transitions offers EPCI-level portraits, not commune-level ones. — [DREAL presentation](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/observatoiretransitions_dossierpresentation_100723-1.pdf)

### Our reading
- **The gap is in synthesis and readability for "all Normans":** one static, lightweight page per commune (good for digital sobriety) answering:
  - what nature is here (habitats, emblematic species from ODIN/INPN);
  - is it doing well (hedges, grassland, water status, land take);
  - what threatens it;
  - what is being done (ABC, TEN, protected areas);
  - what I can do (citizen-science links).
- Reusing ODIN and INPN rather than re-displaying raw species lists avoids duplication.
- It fits the jury's "benefit to all Normans" criterion, but is less of a decision tool for P1/P2. It works best as the public face of B, C, D or I.

### Open points
- Citizen-science apps (Biolit, Sentinelles de la nature, Faune-Normandie/Visionature commune pages) and any "biodiversité de ma commune" national portal were not checked (not checked for lack of time).

### Originality
**MEDIUM.** The data and species lists per commune already exist (ODIN, INPN, ABC), but no plain-language, multi-indicator commune sheet for the general public was found. The originality is in format and audience.

---

## Piste L: Scenario simulator ("what if" planting X km of hedges or renaturing N brownfields)

### In short
Scenario tools exist for experts:
- **Graphab**, a free desktop connectivity-modelling program with documented hedge and corridor scenarios;
- Mon Diagnostic Artificialisation's sobriety trajectory;
- ADEME **Bénéfriches** for project impacts.

No public, online "what-if" simulator linking hedge plantings or brownfield renaturation to connectivity and land-take indicators for Normandy was found. Originality is high, with feasibility risk.

### Sources
- **Graphab** (ThéMA lab, free) evaluates the impact of a development or land-use change on connectivity and compares scenarios, typically in impact studies. Its method sheet recommends several complementary metrics. Its 2025 booklet presents 12 case studies, including prioritising ponds to restore. Version 3.0 is not compatible with earlier projects. — [Graphab method sheet](https://www.trameverteetbleue.fr/sites/default/files/fiche4_graphab_applications.pdf); [Livret Graphab 2025](https://thema.univ-fcomte.fr/productions/software/graphab/download/Livret_Graphab_2025.pdf)
- **INRAE hazel dormouse case:** restoring the 30 most relevant existing corridors raised landscape connectivity (equivalent connected area, ECA) by 11%, while creating 30 new hedges raised it by 38%. — [INRAE/HAL (to check)](https://hal.inrae.fr/hal-02609216v1/file/pub00061169.pdf)
- Mon Diagnostic Artificialisation includes a land-sobriety trajectory tool. — [mondiagartif.beta.gouv.fr](https://mondiagartif.beta.gouv.fr/)
- ADEME's **Bénéfriches** quantifies the environmental, social and economic impacts of a brownfield project, as a complement to Mutafriches. — [Cerema slides listing ADEME's Mutafriches/Bénéfriches](https://cpdt.wallonie.be/wp-content/uploads/2026/02/3_CEREMA-Cartofriches-Olivier-Dupre.pdf); [ADEME friches page (to check)](https://agirpourlatransition.ademe.fr/collectivites/conseils/urbanisme/foncier-friches)
- The Région's 2026 TVB update produces modelling results as a QGIS project; it is potentially the reference network for any regional scenario. — [normandie-a-la-carte note (to check)](https://normandie-a-la-carte.normandie.fr/tvb/tvb_note_accompagnement_donnees.pdf)

### Our reading
- **A public, browser-based simulator** would be novel in Normandy and attractive in a pitch: draw or allocate X km of hedges or N brownfields, then see the change in a simple connectivity metric and in the land-take balance.
- **Feasibility:** full Graphab-style modelling in about 4 weeks is risky. Simplified metrics (hedge density and connectivity proxies, distance-to-reservoir, or precomputed marginal gains per cell) would be needed, plus clear caveats.
- **Best used as a module on top of B, C or A** (e.g., "the priority cells in B: what if we plant there?") rather than as a standalone piste.

### Open points
- Afac/Chambres d'agriculture hedge simulators (e.g., carbon tools) and Cerema ZAN simulators beyond MDA were not checked.
- Whether the Région's TVB modelling will be released in a reusable form is unknown.

### Originality
**HIGH.** Only expert desktop tools (Graphab) or quantity-only trajectories (MDA) exist; no public "what-if" restoration simulator for Normandy was found. It works best as an add-on to B, C or A for feasibility.

---

## Piste M: Coast & Seine estuary (coastal erosion, seabed habitats, tourism and industrial pressure)

### In short
Strong institutional tools already cover this:
- the GIP Seine-Aval **REPERE** shared reference for estuary restoration priorities (5 priority orientations);
- the Seine-Aval 8 programme (2027–2032) with mapping in development;
- ROL (formerly ROLNP, now covering Normandy and Hauts-de-France), with a coastal dynamics atlas and app;
- Cerema/DREAL prospective shorelines for 2050 and 2120;
- ANBDD's planned coastal artificialisation indicator.

Originality is low to medium, and the domain is specialised.

### Sources
- **REPERE** ("référentiel partagé des priorités de restauration des fonctions écologiques de l'estuaire de la Seine"), initiated in 2018 by GIP Seine-Aval with the DREAL. The CSRPN opinion of May 2023 lists **5 priority orientations**:
  1. diversify aquatic habitats of the main channel;
  2. preserve and recreate mudflats;
  3. restore lateral continuity;
  4. preserve and restore wet grasslands;
  5. limit pollution impacts.
  - It also notes that compensation measures are small and lack global coherence. — [CSRPN opinion](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/avis_csrpn_2023-05-08_estuaire_seine_gipsa.pdf); [REPERE 2019](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/repere-05-06-2019-gipsa.pdf)
- The Seine-Aval 8 programme (2027–2032) orientations include a global restoration and climate-adaptation strategy, with mapping among the methods in development. — [GIPSA SA8 orientations](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/gipsa_orientations_sa8.pdf)
- ROL ("Réseau d'Observation du Littoral de Normandie et des Hauts-de-France") works on coastal mobility, hazards and risk management. It publishes a historical shoreline atlas and a "Dynamique côtière" app (erosion and accretion). — [Observatoire des territoires](https://www.observatoire-des-territoires.gouv.fr/index.php/partenaires/reseau-dobservation-du-littoral-de-normandieet-des-hauts-de-france-rol); [B2FIND record](https://b2find.eudat.eu/dataset/00debe7a-e851-5648-ad8b-0dd629abb7ff)
- **Prospective shorelines for 2050 and 2120** (Cerema for DREAL Normandie), based on the knowledge available in 2019. — [data.gouv.fr](https://www.data.gouv.fr/datasets/le-littoral-normand-aux-horizons-2050-et-2120-zones-devolution-du-tait-de-cote/informations)
- In Seine-Maritime, estimated losses are about 230 ha in 20 years, 300 ha in 50 years and 420 ha in 100 years. — [DDTM 76 public leaflet](https://www.seine-maritime.gouv.fr/index.php/contenu/telechargement/38432/257237/file/Plaquette_GRAND_PUBLIC_vf.pdf)
- ANBDD has announced a per-EPCI indicator "artificialisation du littoral". — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)

### Our reading
- Coastal and estuary restoration priorities are already set by expert bodies (GIPSA/REPERE, DREAL), and erosion is monitored (ROL, Cerema).
- A team could integrate erosion, habitats and pressures (tourism, ports/industry) into a "coastal squeeze" view per coastal commune. This overlaps mature institutional work and needs marine expertise in a short timeframe.
- One possibly original niche is a **"retreat space for nature" indicator**: land behind the 2050/2120 lines where habitats could migrate. Not checked against existing work.

### Open points
- Seabed habitat mapping (Ifremer, the Channel maritime façade strategy DSF MEMN) and marine-pressure tools were not checked (not checked for lack of time).
- REPERE maps were not seen.

### Originality
**LOW–MEDIUM.** The estuary restoration priorities (REPERE) and coastal erosion tools (ROL, Cerema 2050/2120) exist and are run by specialist bodies. Only a niche "space for habitat migration" angle might be new.

---

## Piste N: Horses & grasslands (the equine sector as a driver of permanent grassland and bocage maintenance)

### In short
No study or tool was found that maps or quantifies the equine sector's contribution to keeping permanent grassland and hedges in Normandy. Existing material is sectoral:
- IFCE's "Atouts verts des équidés";
- the EIP-AGRI operational group "Equi-Pâture Normandie" (2016–2017), focused on grazing management and welfare, not biodiversity;
- the **EquuRES** environmental label of the Conseil des Chevaux de Normandie.

Grassland loss alarms are documented: the CSRPN says Normandy ranks first for loss of permanent grassland. Originality is high, and the angle fits P2 (positive interactions).

### Sources
- **IFCE-OESC "Atouts verts des équidés" (2020):** the average grazed area per horse in France is about 1 ha, and grazing shapes meadow composition whatever the species. It is a national overview, not Normandy-specific. — [IFCE](https://www.ifce.fr/wp-content/uploads/2020/02/OESC-Atouts-verts-des-equides.pdf)
- **EIP-AGRI OG "Equi-Pâture Normandie":**
  - IFCE lead, with the Chambre régionale d'agriculture and the Conseil des Chevaux de Normandie;
  - 2016–2017, 4 pilot farms (Calvados, Manche, Orne), €68,679;
  - topics: grassland management for fodder autonomy, targeted deworming, welfare and economics;
  - **no biodiversity objective stated**;
  - outputs: guides, fact sheets and a welfare app. — [EU CAP Network](https://eu-cap-network.ec.europa.eu/projects/horse-grazing-normandy_fr)
- **EquuRES label** (Conseil des Chevaux de Normandie): 3 levels for all equine businesses, with themes including resource and biodiversity protection and "espaces extérieurs et paysages". Counts conflict: 18 labelled structures including 7 in Normandy (CCN, 16/05/2025) against "60 Normandy structures" in another source. — [CCN AGM 2025](https://chevaux-normandie.com/wp-content/uploads/2025/05/AG-CCN-2025-VF.pdf); [AD Normandie equine sheet](https://adnormandie.fr/wp-content/uploads/2024/11/Fiche_Equin-1.pdf); [CCN sustainable development sheet](https://chevaux-normandie.com/wp-content/uploads/2019/12/13-DEVELOPPEMENT-DURABLE.pdf)
- The **CSRPN motion of Dec 2024** says Normandy holds first place for loss of permanent grassland surface (−7.43%) and calls for restoration to bring the ratio back to −4.5%. — [CSRPN Normandie](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf)
- Basse-Normandie permanent meadows are floristically rich: 612 meadow species recorded (Fourrages, 2003). — [INRAE/HAL](https://hal.inrae.fr/hal-02681249/document)
- ANBDD per-EPCI indicator "Évolution de la superficie toujours en herbe dans la SAU". — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)

### Our reading
- A Normandy-specific "positive interaction" indicator would be both original and highly regional, and fits P2's "value good practices". It would measure the grassland and hedge share maintained by equine holdings, per commune or small agricultural region, against the grassland-loss trend.
- **Key feasibility question (outside this research's scope):** whether open data can link equine activity to parcels (e.g., RPG crop codes for grazed grassland, equine census aggregates). Without that link, the piste reduces to correlation maps, which is a weaker claim.

### Open points
- No IFCE/OESC Normandy regional study on equines and grasslands was found. Sources asserting Normandy's rank in the equine sector were not collected (not checked for lack of time).

### Originality
**HIGH.** Nothing similar was found. The equine–grassland–bocage link is documented only qualitatively and sectorally, and would be a distinctive Normandy "good-practice" indicator, provided open data allow a credible spatial link.

---

## Previous hackathons and datathons

### In short
Previous **Datathon Normandie** editions (2023–2025) had other themes (health/environment/energy; then employment/training), so **2026 is the first biodiversity edition**. No prior Normandy datathon project on restoration prioritisation was found. National biodiversity hackathons are old (#HackBiodiv 2016) or generic (Open Data University), and no comparable winning restoration MVP was identified.

### Sources
- **Datathon Normandie 2026** (Région Normandie + DataLab Normandie members; partners include the Préfecture and EU co-financing):
  - theme: valuing biodiversity and habitat data while accounting for the impact of human activities;
  - challenge 12 Oct–16 Nov 2026, launch call 12 Oct; expert team answers questions;
  - jury and closing **23 Nov 2026 in Rouen**, with Vice-Presidents of the Région;
  - teams of 2–5, up to 50 participants. — [DataNormandie](https://www.datanormandie.fr/actualites/inscriptions-au-datathon-normandie-2026)
  - Note: the page says the challenge runs to 16 Nov, while our project notes say deliverables are due 12 Nov at noon (presumably from the règlement, not read).
- **2025 (3rd edition):** employment and training, 5 Nov–9 Dec 2025, jury at the Hôtel de Région in Caen. — [DataNormandie](https://www.datanormandie.fr/actualites/datathon-normandie-2025). Six teams took part: AUBE, NormandiSccore, FormaRoute, HeulaJob, Talandie and **Compétences à la carte (winner)**. — [DataNormandie news list](https://www.datanormandie.fr/actualites); [2025 review & winners (team names to check)](https://www.datanormandie.fr/actualites/datathon-2025-bilan-et-laureats)
- **2023 edition:** health, environment and energy (interactions on the Normandy territory), 9 Oct–9 Nov 2023, MVP expected, teams of 2–5. — [ANBDD article, 20 Sept 2023](https://www.anbdd.fr/datathon-le-challenge-data-organise-par-la-region-normandie/)
- The Région's 2026–2028 data/AI roadmap (Dec 2025) presents the Datathon Normandie as a way to boost reuse of DataNormandie data, and lists climate, biodiversity and natural resources among its conditions for success. — [Région Normandie](https://www.normandie.fr/sites/default/files/2026-03/20251215_synthese_feuille_de_route_vf.pdf)
- **Note:** the 2023 winner PRIORENO (per our project notes) shares its name and purpose with **Prioréno**, a national Banque des Territoires service built with the State, Enedis and GRDF that helps local authorities prioritise public-building energy renovation. — [Banque des Territoires](https://www.banquedesterritoires.fr/prioreno-un-nouveau-service-data-de-renovation-energetique)
- **#HackBiodiv (2016):** run by the environment ministry with Etalab, 3–5 June 2016 in Paris, on INPN/SINP data. A preparatory BarCamp defined 8 challenges, including tourism, health, biodiversity in town, climate change, agriculture and data valorisation. — [data.gouv.fr](https://www.data.gouv.fr/posts/hackbiodiv-les-donnees-du-hackathon-biodiversite); [data.gouv.fr BarCamp](https://www.data.gouv.fr/posts/hackbiodiv-les-donnees-du-barcamp-et-du-hackathon-biodiversite)
- **Open Data University** (Latitudes, supported by DINUM; challenges on defis.data.gouv.fr): season-4 themes covered climate, health, culture/AI and mobility. The winner (Université de Tours, "Métropole Bordeaux Résilience") assessed the vulnerability of public buildings to industrial and ecological risks. — [data.gouv.fr](https://www.data.gouv.fr/posts/open-data-university-decouvrez-les-projets-finalistes-de-la-quatrieme-saison)
- The **"Hackathon Outdoor Data Lab"** (outdoor sports and biodiversity, Geotrek ecosystem) is reported in Voiron with Université de Rouen Normandie among partners. The date is unclear: 19–20 Nov 2025 according to one source, but the file is named 2026-10. — [Geotrek presentation](https://geotrek.ecrins-parcnational.fr/ressources/presentations/2026-10-Hackathon-Outdoor-Data-Lab.pdf)
- **EU Datathon:** the 2021 edition ran a Natura 2000 dataset webinar for its Green Deal challenge, and 2022 had a Green Deal category; nature-related winners were not identified. — [data.europa.eu](https://data.europa.eu/en/news-events/news/eu-datathon-webinar-european-environment-agency); [Interoperable Europe, 2022 winners](https://interoperable-europe.ec.europa.eu/collection/open-data/news/meet-winners-eu-datathon-2022)
- **Related non-hackathon programmes:**
  - OFB "Mission Nature": 28 funded restoration projects in 2026, extended to 2026–2027. — [OFB](https://ofb.gouv.fr/sites/ofb-gouv-fr/files/2026-07/ofb_missionnature_a4_web_pages.pdf)
  - IUCN/Huawei Tech4Nature prizes, first awarded 13 Oct 2025. — [IUCN](https://iucn.org/fr/node/45222)
  - iDiv MICODA biodiversity datathon (2023, Latin America). — [MICODA](https://micoda.idiv.de/datathons/2023)
  - Hackathon "Donnée en Région" Nouvelle-Aquitaine 2024 (booklet exists; content not checked). — [Préfecture Nouvelle-Aquitaine](https://www.prefectures-regions.gouv.fr/nouvelle-aquitaine/irecontenu/telechargement/118661/882958/file/Livret_Hackathon_Donn%C3%A9e.en.R%C3%A9gion_Nouvelle-Aquitaine%202024.pdf)

### Our reading
- **Within this competition series, biodiversity is new territory:** no previous Datathon Normandie project competes with the pistes.
- The Prioréno precedent suggests that the jury rewarded a **regionally adapted, usable decision map** even when a national namesake tool existed. Originality may therefore be judged on regional fit and usability as much as on absolute novelty. Showing awareness of existing tools (ANBDD, Cartofriches, MDA) and positioning against them is still advisable.
- The beta.gouv / Mon Diag Artif lineage (a State startup) shows that "artificialisation diagnosis per territory" has already been productised nationally.

### Open points
- The theme and winners of the 2024 (2nd) edition were not found online; NormanDTour is unverified.
- The 2023 winners list was not found (PRIORENO unverified).
- GitHub hackathon repositories, GBIF Ebbe Nielsen Challenge entries, Data for Good projects, EIG biodiversity projects and other regions' biodiversity datathons were not checked (not checked for lack of time).

---

## Existing Normandy-specific restoration prioritisation exercises

### In short
Normandy already has several official priority-setting frameworks:
- SRADDET TVB priority sectors and corridors to restore;
- the 2026 TVB/trame noire remodelling;
- the regional biodiversity strategy 2030 (56 objectives);
- the SNAP regional plan (2022–2024, then 2025–2027);
- the COP Normandie roadmap (hedges, peatlands);
- AESN's 12th programme and the PAPARCE/PLAGEPOMI continuity priorities;
- GIP Seine-Aval REPERE for the estuary;
- Région FEDER calls (TVB works, Normandie Haies);
- EPFN's brownfield decision tool.

Most are framework- or list-based. None found offers an open, interactive, multi-criteria prioritisation across habitats.

### Sources
- SRADDET TVB with "secteurs d'actions prioritaires" and "corridors écologiques d'intérêt régional à restaurer"; the 2026 TVB works call; the June 2026 TVB/trame noire update. — [Région, to check](https://rn136.normandie.fr/sites/default/files/2025-12/aap_travaux_tvb_2026_vf.pdf); [TVB note](https://normandie-a-la-carte.normandie.fr/tvb/tvb_note_accompagnement_donnees.pdf)
- A 2024 Région call supports EPCI TVB strategies, in line with the SRB target of 100% of EPCIs with a TVB action plan by 2030. — [Région AAP stratégie TVB 2024](https://www.normandie.fr/sites/default/files/2024-03/aap_strategietvb_2024_0.pdf); [SRB objectives](https://rn136.normandie.fr/sites/default/files/2023-05/srb-normandie-fiches-objectifs.pdf)
- SNAP regional plan 2022–2024 (update 2025–2027) with lists of planned strict-protection areas per department. — [DREAL](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/extension_du_reseau-ap_14.pdf); [Aides-territoires](https://aides-territoires.beta.gouv.fr/aides/proteger-et-restaurer-les-espaces-naturels-25/)
- AESN 12th programme 2025–2030, actions F.1 (river dynamics) and F.2 (wetlands and coast). — [AESN](https://ecoentreprises-france.fr/app/uploads/2024/12/AESN_12EPROGRAMME_PROGRAMME.pdf). PAPARCE priority works (Sept 2023) and PLAGEPOMI 2022–2027. — [data.gouv.fr](https://www.data.gouv.fr/datasets/ouvrages-prioritaires-sur-le-bassin-seine-normandie); [PLAGEPOMI](https://www.drieat.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/projet_plagepomi_complet_2022-27.pdf)
- GIP Seine-Aval REPERE (estuary restoration priorities, 5 orientations). — [CSRPN 2023](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/avis_csrpn_2023-05-08_estuaire_seine_gipsa.pdf)
- "Opération Normandie Haies" 2026 (zero net loss by 2030). — [Région](https://www.normandie.fr/sites/default/files/2026-02/aap_operation_normandie_haie_2026_0.pdf)
- EPFN brownfield observatory with a vocation decision tool. — [Info COP (to check)](https://www.prefectures-regions.gouv.fr/irecontenu/telechargement/141551/1029345/file/Info%20Cop)
- PNR-level work: Normandie-Maine bocage observatory (BD Bocage 1947–2020); the Marais du Cotentin et du Bessin park communicates on pond restoration (Sept 2025). — [Fédération des PNR](https://www.parcs-naturels-regionaux.fr/sites/federationpnr/files/document/centre_de_ressources/Normandie%20Maine%20bocage.pdf); [PNR MCB press release](https://parc-cotentin-bessin.fr/sites/default/files/inline-files/CP_20250926_RESTAURATION_MARES_PNRMCB.pdf)

### Our reading
- **Any P1 MVP should be positioned as operationalising these frameworks**, for example "turn the SRADDET priorities into a ranked, explainable list per EPCI, updated with 2026 data". Presenting it as an alternative to them is riskier.
- **Timing:** the Région's new TVB/trame noire model and France's national restoration plan are in flight. A datathon tool that can ingest them later is more credible.

### Open points
- CEN Normandie's five-year plan and site priorities were not checked.
- PNR charters' priority maps (Perche, Boucles de la Seine Normande) were not checked.
- AESN 12th-programme priority maps were not found.

---

## Overall: what is already done, and where the gaps are

### In short
**ANBDD's per-EPCI indicator app is the single most important "already done" reference.** It covers baseline indicators relevant to C, D, E, F, G, I and N, so teams should reuse rather than recompute it. Cerema's Cartofriches mutability index pre-empts A. Official lists pre-empt F, and specialist bodies cover M. The clearest white spaces are J (needs × efforts), L (public what-if simulator), N (equine–grassland link), the Normandy-wide restorable-wetlands layer (G), the ecological-quality balance of land take (I), and the Normandy gap map (H, subject to CarHab coverage).

### Sources
- ANBDD's 8 per-EPCI indicators:
  - land cover;
  - land consumption;
  - water ecological status;
  - hedges;
  - permanent grassland;
  - wetlands;
  - terrestrial fragmentation;
  - river fragmentation.
  - Planned: pesticides, coastal artificialisation. — [ANBDD](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- Cartofriches renaturation index for all brownfields without a project. — [Cerema documentation](https://doc-datafoncier.cerema.fr/doc/export/511)
- Seine-Normandie priority works list. — [data.gouv.fr](https://www.data.gouv.fr/datasets/ouvrages-prioritaires-sur-le-bassin-seine-normandie)
- GIP Seine-Aval REPERE. — [CSRPN 2023](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/avis_csrpn_2023-05-08_estuaire_seine_gipsa.pdf)

### Our reading
Summary table. These are judgements based on what was found; "not found" means not found in this search, not proven absent.

| Piste | Closest existing equivalent | Status / date | Originality |
|---|---|---|---|
| A Friches → Nature | Cerema Cartofriches mutability index (renaturation); EPFN observatory decision tool; Mutafriches/Bénéfriches; IdF REGREEN | Live (Cartofriches data Mar–Jul 2026; EPFN updated 2026) | LOW–MEDIUM |
| B Multi-criteria priority map | SRADDET TVB priority sectors; 2026 TVB/trame noire update; national restoration plan (draft 2026); NaturaConnect/Nature-3B (embargo to end 2026) | Frameworks; no open adjustable tool found | MEDIUM |
| C Bocage 70 yrs | DREAL statistical indicator (since 2002, updated Nov 2024); ANBDD hedge density/connectivity per EPCI; DNSB/BD Haie; PNR NM BD Bocage; national Observatoire de la haie not live | Monitoring done; targeting less so | MEDIUM |
| D EPCI bulletin | ANBDD EPCI indicator app (since Oct 2022); Observatoire normand des transitions (Oct 2023); SGPE regional COP indicators (Oct 2025) | Live | LOW (MEDIUM if effort/COP-at-EPCI focus) |
| E Water × agriculture | AESN état des lieux; ANBDD water status per EPCI; Géophyto (department level, 2015–2022); AREAS/CATER diagnostics | Pieces exist, not integrated | MEDIUM–HIGH |
| F River continuity | ROE/ICE; PAPARCE priority works (Sept 2023); PLAGEPOMI 2022–27; ANBDD river fragmentation | Official and mature | LOW–MEDIUM |
| G Restorable wetlands | Potential-wetland models; ANBDD wetland indicator; Brittany FMA 2021 analysis | No Normandy layer found | MEDIUM–HIGH |
| H Protection gaps | PatriNat national diagnostics (2019/2020/2023); SNAP regional plan; CarHab (Normandy coverage uncertain) | National only | MEDIUM–HIGH |
| I What concrete ate | MDA (quantity), Région land-consumption app, ANBDD land take; ONB-type ZNIEFF loss indicators elsewhere (CLC 1990–2012) | Quality balance not found in Normandy | MEDIUM–HIGH |
| J Coherence needs × efforts | Fonds vert open list (no map); national financing reports | Not found | HIGH |
| K Citizen commune sheet | Atlas d'ODIN, INPN Espèces, ABC PDFs, ANBDD resource sheets | Species-centred only | MEDIUM |
| L What-if simulator | Graphab (expert desktop), MDA trajectory, Bénéfriches | No public simulator found | HIGH (feasibility risk) |
| M Coast & estuary | GIPSA REPERE; ROL coastal app; Cerema 2050/2120 shorelines | Specialist tools live | LOW–MEDIUM |
| N Horses & grasslands | IFCE sector reports; EIP-AGRI Equi-Pâture (2016–17); EquuRES label | No spatial study found | HIGH |

Further inferences:
- **Combinations that maximise originality while reusing what exists:**
  - B + L: an adjustable priority map with a what-if module;
  - G + I: restorable wetlands plus the "what concrete ate" loss balance;
  - J built on ANBDD indicators as the "needs" axis;
  - C (targeting) + L.
- **Least advisable as standalone pistes:** D and F (duplication), and A unless reframed around regional network prioritisation and ZPR.
- **Expert jury members may come from ANBDD, DREAL, the Région or EPFN** (jury composition not verified). Explicitly citing and building on their tools (ANBDD app, Cartofriches, SRADDET TVB, REPERE) is likely to be read as rigour rather than lack of originality.

### Open points
- Several checks could not be done in the time available:
  - Afac-Agroforesteries tools;
  - citizen-science apps (Biolit, Sentinelles de la nature, Faune-Normandie);
  - GitHub/GBIF/Data for Good/EIG hackathon projects;
  - AESN 12th-programme priority maps;
  - seabed habitat tools;
  - CarHab coverage per Normandy department;
  - CEN Normandie plans;
  - the 2024 Datathon Normandie edition.
- Several Normandy PDFs (DREAL, Préfecture, Région subdomains) could not be opened, so their figures should be confirmed before quoting them in the pitch.
