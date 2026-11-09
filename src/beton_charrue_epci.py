"""Bilan « béton + charrue » par EPCI sur la fenêtre OCS GE d'un département.

Usage :
    python src/beton_charrue_epci.py <zan_evol_AAAA_BBBB_XX.gpkg> <annee_debut> <annee_fin> \
        <seq1524_dXX.gpkg> <ref_fr_en.csv> <dossier_communes> <sortie.csv>

Béton : polygones `artificialisation = 1` de la couche officielle IGN « OCS GE
Artificialisation, différentiel » (ressource OCSGE-ARTIFICIALISATION, DIFF-AAAA-BBBB), qui
applique le décret 2023-1096. La désartificialisation (`artificialisation = -1`) est
seulement affichée, séparée en « sols rendus » (CS1.1.x l'année de début) et en simple
changement d'usage d'une surface déjà végétalisée. Le béton posé sur de l'herbe agricole
(CS2.2.1 / US1.1) hors parcelle déclarée est compté à part comme « prairies probables hors
PAC ». Il sert à la borne haute de la part du béton. Une règle maison couverture × usage ne reproduit pas cette couche
(tests/T5b), car l'IGN applique des critères en plus du couple CS/US.
Ce qui a été bétonné est qualifié par la culture RPG de l'année de début (LCP de RPG Explorer).

Charrue : prairies permanentes passées en culture d'une année à la suivante sur la même
fenêtre, en retirant la surface que le béton a prise sur les mêmes LCP (le béton l'emporte).
Les classes RPG et la définition des prairies anciennes viennent de definitions.py.
"""
import sys

import duckdb

from definitions import annees_entre, classes_sql, jointures_ref, pp_ancienne_sql, retournement_sql
from geo_utils import charger_communes, rattacher_plus_proche

DIFF, Y0, Y1, GPKG, REF, COMMUNES, OUT = sys.argv[1:8]
y0, y1 = int(Y0), int(Y1)
a0, a1 = f"{y0 % 100:02d}", f"{y1 % 100:02d}"
YEARS = annees_entre(y0, y1)


con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{REF}', header=true)")
# Communes des 5 départements : un objet de ce département peut tomber dans une commune voisine
charger_communes(con, COMMUNES)

# 1. Béton : polygones nouvellement artificialisés (couche officielle IGN)
con.execute(f"""
    CREATE TABLE beton AS
    SELECT fid, cs_{y0} AS cs0, us_{y0} AS us0, cs_{y1} AS cs1, us_{y1} AS us1, ST_MakeValid(geom) AS geom
    FROM ST_Read('{DIFF}')
    WHERE artificialisation = 1
""")
n, ha = con.execute("SELECT count(*), sum(ST_Area(geom)) / 1e4 FROM beton").fetchone()
desartif = con.execute(
    f"SELECT coalesce(sum(ST_Area(geom)), 0) / 1e4 FROM ST_Read('{DIFF}') WHERE artificialisation = -1").fetchone()[0]
print(f"Béton {y0}->{y1} : {n:,} polygones, {ha:,.0f} ha ; désartificialisation : {desartif:,.0f} ha")
print("  occupation avant :", con.execute(
    "SELECT cs0, us0, round(sum(ST_Area(geom))/1e4) ha FROM beton GROUP BY ALL ORDER BY ha DESC LIMIT 6").fetchall())

# 2. LCP avec classes annuelles (definitions.py)
con.execute(f"""
    CREATE TABLE lcp AS
    SELECT l.id_lcp, l.area_lcp AS ha, ST_MakeValid(l.wkb_geometry) AS geom,
           ST_PointOnSurface(l.wkb_geometry) AS pt,
           {classes_sql(non_declare="'non déclaré'")}
    FROM ST_Read('{GPKG}') l
    {jointures_ref()}
""")

# 3. Intersection béton x LCP : ce que le béton a pris aux terres agricoles déclarées
con.execute(f"""
    CREATE TABLE beton_lcp AS
    SELECT b.fid, l.id_lcp, l.k{a0} AS k0, ST_Area(ST_Intersection(b.geom, l.geom)) / 1e4 AS ha_beton
    FROM beton b JOIN lcp l ON ST_Intersects(b.geom, l.geom)
""")
con.execute("CREATE TABLE beton_par_lcp AS SELECT id_lcp, sum(ha_beton) AS ha_beton FROM beton_lcp GROUP BY id_lcp")
# Part de chaque polygone béton couverte par une parcelle déclarée l'année de début
con.execute("""
    CREATE TABLE beton_declare AS
    SELECT fid, sum(ha_beton) FILTER (WHERE k0 <> 'non déclaré') AS ha_declare FROM beton_lcp GROUP BY fid
""")

