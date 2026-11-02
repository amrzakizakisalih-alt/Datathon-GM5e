"""Mesure l'effet de l'ancien rattachement, limité aux communes du département de l'objet.

La pipeline charge désormais les communes des 5 départements. Ce script garde la comparaison
qui a motivé ce changement : « pipeline » y désigne donc l'ancienne méthode.

Usage :
    python src/test_rattachement.py

Pipeline : un objet (LCP ou polygone de béton) est cherché dans les communes de son seul
département, puis rattaché à la plus proche de ce département s'il n'y tombe pas.
Test : les objets sans commune sont recherchés dans les communes des 5 départements.

Statut de chaque objet sans commune dans son département :
  autre_dep      son point tombe dans une commune d'un autre département normand
  hors_contours  son point ne tombe dans aucune commune normande (littoral, hors Normandie)
                 il est alors comparé à la commune normande la plus proche : son vrai EPCI
                 reste inconnu s'il est hors de Normandie

Sortie : data/processed/test_rattachement_epci.csv
"""
import csv
from pathlib import Path

import duckdb

RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
OUT = RACINE / "data" / "processed" / "test_rattachement_epci.csv"
YEARS = [f"{y:02d}" for y in range(15, 25)]
CULTURE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 14, 15, 24, 25)

with open(RAW / "ocsge_artif" / "fenetres.csv", encoding="utf-8") as f:
    FENETRES = list(csv.DictReader(f, delimiter=";"))

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{RAW}/rpg_explorer/ref_fr_en.csv', header=true)")
con.execute("CREATE TABLE communes (dep VARCHAR, insee VARCHAR, epci_code VARCHAR, epci_nom VARCHAR, geom GEOMETRY)")
for x in FENETRES:
    con.execute(f"""
        INSERT INTO communes
        SELECT '{x["dep"]}', code, codeEpci, json_extract_string(epci, '$.nom'),
               ST_Transform(geom, 'EPSG:4326', 'EPSG:2154', always_xy := true)
        FROM ST_Read('{RAW}/geo/communes_{x["dep"]}.geojson')
    """)

con.execute("""
    CREATE TABLE objets (dep VARCHAR, nature VARCHAR, id VARCHAR, ha DOUBLE, stock_2015 DOUBLE, charrue DOUBLE, pt GEOMETRY)
""")
for x in FENETRES:
    d = x["dep"]
    gpkg = RAW / "rpg_explorer" / f"seq1524_d{d}.gpkg"
    joins = " ".join(f"LEFT JOIN ref r{y} ON r{y}.crop = l.crop{y}" for y in YEARS)
    passages = " + ".join(
        f"CASE WHEN r{a}.grp = 18 AND r{b}.grp IN {CULTURE} THEN 1 ELSE 0 END" for a, b in zip(YEARS, YEARS[1:]))
    con.execute(f"""
        INSERT INTO objets
        SELECT '{d}', 'lcp', CAST(l.id_lcp AS VARCHAR), l.area_lcp,
               CASE WHEN r15.grp = 18 THEN l.area_lcp ELSE 0 END, l.area_lcp * ({passages}),
               ST_PointOnSurface(l.wkb_geometry)
        FROM ST_Read('{gpkg}') l {joins}
    """)
    con.execute(f"""
        INSERT INTO objets
        SELECT '{d}', 'beton', CAST(fid AS VARCHAR), ST_Area(ST_MakeValid(geom)) / 1e4, 0, 0,
               ST_PointOnSurface(ST_MakeValid(geom))
        FROM ST_Read('{RACINE / x["couche"]}') WHERE artificialisation = 1
    """)

# 1. Comme la pipeline : objets dont le point tombe dans une commune de leur département
con.execute("""
    CREATE TABLE trouves AS
    SELECT o.dep, o.nature, o.id, any_value(c.epci_code) AS epci, count(*) AS n
    FROM objets o JOIN communes c ON c.dep = o.dep AND ST_Within(o.pt, c.geom)
    GROUP BY ALL
""")
con.execute("""
    CREATE TABLE sans AS
    SELECT o.* FROM objets o ANTI JOIN trouves t ON t.dep = o.dep AND t.nature = o.nature AND t.id = o.id
""")
# 2. Comme la pipeline : commune la plus proche dans le département
con.execute("""
    CREATE TABLE proche_dep AS
    SELECT s.dep, s.nature, s.id, arg_min(c.epci_code, ST_Distance(s.pt, c.geom)) AS epci_avant,
           min(ST_Distance(s.pt, c.geom)) AS dist_dep
    FROM sans s JOIN communes c ON c.dep = s.dep GROUP BY ALL
""")
# 3. Test : commune contenant le point parmi les 5 départements, sinon la plus proche parmi les 5
con.execute("""
    CREATE TABLE dans_tous AS
    SELECT s.dep, s.nature, s.id, any_value(c.epci_code) AS epci
    FROM sans s JOIN communes c ON ST_Within(s.pt, c.geom) GROUP BY ALL
""")
con.execute("""
    CREATE TABLE proche_tous AS
    SELECT s.dep, s.nature, s.id, arg_min(c.epci_code, ST_Distance(s.pt, c.geom)) AS epci,
           min(ST_Distance(s.pt, c.geom)) AS dist
    FROM sans s ANTI JOIN dans_tous t ON t.dep = s.dep AND t.nature = s.nature AND t.id = s.id
    JOIN communes c ON true GROUP BY ALL
""")
con.execute("""
    CREATE TABLE comparaison AS
    SELECT s.dep, s.nature, s.id, s.ha, s.stock_2015, s.charrue, p.epci_avant, p.dist_dep,
           coalesce(t.epci, a.epci) AS epci_apres,
           CASE WHEN t.epci IS NOT NULL THEN 'autre_dep' ELSE 'hors_contours' END AS statut
    FROM sans s
    JOIN proche_dep p USING (dep, nature, id)
    LEFT JOIN dans_tous t USING (dep, nature, id)
    LEFT JOIN proche_tous a USING (dep, nature, id)
""")


