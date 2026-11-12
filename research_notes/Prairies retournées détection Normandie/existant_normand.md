# Existing Normandy indicators, studies, tools and rules on permanent-grassland loss and ploughing (retournement des prairies permanentes)

Status as of 18 October 2026. Each finding says how it was checked:
- **[full text]**: I read the primary document itself.
- **[web page]**: I read the web page; the wording below is a paraphrase, not checked line by line.
- **[excerpt]**: I only saw the figure in a search-engine excerpt, not in the document. Treat it as unverified.

DREAL Normandie PDFs return HTTP 403 when opened online. I downloaded four small PDFs one by one (two CSRPN motions, one DREAL decision, the ANBDD hedge sheet) and read their full text. I downloaded no datasets.

---

## 1. The Agreste 2021 study: what it measures and with which data

### In short
The study is Agreste Études Normandie n°6 (Sept. 2021, DRAAF Normandie / SRISE). It measures loss of **all grassland** (permanent plus temporary) between 2008 and 2019. The source is **OSCOM**, the DRAAF's annual land-cover database at **commune** level, built by overlaying several sources. Teruti is not used. The study then attributes losses to farming systems using reconstructed farms from **ASP/PAC declarations plus BDNI cattle data (2007–2018)**. The study publishes only department-level tables and smoothed maps. I found no open download of the OSCOM Normandie tables, only a metadata record on GéoNormandie.