# 4. Rattachement communes / EPCI : point intérieur, ou à défaut commune la plus proche
con.execute("""
    CREATE TABLE lcp_e AS
    SELECT l.*, coalesce(bl.ha_beton, 0) AS ha_beton, c.insee, c.epci_code, c.epci_nom
    FROM lcp l LEFT JOIN beton_par_lcp bl USING (id_lcp)
    LEFT JOIN communes c ON ST_Within(l.pt, c.geom)
""")
rattacher_plus_proche(con, "lcp_e", "id_lcp", "t.pt")
# Prairies probables hors PAC : herbe agricole (CS2.2.1 / US1.1) bétonnée hors parcelle déclarée
con.execute("""
    CREATE TABLE beton_e AS
    SELECT b.*, ST_Area(b.geom) / 1e4 AS ha,
           CASE WHEN b.cs0 = 'CS2.2.1' AND b.us0 = 'US1.1'
                THEN greatest(ST_Area(b.geom) / 1e4 - coalesce(d.ha_declare, 0), 0) ELSE 0 END AS ha_herbe_hors_pac,
           c.insee, c.epci_code, c.epci_nom
    FROM beton b LEFT JOIN beton_declare d USING (fid)
    LEFT JOIN communes c ON ST_Within(ST_PointOnSurface(b.geom), c.geom)
""")
rattacher_plus_proche(con, "beton_e", "fid", "ST_PointOnSurface(t.geom)")
# Désartificialisation : « sols rendus » (sol bâti, revêtu ou stabilisé redevenu végétal ou nu)
# ou simple changement d'usage d'une surface déjà végétalisée (ex. fin de chantier sur prairie)
con.execute(f"""
    CREATE TABLE desartif AS
    SELECT d.fid, ST_Area(d.geom) / 1e4 AS ha, d.cs_{y0} LIKE 'CS1.1%' AS sols_rendus,
           c.insee, c.epci_code, c.epci_nom, d.geom
    FROM (SELECT fid, cs_{y0}, ST_MakeValid(geom) AS geom FROM ST_Read('{DIFF}') WHERE artificialisation = -1) d
    LEFT JOIN communes c ON ST_Within(ST_PointOnSurface(d.geom), c.geom)
""")
rattacher_plus_proche(con, "desartif", "fid", "ST_PointOnSurface(t.geom)")
con.execute("""
    CREATE TABLE desartif_e AS
    SELECT epci_code, sum(ha) FILTER (WHERE sols_rendus) AS ha_sols, sum(ha) FILTER (WHERE NOT sols_rendus) AS ha_usage
    FROM desartif GROUP BY ALL
""")
print("Désartificialisation : sols rendus {:,.0f} ha, changement d'usage {:,.0f} ha".format(
    *con.execute("SELECT coalesce(sum(ha_sols), 0), coalesce(sum(ha_usage), 0) FROM desartif_e").fetchone()))

# 5. Contrôle du double compte : PP de l'année de début touchées par le béton, devenir RPG à la fin
print("\nPP en", y0, "touchées par le béton - classe RPG en", y1, ":", con.execute(f"""
    SELECT k{a1}, round(sum(ha_beton)) FROM lcp_e WHERE k{a0} = 'PP' AND ha_beton > 0 GROUP BY 1 ORDER BY 2 DESC""").fetchall())

# 6. Charrue sur la fenêtre, nette du béton : surface retournée moins la part bétonnée de la LCP
# Prairie ancienne : PP chaque année de 2015 jusqu'à l'année N (definitions.py, comme retournements_epci.py)
charrue = " UNION ALL ".join(f"""
    SELECT epci_code, greatest(ha - ha_beton, 0) AS ha, ({pp_ancienne_sql(YEARS[i])}) AS pp_ancienne
    FROM lcp_e WHERE {retournement_sql(YEARS[i], YEARS[i + 1])}""" for i in range(len(YEARS) - 1))