def afficher(titre, requete):
    print(f"\n{titre}")
    res = con.execute(requete)
    print(" | ".join(c[0] for c in res.description))
    for ligne in res.fetchall():
        print(" | ".join(f"{v:,.1f}" if isinstance(v, float) else str(v) for v in ligne))


afficher("Points contenus dans plusieurs communes du département (contours qui se chevauchent)",
         "SELECT nature, count(*) AS objets FROM trouves WHERE n > 1 GROUP BY 1 ORDER BY 1")
afficher("Objets et surface au total", """
    SELECT nature, count(*) AS objets, sum(ha) AS ha, sum(stock_2015) AS stock_2015, sum(charrue) AS charrue
    FROM objets GROUP BY 1 ORDER BY 1""")
afficher("Objets sans commune dans leur département", """
    SELECT nature, dep, count(*) AS objets, sum(ha) AS ha, sum(charrue) AS charrue,
           median(dist_dep) AS dist_mediane_m, max(dist_dep) AS dist_max_m
    FROM comparaison GROUP BY 1, 2 ORDER BY 1, 2""")
afficher("Effet du test, par statut", """
    SELECT nature, statut, count(*) AS objets, sum(ha) AS ha,
           count(*) FILTER (WHERE epci_avant <> epci_apres) AS objets_changent_epci,
           coalesce(sum(ha) FILTER (WHERE epci_avant <> epci_apres), 0) AS ha_changent,
           coalesce(sum(stock_2015) FILTER (WHERE epci_avant <> epci_apres), 0) AS stock_change,
           coalesce(sum(charrue) FILTER (WHERE epci_avant <> epci_apres), 0) AS charrue_change
    FROM comparaison GROUP BY 1, 2 ORDER BY 1, 2""")

# 4. Effet par EPCI : valeurs de la pipeline, puis valeurs une fois les objets déplacés
con.execute("""
    CREATE TABLE base AS
    SELECT o.nature, o.dep, o.id, o.ha, o.stock_2015, o.charrue, coalesce(t.epci, p.epci_avant) AS epci
    FROM objets o
    LEFT JOIN trouves t USING (dep, nature, id)
    LEFT JOIN proche_dep p USING (dep, nature, id)
""")
con.execute("""
    CREATE TABLE par_epci AS
    WITH noms AS (SELECT epci_code AS epci, any_value(epci_nom) AS epci_nom FROM communes GROUP BY 1),
    v AS (
        SELECT epci,
               sum(stock_2015) AS stock, sum(charrue) AS charrue,
               sum(ha) FILTER (WHERE nature = 'beton') AS beton
        FROM base GROUP BY 1),
    mouv AS (
        SELECT epci, sum(stock) AS d_stock, sum(charrue) AS d_charrue, sum(beton) AS d_beton FROM (
            SELECT epci_avant AS epci, -stock_2015 AS stock, -charrue AS charrue,
                   CASE WHEN nature = 'beton' THEN -ha ELSE 0 END AS beton
            FROM comparaison WHERE epci_avant <> epci_apres
            UNION ALL
            SELECT epci_apres, stock_2015, charrue, CASE WHEN nature = 'beton' THEN ha ELSE 0 END
            FROM comparaison WHERE epci_avant <> epci_apres)
        GROUP BY 1)
    SELECT v.epci AS epci_code, n.epci_nom,
           round(coalesce(v.stock, 0), 1) AS stock_2015_ha, round(coalesce(m.d_stock, 0), 1) AS ecart_stock_ha,
           round(100 * coalesce(m.d_stock, 0) / nullif(v.stock, 0), 2) AS ecart_stock_pct,
           round(coalesce(v.charrue, 0), 1) AS charrue_ha, round(coalesce(m.d_charrue, 0), 1) AS ecart_charrue_ha,
           round(100 * coalesce(m.d_charrue, 0) / nullif(v.charrue, 0), 2) AS ecart_charrue_pct,
           round(coalesce(v.beton, 0), 1) AS beton_ha, round(coalesce(m.d_beton, 0), 1) AS ecart_beton_ha,
           round(100 * coalesce(m.d_beton, 0) / nullif(v.beton, 0), 2) AS ecart_beton_pct
    FROM v LEFT JOIN mouv m USING (epci) LEFT JOIN noms n USING (epci)
    ORDER BY greatest(abs(coalesce(ecart_stock_pct, 0)), abs(coalesce(ecart_charrue_pct, 0)),
                      abs(coalesce(ecart_beton_pct, 0))) DESC
""")
con.execute(f"COPY par_epci TO '{OUT}' (HEADER, DELIMITER ';')")
afficher("EPCI les plus touchés", "SELECT * FROM par_epci LIMIT 12")
afficher("Nombre d'EPCI au-dessus de 1 % d'écart (stock, charrue ou béton)", """
    SELECT count(*) AS epci_total,
           count(*) FILTER (WHERE abs(coalesce(ecart_stock_pct, 0)) > 1) AS stock,
           count(*) FILTER (WHERE abs(coalesce(ecart_charrue_pct, 0)) > 1) AS charrue,
           count(*) FILTER (WHERE abs(coalesce(ecart_beton_pct, 0)) > 1) AS beton
    FROM par_epci""")
print(f"\nÉcrit : {OUT}")