### Sources
- **Title.** "Les prairies en Normandie entre 2008 et 2019 – Le retournement de prairies : en faveur de quels systèmes agricoles sur le territoire normand ?", Agreste Études n°6, Sept. 2021. Author Y. Gourlaouen, maps X. Leclair, ISSN 2728-9664. [full text] — [DRAAF Normandie PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Headline.** Normandy lost about 11% of its agricultural grassland between 2008 and 2019. The PDF prints "11 1%", a typo. [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Stock and loss.** According to OSCOM, grassland covered **809,000 ha in 2019**, out of about 2 million ha of agricultural land. The loss over 2008–2019 was **103,000 ha** in the text. Arable land gained **almost 89,000 ha**. "Artificialisation explique globalement le reste". [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Method box (Encadré 3), OSCOM 2008–2019 table.** It covers "Prairies et autres sols agricoles", with destination shares (to arable / to artificialisation):

  | Department | Change (ha) | To arable | To artificialisation |
  |---|---|---|---|
  | Calvados | −21,632 | 76% | 24% |
  | Eure | −9,928 | 71% | 29% |
  | Manche | −30,098 | 84% | 15% |
  | Orne | −21,299 | 94% | 6% |
  | Seine-Maritime | −24,842 | 80% | 20% |
  | **Normandie** | **−107,799** | **82%** | **18%** |

  Over the same period, artificialised land rose by +22,421 ha, forest and semi-natural land fell by −3,254 ha, and arable land rose by +88,641 ha. Grassland makes up 96% of all agricultural land-cover changes. "18% des prairies sont artificialisées" after netting out flows from semi-natural land. In OSCOM, prairies = permanent + temporary grassland. [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **West-east split.** Calvados, Manche and Orne lost 71,000 ha, which is **69%** of the regional loss, and gained 62,000 ha of arable land. In the west, ploughed grassland went to cereals and oilseeds. In the east (mainly Seine-Maritime and the eastern Pays de Bray), it went to industrial crops (sugar beet, flax) and potatoes. [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Which farms.** Three quarters of ploughed grassland came from specialised dairy farms and the rest from mixed dairy farms. The arable land gained went half to field-crop farms, a third to mixed beef farms, and the rest to mixed dairy farms. Example: in Calvados, dairy lost about 21,000 ha of grassland and field-crop farms gained about 8,000 ha. [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Maps.**
  - (a) A smoothed map of grassland loss. It uses a Biweight kernel on a 1 km² hexagonal grid with a 7.5 km radius.
  - (b) A map of **each EPCI's dominant agricultural shift, 2007–2018**. It crosses the system losing the most grassland with the system gaining the most arable land. "Pas ou peu de perte" means less than 1 ha of grassland lost per km².
  - (c) A commune map (communes losing more than 1 ha/km²) showing the main use of lost grassland: arable, artificialisation, or forest/semi-natural. A use counts as dominant if it accounts for at least 2/3 of the loss.

  [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Caveat on system splits.** Farms were reconstructed from ASP PAC surfaces and BDNI cattle data using an Inosys-inspired typology. The DRAAF says the per-system estimates "pouvant être fragiles, même par département", but considers each system's weight reliable. OSCOM is described as "exhaustif mais n'apporte pas d'information sur les systèmes". The study continues joint Chambre régionale d'agriculture / DRAAF work from 2016 and 2018 ("Les trajectoires de la polyculture-élevage…"). [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **Related DRAAF studies** (titles from the same PDF):
  - Agreste Études n°2 (Aug. 2020), land consumption 2008–2018.
  - Agreste Études n°3 (Nov. 2020), use of artificialised agricultural land 2009–2018.
  - Agreste Analyse n°1 (June 2017).
  - A "Présentation de l'OSCOM 2008-2019 : consultation, couches et métadonnées".

  [full text] — [same PDF](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **How OSCOM is built.** The method was started by DRAAF and DREAL Haute-Normandie and the DDTM 27 and 76. It overlays IGN BD TOPO and BD Forêt, the RPG, and MAJIC land-tax files. [excerpt] — [DREAL ARA OSCOM doc](https://www.auvergne-rhone-alpes.developpement-durable.gouv.fr/IMG/pdf/Oscom_Dreal-2.pdf)
- **Where OSCOM is catalogued.** A DDT de l'Orne comparison of land-cover databases (June 2022) points to an OSCOM metadata record on geonormandie.fr. I could not confirm a download link. [excerpt] — [DDT 61 comparatif BDD occupation du sol](https://www.orne.gouv.fr/contenu/telechargement/13110/106734/file/20220617_dia_comparatif-bdd-occupation_du_sol_cle267a3b.pdf)

### Our reading
- Our "82% of losses went to arable land" figure comes from this OSCOM table (2008–2019, all grassland, net flows). It mixes temporary and permanent grassland and is a net balance, not parcel-level ploughing events. Parcel-level ploughing would need a year-to-year RPG comparison.
- The DRAAF already maps grassland loss at commune, smoothed-grid and EPCI-typology level, but only up to 2019 and only as static PDF maps. An annual EPCI or commune ploughing indicator for 2015–2025 from open RPG data would therefore extend this work in time and openness rather than duplicate it. The positioning would be "the follow-up to Agreste 2021".

### Open points
- I could not confirm whether OSCOM Normandie tables (commune × year × land-cover class) are openly downloadable. GéoNormandie has a metadata record, but I did not verify access. Ask DRAAF SRISE: srise.draaf-normandie@agriculture.gouv.fr, listed in the PDF.
- I found no Agreste update of this study after 2019.

---

## 2. What ANBDD and regional observatories publish per EPCI

### In short
ANBDD publishes a regional and department sheet, "Évolution de la Surface Toujours en Herbe (STH) dans la SAU en Normandie" (2009–2019 and 2000–2020). It also runs an online **"Indicateurs territoriaux de la biodiversité"** tool that generates per-**EPCI** reports, downloadable as PDF with raw data in **Excel**. One of its indicators is the "évolution des prairies permanentes dans la SAU". This is the closest existing product to our module, so we must check it in the tool before claiming novelty.

### Sources
- **ANBDD STH sheet, figures.**
  - 804,900 ha of STH in 2020, which is 39% of SAU, ranking 6th of 13 regions (France: 34%). STH covers 27% of the region's total area.
  - 2009–2019: STH −54,000 ha (−6.3%, against −0.4% nationally). The STH share of SAU fell from 40.4% to 38.8%. SAU fell by 52,000 ha.
  - 2000–2020: STH −151,400 ha, share of SAU from 44% to 39%.
  - 2020 department shares of STH in SAU: Manche 54%, Calvados 45%, Orne 43%, Seine-Maritime 29%, Eure 20%.

  The scale is region and department, not EPCI. It cites the recensement agricole and OSCOM. No raw data is offered on the page. Image paths suggest an upload in June 2023. [web page] — [ANBDD STH page](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-normands-de-la-biodiversite/evolution-de-la-surface-toujours-en-herbe-sth-dans-la-surface-agricole-utile-sau-en-normandie/); [PDF fiche](https://www.anbdd.fr/wp-content/uploads/2023/06/Evolution-STH-SAU.pdf)
- **ANBDD STH definition.** STH means permanent grassland, sown or natural, older than 5 years. INSEE uses a 6-year threshold. [excerpt] — [ANBDD PDF](https://www.anbdd.fr/wp-content/uploads/2023/06/Evolution-STH-SAU.pdf)
- **ANBDD "Indicateurs territoriaux de la biodiversité".** Regional indicators broken down by EPCI. The user picks an EPCI and an indicator, then clicks "Générer le rapport". Output is a PDF report, with raw data downloadable as Excel.
  - Current indicators: change in main land-cover types; land consumption; ecological status of surface water bodies; hedge density and connectivity; **change in permanent grassland within SAU**; wetlands; fragmentation of natural areas; fragmentation of watercourses.
  - Planned: coastal artificialisation, pesticide use, a key-figures summary.
  - The page does not name data sources or reference years. Contact: ANBDD chargée de mission scientifique.

  [web page] — [ANBDD indicateurs territoriaux](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-territoriaux-de-la-biodiversite/)
- **ANBDD land-cover indicator page.** It exists. I did not open it. — [ANBDD occupation du sol](https://www.anbdd.fr/biodiversite/connaissance/les-indicateurs-normands-de-la-biodiversite/occupation-du-sol/)
- **Chambre d'agriculture (Agriscopie).** STH was 37% of regional agricultural area in 2022, and 46% in Calvados, Manche and Orne. [excerpt] — [Chambre fiche 3 Terre](https://refonte-normandie.chambres-agriculture.fr/fileadmin/user_upload/Normandie/506_Fichiers-communs/PDF/AGRISCOPIE/Panorama_agriculture/fiche_3_-_Terre.pdf)
- **Chambre (élevage & eau).** STH fell 17% since 2000 in Normandy, but permanent grassland still covers 36% of SAU. [excerpt] — [Chambre PEP élevage et qualité eau](https://refonte-normandie.chambres-agriculture.fr/fileadmin/user_upload/National/FAL_commun/publications/Normandie/pep-elevage-et-qualite-eau.pdf)
- **INSEE / ANBDD (2020).** STH covers 21% of Normandy's territory, against 14% in provincial France. [excerpt] — [Insee Analyses Normandie n°80](https://www.insee.fr/fr/statistiques/4629011)
- **Long series (Agreste RA).** STH share of Normandy SAU: 68.2% (1970), 52.6% (1988), 46.0% (1998). [excerpt] — [HAL INRAE](https://hal.inrae.fr/hal-02681249/document)

### Our reading
- **Redundancy risk.** If the ANBDD EPCI indicator already gives the net change in permanent grassland in SAU per EPCI from RPG or RA, a simple "net STH change per EPCI" module would duplicate it. The team adds value by measuring things it does not:
  - (i) **gross** ploughing flows at parcel level (permanent-grassland parcel in year N that becomes an arable code in year N+1), separate from new grassland;
  - (ii) a **destination split** in one map with the artificialisation module: arable vs artificialised vs other, updating the Agreste 82/18 split per EPCI and per year;
  - (iii) overlays with sensitivity zonings: Natura 2000 / prairies sensibles, wetlands, drinking-water catchments, erosion slopes, hedges.
- Sources disagree on STH stock and share: ANBDD 39% of SAU (2020), Chambre 37% (2022) and 36%, OSCOM 809,000 ha (including temporary grassland), BCAE1 ratio 32.29% (PAC-declared permanent grassland only). The cause is different definitions (STH, permanent grassland, all grassland) and denominators (SAU, total area, PAC-eligible area). A pitch must name its definition.

### Open points
- I could not see which source and years the ANBDD EPCI "prairies permanentes" indicator uses (RPG? RA 2010/2020?). Open the tool and download the Excel for one EPCI to check.
- I found no Normandy "ODIN" or "Observatoire normand des transitions" grassland indicator in what I searched. Its existence and content are unverified.

---

## 3. BCAE 1 in Normandy and publicity of ploughing authorisations

### In short
Normandy had the **worst** permanent-grassland ratio decline in France in 2023. This put the region under the **ban regime** (late 2023), with reseeding obligations. In 2024, EU Delegated Regulation 2024/1235 allowed the 2018 reference to be recalculated (34.93% to 32.94%). The ban was then lifted retroactively from 1 Jan 2024.

Since then:
- 2025: ratio −1.89%, no regime.
- 2026: ratio **32.29% vs reference 32.94%, −1.97%**, no regime. Permanent grassland is nevertheless down **59,703 ha (−8.9%) since 2018**.
- Thresholds (2026, as reported): authorisation regime above 4% decline; reimplantation/ban threshold raised from 5% to **10%** by décret 2026-348 of 7 May 2026.

Individual BCAE 1 authorisations from DDT(M) are **not published**. Environmental "examen au cas par cas" decisions for ploughing of 4 ha or more (rubrique 46) **are published** by DREAL Normandie as PDFs, which name the petitioner and the cadastral parcels.

### Sources

**Ratio series and regime**
- **2026 arrêté.** Arrêté of 11 Sept. 2026 (JORF n°0218, 18 Sept. 2026, NOR AGRT2624078A) sets the 2026 ratios.
  - Normandy: annual ratio **32.29%**, reference ("2018 retraité") **32.94%**, change **−1.97%**.
  - "aucune région n'est concernée par la mise en place des obligations de compensation", and none by the reconversion obligations of art. 48(3) of Reg. (EU) 2022/126.
  - Other regions: Bretagne −3.53% (closest to the threshold), Hauts-de-France −1.93%, PACA −2.18%.

  [web page] — [Légifrance JORFTEXT000054855099](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054855099)
- **2026 area figures.** Permanent grassland **614,166 ha** out of **1,901,944 ha** of SAU. Down **59,703 ha (−8.9%) since 2018**, from 673,869 ha. [web page] — [Réussir, 23 Sept. 2026](https://www.reussir.fr/lait/prairies-permanentes-2026-pas-dobligations-de-compensation-ni-de-reconversion-pour-2026); [Transformez votre lait, 21 Sept. 2026](https://www.transformation-laitiere.fr/prairies-permanentes-ratios-2026-bretagne-seuil-4-pourcent/)
- **2025.** Normandy ratio change −1.89%, "la Normandie n'est pas en régime de compensation ou d'interdiction". [web page] — [DDTM Eure, updated 5 Dec. 2025](https://www.eure.gouv.fr/Actions-de-l-Etat/Agriculture/L-actualite-de-l-agriculture/Maintien-des-prairies-permanentes)
- **2025 arrêté.** Dated 26 Dec. 2025 (JO 28 Dec. 2025). Normandy annual ratio **32.32%**. [excerpt] — [Légifrance JORFTEXT000053177444](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000053177444/)
- **2026 thresholds** (as reported by trade press):
  - A decline of more than **4%** triggers prior individual authorisation with compensation in N+1.
  - A decline of more than **10%** triggers the reimplantation/ban obligations. This second threshold was 5% until 9 May 2026.
  - Décret 2025-1364 (26 Dec. 2025) set the 5% threshold. **Décret 2026-348 (7 May 2026)** raised it to 10%.
  - The article flags an internal inconsistency in D.614-45: §II ties reimplantation to 4%, §IV to 10%.

  [web page] — [Transformez votre lait](https://www.transformation-laitiere.fr/prairies-permanentes-ratios-2026-bretagne-seuil-4-pourcent/). Réussir also quotes a Chambre d'agriculture de Normandie adviser on the 10% ban threshold. — [Réussir](https://www.reussir.fr/lait/prairies-permanentes-2026-pas-dobligations-de-compensation-ni-de-reconversion-pour-2026). *I did not verify these décrets on Légifrance.*
- **Conflicting earlier thresholds.**
  - Réussir: authorisation regime at a 2–5% decline, ban above 5% (start of CAP 2023-27). [excerpt] — [Réussir](https://www.reussir.fr/chevre/pac-et-prairie-permanente-quelles-sont-les-regles-de-retournement)
  - Réussir, Dec. 2024: 3–5%. [web page] — [Réussir](https://www.reussir.fr/lait/prairies-permanentes-larrete-sur-lassouplissement-des-regles-est-sorti)
  - DDTM Eure, Dec. 2025: compensation at 4–5%, ban above 5%. [web page] — [DDTM Eure](https://www.eure.gouv.fr/Actions-de-l-Etat/Agriculture/L-actualite-de-l-agriculture/Maintien-des-prairies-permanentes)

  Thresholds have changed several times. Cite the 2026 version with its date.
- **2023 ban.** DRAAF Normandie, "Prairies permanentes : la Normandie passe en régime d'interdiction" (22 Nov. 2023). The 2023 ratio was more than 5% below the 2018 reference (arrêté of 31 Oct. 2023, art. D614-45 CRPM). Consequences:
  - farmers had to **reconvert** part of the parcels converted during the previous two campaigns, notified by DDT(M);
  - a general ploughing **ban**, with exceptions only through a DDT(M) conversion authorisation tied to compensation;
  - a target of bringing the degradation back under 4.5%;
  - a reseeding deadline of 31 Dec. 2024.

  The page has no maps or lists of parcels or farms. [web page] — [DRAAF Normandie](https://draaf.normandie.agriculture.gouv.fr/prairies-permanentes-la-normandie-passe-en-regime-d-interdiction-a3672.html)
- **Exemptions under the 2023–24 ban.**
  - No reseeding obligation for farms that ploughed less than 0.5 ha.
  - Exemptions possible for farms with more than 75% permanent grassland.
  - Young or new farmers may convert less than 25% of their permanent grassland.
  - Deadlines: 2 Jan. 2024 (conversion requests), 15 Jan. 2024 (derogation requests), 31 Dec. 2024 (reseeding).

  [web page] — [Coordination Rurale Normandie, 30 Nov. 2023](https://www.coordinationrurale.fr/nos-cr-locales-actualites/normandie/regime-dinterdiction-de-retournement-des-prairies-permanentes-en-normandie/)
- **Size of the 2023 decline: sources conflict.**
  - CSRPN motions: "−7.43% selon l'arrêté du 31 octobre 2023". [full text] — [CSRPN motion 2023-12-12](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2023-12-12_prairies.pdf)
  - Réussir: "−6.45%" (2018–2023). [web page] — [Réussir Dec. 2024](https://www.reussir.fr/lait/prairies-permanentes-larrete-sur-lassouplissement-des-regles-est-sorti)

  Unresolved. Check the 31 Oct. 2023 arrêté on Légifrance.
- **Recalculation.** EU Delegated Regulation **2024/1235 of 12 March 2024** changed the reference-ratio method. Normandy's 2018 ratio went from **34.93% to 32.94%**. The method also counted areas still in grassland on the ground but no longer in the PAC in 2023. The 2018–2023 change fell to **−1.85%**, against −7.43%, so no regime applied in any region. The CSRPN states: "Ce moindre déclin … résulte d'une modification de l'indicateur. Sur le terrain, le recul est toujours le même." [full text] — [CSRPN motion 2024-12-12](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf)
  - Conflict: Réussir gives the recalculated reference as 32.84% and the recalculated change as −0.79%. The arrêté of 25 Nov. 2024 lifted the ban retroactively from 1 Jan. 2024. [web page] — [Réussir, 3 Dec. 2024](https://www.reussir.fr/lait/prairies-permanentes-larrete-sur-lassouplissement-des-regles-est-sorti). The 2026 Légifrance annex uses **32.94%**, so prefer that value.
- **History under the previous CAP.** A late-2017 arrêté found Normandy's ratio −3.55% (Hauts-de-France −4.68%) below the reference, which triggered prior authorisation for ploughing in 2017–18. [excerpt] — [Terre-net](https://www.terre-net.fr/reglementation/article/132187/la-normandie-et-les-hauts-de-france-epingles-pour-retournement-excessif)

**Other protections, independent of the ratio**
- **"Prairies sensibles" (BCAE 9).** Grassland in Natura 2000 zones. It cannot be ploughed and can be checked on the RPG in TéléPAC or on the Géoportail layer "prairies-sensibles-BCAE".
- **Wetland grassland.** Mapped on the DREAL / Géo-IDE viewer.
- **Environmental code, art. R122-2.** Converting more than 4 ha of grassland requires a case-by-case examination.
- **Environmental code, art. L414-2.** Grassland in Natura 2000 that is not classed "sensible" still needs a Natura 2000 impact assessment before ploughing.
- **Permanent status.** Grassland becomes permanent after 5 full years (from the 6th declaration), even if ploughed and reseeded.

[web page] — [DDTM Eure](https://www.eure.gouv.fr/Actions-de-l-Etat/Agriculture/L-actualite-de-l-agriculture/Maintien-des-prairies-permanentes)
- **Other frameworks.** Even without a BCAE 1 regime, permission may be required in nitrate-vulnerable zones, drinking-water catchment areas or Natura 2000. [web page] — [Réussir 2026](https://www.reussir.fr/lait/prairies-permanentes-2026-pas-dobligations-de-compensation-ni-de-reconversion-pour-2026)
- **Nitrates.** The 6th regional nitrates action programme for Normandy (arrêté of 30 July 2018) bans ploughing grassland within **35 m of watercourses**, with derogations (young farmer, long rotation). [excerpt] — [Orne regulation table](https://www.orne.gouv.fr/contenu/telechargement/9849/90429/file/tab_reglementation_prairies_v2_cle781337.pdf). The 7th PAR is under consultation or adopted. [excerpt] — [AELB opinion on PAR7](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/5-avis_aelb_projetpar7_nitratenormandie.pdf)

**Publicity of authorisations and decisions**
- **BCAE 1 (DDT(M)).** No source shows publication of individual authorisations or reconversion notifications. The DRAAF and DDTM pages give only forms, deadlines and contacts, with no lists or maps. [web page] — [DRAAF](https://draaf.normandie.agriculture.gouv.fr/prairies-permanentes-la-normandie-passe-en-regime-d-interdiction-a3672.html); [DDTM Eure](https://www.eure.gouv.fr/Actions-de-l-Etat/Agriculture/L-actualite-de-l-agriculture/Maintien-des-prairies-permanentes)
- **Environmental case-by-case (rubrique 46 a).** These **are public**. Example: decision of 8 April 2025 on ploughing about **10 ha** of permanent grassland at Montigny (76).
  - The grassland had been uncultivated for more than 20 years, followed by wheat, barley, rapeseed and flax.
  - The decision lists cadastral parcels, identified as permanent grassland in the **RPG 2023**, names the individual petitioner, and records a ZNIEFF II and an ecological corridor.
  - Outcome: **subject to environmental assessment** (biodiversity, hydraulic regulation, soils).
  - Stated grounds: "le rôle essentiel des prairies permanentes pour la protection des ressources en eau, la prévention des inondations et l'érosion des sols, la biodiversité et la captation du CO2".

  [full text] — [DREAL decision PDF](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/d_2025_5772_retournement_prairies_permanentes_montigny.pdf)
  - A similar 2025 decision exists for Écouché-les-Vallées (61). [excerpt] — [DREAL PDF](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/d_2025_5764_retournement_prairies_permanentes_echouche_les_val_signe.pdf)
  - The Montigny decision cites request "n° 2025-5764", while its file is named "5772". This is a numbering oddity in the source.
  - Rubrique 46 covers grassland conversion totalling 4 ha or more, even over several years or parcels. [excerpt] — Hauts-de-France DREAL decisions, e.g. [2025-8647](https://www.hauts-de-france.developpement-durable.gouv.fr/IMG/pdf/2025-8647-decision.pdf)

**Open data that can detect ploughing**
- **RPG (IGN / ASP, Licence Ouverte 2.0, annual).** Since the **2024 edition** it has 8 databases, including RPG Parcelles, RPG Îlots (anonymous), RPG GCP (groups: arable / permanent crops / permanent grassland / wooded), **RPG PP – Prairies permanentes**, RPG ZDH (homogeneous density zones on permanent grassland), SNA (non-agricultural elements: hedges, trees), IAE and BIO. The data is anonymised. Rules are set by MASA instruction DGPE/SDGP/2022-106. Last update shown: 29 Sept. 2026. [web page] — [data.gouv.fr RPG](https://www.data.gouv.fr/datasets/rpg)
- **Pressure-zone maps.** Indicative ministry maps of the zonings used to regulate ploughing exist, for example in Hauts-de-France in 2026. [excerpt] — [DREAL HdF tuto carto zonages prairie](https://www.hauts-de-france.developpement-durable.gouv.fr/IMG/pdf/2026-tuto_explication_carto_zonages_prairie.pdf)

### Our reading
- The regional ratio is a **net, region-wide, PAC-declared** indicator. It says nothing about where ploughing happens, and its method has changed: 2018 reference recalculated, thresholds moved from 5% to 10%. It can show "no problem" (−1.97%) while permanent-grassland area falls 8.9% since 2018. This gap is the module's main positioning argument, and the CSRPN makes the same point.
- **Unmet demand.** The CSRPN has asked the DRAAF twice (2023, 2024) for "un indicateur de suivi des retournements / implantations de prairies publié chaque trimestre". A public, annual, EPCI and commune ploughing indicator built on open RPG directly answers a documented request from the regional scientific council.
- **Validation data.** Published rubrique 46 decisions (4 ha or more) can serve as ground-truth cases for testing detection. They should not be republished with petitioner names.

### Open points
- No Normandy figures on the number or area of BCAE 1 authorisations or 2024 reseeding. Not published as far as I found.
- I did not verify décrets 2025-1364 and 2026-348 or the exact current text of art. D.614-45 on Légifrance.
- I did not check the full set of Normandy ratio values for 2019–2022 (old method) or the 2024 values.
- I did not verify the attributes of RPG PP (for example whether it flags "sensible" grassland or the year it became permanent).

---

## 4. Links with other pressures (hedges, erosion, nitrates, biodiversity)

### In short
The best-documented links are:
- **hedges**: dense bocage depends on grassland, and long-term hedge loss is concentrated in the dairy west;
- **nitrates**: AESN says new nitrate-degraded water points lie mainly in grassland-ploughing zones, "notamment en Normandie";
- **erosion and muddy floods** in Pays de Caux: ploughing is cited as aggravating, with AREAS as the reference body;
- **the CSRPN's list of ecosystem services**.

I found no Normandy-specific farmland-bird figures.

### Sources
- **ANBDD hedge indicator (update 2024).**
  - **158,433 km** of hedges and **53 m/ha** (France 27 m/ha). Normandy ranks 3rd among regions. Manche has **96 m/ha**, 1st department in France. Coherence index 39%.
  - Densities are highest in agricultural land (63 m/ha), especially **grassland (92 m/ha)** and heterogeneous agricultural zones (86 m/ha).
  - Bocage density historically "liée au développement des prairies … et donc de l'élevage bovin laitier".
  - Long-term losses (regression trend): Manche **−1,208 km/yr (1972–2015)**, Orne −829 km/yr and Calvados −654 km/yr (1972–2016), Seine-Maritime −73 km/yr (2003–2015), Eure −70 km/yr (2005–2015).
  - Coherence fell 23% in Calvados over 44 years.
  - Sources: Dispositif de Suivi des Bocages 2004–2022, and a DREAL 2020 report (W. Latizeau).

  [full text] — [ANBDD hedge sheet 2024](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/lineaireshaies-normandie-2024_anbdd.pdf)
- **CSRPN 2024 on hedges.** It asks the DRAAF to study the disappearance of grassland "et du linéaire des haies existantes, souvent victimes collatérales de retournements de prairies". [full text] — [CSRPN 2024](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf)
- **Nitrates (AESN annual review, Nov. 2021).** "les dégradations liées aux nitrates sont en hausse". New degraded sites "se trouvent principalement dans les zones de retournement de prairies, et notamment en Normandie". About **90 stations** were downgraded for nitrates in 2021. Of 512 stations, 58% were in good status. The article also notes worse green-algae strandings (Courseulles-sur-Mer). [web page] — [Réussir, 10 Dec. 2021](https://www.reussir.fr/agriculture-massif-central/en-seine-normandie-ameliorer-leau-en-additionnant-les-politiques)
- **Payments for environmental services.** AESN-funded schemes to keep grass. Le Havre Seine Métropole tested them on 4 of its 8 catchment basins, paying **13 to 132 €/ha/yr** depending on the grass share of SAU. [excerpt] — [Banque des Territoires](https://www.banquedesterritoires.fr/experience/le-havre-seine-metropole-teste-les-paiements-pour-services-environnementaux-76)
- **Erosion in Pays de Caux.** Ploughing grassland and farm enlargement "accentuent encore aujourd'hui les phénomènes érosifs". [excerpt] — Ouvry, Richet & Saunier, *Sciences Eaux & Territoires* 2019, quoted in [Lheriteau, EGS](https://afes.fr/wp-content/uploads/2023/04/EGS_14_3_EGS_14_3_Lheriteau.pdf). AREAS was created in 1985 by the Chambre d'agriculture to deal with runoff, erosion and muddy floods. [excerpt] — [AREAS poster JMS 2024](https://afes.fr/wp-content/uploads/2025/03/Poster_JMS2024_04.12-05.12_AREAS.pdf). Runoff in autumn and winter causes erosion, muddy floods and turbidity. [excerpt] — [Lheriteau, EGS](https://afes.fr/wp-content/uploads/2023/04/EGS_14_3_EGS_14_3_Lheriteau.pdf)
- **CSRPN 2023: ecosystem services of grassland.**
  - Pollinators and earthworms.
  - Groundwater recharge and drinking-water quality.
  - Flood peak reduction, and prevention of runoff and erosion.
  - "80 T carbone/ha", similar to forests.
  - Thermal buffering and landscape.

  It calls grassland loss "une catastrophe écologique à bas bruit". It notes the regional biodiversity strategy's operational objective of **"zéro perte nette de prairies à l'échelle normande à l'horizon 2030"**. It recommends priority reseeding of permanent grassland in high-stakes zones (wetlands, Natura 2000, ZNIEFF) and protection of oligotrophic grassland. [full text] — [CSRPN 2023](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2023-12-12_prairies.pdf)
- **Biodiversity (national context).** The 24 farmland-specialist bird species lost 63 index points in 35 years (STOC). [excerpt] — [SDES, milieux agricoles 2025](https://www.statistiques.developpement-durable.gouv.fr/milieux-agricoles-et-enjeux-environnementaux-en-france-etat-des-connaissances-en-2025). In Normandy, the Crested Lark (Cochevis huppé), a farmland species, "semble en régression marquée dans notre région". [excerpt] — [LPO Normandie](https://normandie.lpo.fr/wp-content/uploads/2024/10/OL17-cochevis-huppe-Normandie.pdf)
- **PNR wet grassland.** PNR Marais du Cotentin et du Bessin has about 30,000 ha of wet grassland, mostly Natura 2000. In PNR Boucles de la Seine, 170 farms have contracted extensive grassland management on 5,907 ha. Drainage of wet grassland for maize is a known pressure there. [excerpt] — [Fédération PNR fiche MCB](https://www.parcs-naturels-regionaux.fr/sites/federationpnr/files/document/centre_de_ressources/fiche_marais_du_cotentin_et_du_bessin.pdf); [TVB fiche PNR BSN](https://trameverteetbleue.fr/sites/default/files/fiche_experience_pnr_bsn_0.pdf)

### Our reading
- Spatial overlays that the module could compute from open data, each backed by a regional source:
  - ploughed parcels × slope / Pays de Caux runoff axes (erosion);
  - ploughed parcels × drinking-water catchment areas (AESN nitrate argument);
  - ploughed parcels × RPG SNA hedges (CSRPN "victimes collatérales");
  - ploughed parcels × Natura 2000 / wetlands / ZNIEFF (CSRPN priority zones).

### Open points
- No quantified Normandy statistic directly linking ploughed hectares to hedge removal, muddy-flood events or nitrate trends. Links are qualitative or correlational.
- No Normandy STOC farmland-bird index found. GONm and LPO Normandie may hold one.
- No regional map of ploughed grassland after 2019 found from DRAAF, Chambre or PNR. The Agreste 2021 smoothed map (2008–2019) is the latest regional map I found.

---

## 5. Potential users and sensitivities

### In short
There are documented potential users and demands:
- **CSRPN / DREAL**: explicitly asked for a quarterly ploughing/implantation indicator;
- **DRAAF / DDT(M)**: BCAE 1 monitoring and reseeding targeting;
- **ANBDD**: EPCI indicators;
- **Région**: regional biodiversity strategy, "zéro perte nette de prairies 2030";
- **AESN and catchment authorities**: nitrates and PES;
- **PNR**: MAEC areas;
- **Chambre d'agriculture / AREAS**: erosion advice.

The main sensitivities are that (a) ploughing is legal in most cases, (b) regulatory status depends on the ratio, and (c) parcel-level data can be linked to individual farmers. Farm unions have treated the ban regime as an administrative constraint.

### Sources
- **CSRPN demands.** "Mettre en place un indicateur de suivi des retournements / implantations de prairies publié chaque trimestre"; regular information on ratios; that reference ratios be based on "réalités surfaciques constatées sur le terrain". The motion went to the regional prefect, the President of the Regional Council, the DRAAF, the prefects, the DDT(M)s and the GIEC normand. [full text] — [CSRPN 2024](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf); [CSRPN 2023](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2023-12-12_prairies.pdf)
- **DDT(M) role.** DDT(M)s notify farmers who must reconvert and instruct conversion authorisations. [web page] — [DRAAF 2023](https://draaf.normandie.agriculture.gouv.fr/prairies-permanentes-la-normandie-passe-en-regime-d-interdiction-a3672.html). DDTM 27 advises farmers to check with it before any ploughing. [web page] — [DDTM Eure](https://www.eure.gouv.fr/Actions-de-l-Etat/Agriculture/L-actualite-de-l-agriculture/Maintien-des-prairies-permanentes)
- **Coordination Rurale Normandie (Nov. 2023).** Neutral, informational tone. It flags uncertainty ("cas d'exemption … doivent encore être définis") and dependence on ministry lists of farmers. It warns that the region could stay under the ban in 2025 if too little is reseeded. [web page] — [CR Normandie](https://www.coordinationrurale.fr/nos-cr-locales-actualites/normandie/regime-dinterdiction-de-retournement-des-prairies-permanentes-en-normandie/)
- **Trade press.** It questioned whether farmers who had stopped ruminant farming should be forced to reseed. The Chambre adviser expected the administration to target land ploughed in 2022–2023. [excerpt] — [Réussir](https://www.reussir.fr/lait/pac-et-prairies-permanentes-delais-tres-courts-pour-vos-demandes)
- **Agreste framing.** Ploughing is an economic consequence of the shift from dairy to mixed farming or arable, while milk production holds or rises (e.g. Manche). It is not framed as misconduct. [full text] — [Agreste 2021](https://draaf.normandie.agriculture.gouv.fr/IMG/pdf/Agreste_Etudes_no6-Prairies_Normandie_2008_2019-septembre_2021_cle09a9b1.pdf)
- **CSRPN causes.** It attributes grassland loss to land consolidation, changes of activity, and the transformation and decline of livestock farming. [full text] — [CSRPN 2024](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/motion_csrpn_2024-12-12_prairies_vfsigne.pdf)
- **Data protection.** RPG open data is anonymised and its release is governed by MASA instruction DGPE/SDGP/2022-106. [web page] — [data.gouv.fr RPG](https://www.data.gouv.fr/datasets/rpg). DREAL rubrique 46 decisions are published with petitioner name and cadastral references. [full text] — [DREAL Montigny decision](https://www.normandie.developpement-durable.gouv.fr/IMG/pdf/d_2025_5772_retournement_prairies_permanentes_montigny.pdf)
- **Data quality caveat.** PAC declarations do not describe the ecological quality of grassland, since botanical composition is not declared. [excerpt] — [Observatoire biodiversité Centre-Val de Loire 2026](https://www.biodiversite-centrevaldeloire.fr/sites/default/files/content/ressources/pdf/2026-07/R%C3%A9cap_indicateur_ocsolprairies_2026.pdf)

### Our reading
- **How a public tool should present ploughing:**
  1. **Aggregate** results publicly at commune, EPCI or a 1 km grid, like the Agreste smoothed maps. Avoid parcel-level "ploughed field" maps that, combined with cadastre or a DREAL decision, can identify a farmer.
  2. Say that most ploughing is **legal** and is not a breach. Use neutral wording ("conversion prairie → culture") and avoid "infraction".
  3. Separate **gross** losses from **gains** (new permanent grassland, reseeding) and show the **net** figure.
  4. Give the **economic context** of livestock decline, as Agreste and CSRPN do.
  5. Label the definitions (RPG permanent grassland vs STH vs OSCOM grassland) and show the official regional ratio next to it for consistency.
  6. Present it as a **decision aid**: targeting reseeding, PES and MAEC, and erosion or catchment priority.
- **Likely user groups:**
  - DRAAF and DDT(M): BCAE 1 early warning before the 4% threshold.
  - Région / ANBDD: SRB "zéro perte nette de prairies 2030" monitoring, and extending the EPCI indicators.
  - AESN and catchment authorities: catchment overlays.
  - PNR: wet grassland in MCB and BSN.
  - Chambre / AREAS: erosion advice.
  - EPCI elected officials: PLUi, SCoT, PCAET.

### Open points
- No documented opinion from Normandy farm unions (FNSEA/FRSEA, JA, CR, Confédération paysanne) on a public map of grassland ploughing.
- No CNIL or ministry guidance found specific to republishing derived parcel-level RPG change maps.