con.execute(f"""
    CREATE TABLE resultat AS
    WITH e AS (
        -- Seulement les EPCI où ce département a des objets, pas les 71 EPCI des communes chargées
        SELECT DISTINCT epci_code, epci_nom FROM (
            SELECT epci_code, epci_nom FROM lcp_e UNION ALL
            SELECT epci_code, epci_nom FROM beton_e UNION ALL
            SELECT epci_code, epci_nom FROM desartif)
        WHERE epci_code IS NOT NULL),
    b AS (SELECT epci_code, sum(ha) AS beton_total, sum(ha_herbe_hors_pac) AS beton_herbe_hors_pac
          FROM beton_e WHERE epci_code IS NOT NULL GROUP BY ALL),
    -- Ventilation du béton par culture de l'année de début, rattachée à l'EPCI du POLYGONE de béton
    -- (comme beton_total) : les deux s'additionnent toujours, même pour un béton en limite d'EPCI
    bq AS (
        SELECT be.epci_code,
               sum(bl.ha_beton) FILTER (WHERE bl.k0 = 'PP') AS beton_sur_pp,
               sum(bl.ha_beton) FILTER (WHERE bl.k0 = 'PT') AS beton_sur_pt,
               sum(bl.ha_beton) FILTER (WHERE bl.k0 IN ('culture', 'fourrage', 'gel')) AS beton_sur_cultures
        FROM beton_lcp bl JOIN beton_e be USING (fid) WHERE be.epci_code IS NOT NULL GROUP BY ALL),
    ch AS (
        SELECT epci_code, sum(ha) AS charrue_pp, sum(ha) FILTER (WHERE pp_ancienne) AS charrue_pp_anciennes
        FROM ({charrue}) WHERE epci_code IS NOT NULL GROUP BY ALL)
    SELECT e.epci_code, e.epci_nom, {y0} AS debut, {y1} AS fin,
           round(coalesce(b.beton_total, 0), 1) AS beton_total,
           round(coalesce(d.ha_sols, 0), 1) AS desartif_sols,
           round(coalesce(d.ha_usage, 0), 1) AS desartif_usage,
           round(coalesce(beton_sur_pp, 0), 1) AS beton_sur_pp,
           round(coalesce(beton_sur_pt, 0), 1) AS beton_sur_pt,
           round(coalesce(beton_sur_cultures, 0), 1) AS beton_sur_cultures,
           round(coalesce(b.beton_total, 0) - coalesce(beton_sur_pp, 0) - coalesce(beton_sur_pt, 0)
                 - coalesce(beton_sur_cultures, 0), 1) AS beton_hors_rpg,
           round(coalesce(b.beton_herbe_hors_pac, 0), 1) AS beton_herbe_hors_pac,
           round(coalesce(charrue_pp, 0), 1) AS charrue_pp,
           round(coalesce(charrue_pp_anciennes, 0), 1) AS charrue_pp_anciennes,
           round(coalesce(beton_sur_pp, 0) + coalesce(charrue_pp, 0), 1) AS prairies_perdues,
           round(100 * coalesce(beton_sur_pp, 0) / nullif(coalesce(beton_sur_pp, 0) + coalesce(charrue_pp, 0), 0), 1)
               AS part_beton_pct,
           round(coalesce(beton_sur_pp, 0) + coalesce(b.beton_herbe_hors_pac, 0) + coalesce(charrue_pp, 0), 1)
               AS prairies_perdues_haute,
           round(100 * (coalesce(beton_sur_pp, 0) + coalesce(b.beton_herbe_hors_pac, 0))
                 / nullif(coalesce(beton_sur_pp, 0) + coalesce(b.beton_herbe_hors_pac, 0) + coalesce(charrue_pp, 0), 0), 1)
               AS part_beton_haute_pct
    FROM e LEFT JOIN b USING (epci_code) LEFT JOIN bq USING (epci_code) LEFT JOIN ch USING (epci_code)
    LEFT JOIN desartif_e d USING (epci_code)
    ORDER BY prairies_perdues DESC
""")
con.execute(f"COPY resultat TO '{OUT}' (HEADER, DELIMITER ';')")
print(f"\nÉcrit : {OUT}")
print("TOTAL :", dict(zip(
    ["beton", "beton_sur_pp", "beton_herbe_hors_pac", "charrue_pp", "charrue_anciennes", "part_beton_pct", "part_beton_haute_pct"],
    con.execute("""SELECT round(sum(beton_total)), round(sum(beton_sur_pp)), round(sum(beton_herbe_hors_pac)),
        round(sum(charrue_pp)), round(sum(charrue_pp_anciennes)),
        round(100 * sum(beton_sur_pp) / sum(prairies_perdues), 1),
        round(100 * (sum(beton_sur_pp) + sum(beton_herbe_hors_pac)) / sum(prairies_perdues_haute), 1)
        FROM resultat""").fetchone())))
