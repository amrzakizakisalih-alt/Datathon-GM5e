"""Bloc D : ce que le béton et la charrue ont pris en milieux remarquables, par EPCI.

Usage :
    python src/qualite_epci.py <dep> <sortie.csv>

Lit dans data/raw/ (voir telecharger_donnees.py) : la couche d'artificialisation du département
(fenetres.csv), RPG Explorer, les communes, les ZNIEFF, Natura 2000, l'inventaire des zones humides
de la DREAL et les milieux potentiellement humides (MPH) de l'INRAE.

Béton (polygones « artificialisés » de l'IGN sur la fenêtre OCS GE, surfaces totales en ha) :
  beton_ligneux      couverture boisée l'année de début (OCS GE CS2.1.x : bois, bosquets, haies larges).
                     La couche nationale des haies (édition 2026) montre les haies actuelles, pas celles
                     détruites avant : elle ne permet pas de mesurer des km de haies bétonnées.
  beton_znieff1, beton_znieff2, beton_natura2000 (SIC + ZPS), beton_zh (inventaire DREAL) :
                     surface de l'intersection, zones superposées fusionnées pour ne rien compter deux fois.
  beton_mph          surface dans l'enveloppe des milieux potentiellement humides (classes 1 à 3), d'après
                     la part des pixels de 50 m du polygone ; point intérieur si le polygone est plus petit.

Charrue (retournements stricts PP -> culture, cumulés sur les 9 paires 2015->2024, en ha ; même définition
que retournements_epci.py, partagée par definitions.py) : charrue_<zone> et charrue_<zone>_anc (prairies anciennes), pour zone dans
zh, mph, natura2000, znieff1. Une LCP est dans une zone si son point intérieur y est.
Natura 2000 : un retournement dans le périmètre d'un site n'est pas une infraction. La PAC n'y interdit
que le retournement des « prairies sensibles », et la plupart des sites concernés ne sont pas désignés
pour leurs prairies (voir tests/T9). Ne pas présenter cet indicateur comme une infraction.
"""
import csv
import json
import sys
from pathlib import Path

import duckdb
import rasterio
import rasterio.mask

from definitions import ANNEES as YEARS, classes_sql, jointures_ref, pp_ancienne_sql, retournement_sql
from geo_utils import charger_communes, rattacher_plus_proche

DEP, OUT = sys.argv[1], sys.argv[2]
RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
MPH = RAW / "mph" / "mph_normandie.tif"
ZONES = {  # nom -> source lue par ST_Read (Lambert-93)
    "znieff1": RAW / "zonages" / "znieff1.geojson",
    "znieff2": RAW / "zonages" / "znieff2.geojson",
    "natura2000": RAW / "zonages" / "natura2000.geojson",
    "zh": RAW / "zones_humides" / "dataset" / "drealnorm_zh_s_r28.shp",
}

with open(RAW / "ocsge_artif" / "fenetres.csv", encoding="utf-8") as f:
    fen = {x["dep"]: x for x in csv.DictReader(f, delimiter=";")}[DEP]
y0, y1 = int(fen["debut"]), int(fen["fin"])

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true)")
# Communes des 5 départements : un objet de ce département peut tomber dans une commune voisine
charger_communes(con, RAW / "geo")
# Communes du seul département : elles fixent l'emprise des zonages et la liste des EPCI en sortie
con.execute(f"""
    CREATE TABLE communes_dep AS
    SELECT codeEpci AS epci_code, json_extract_string(epci, '$.nom') AS epci_nom,
           ST_Transform(geom, 'EPSG:4326', 'EPSG:2154', always_xy := true) AS geom
    FROM ST_Read('{RAW / 'geo' / f'communes_{DEP}.geojson'}')
""")
x0, ya, x1, yb = con.execute(
    "SELECT ST_XMin(e) - 5000, ST_YMin(e) - 5000, ST_XMax(e) + 5000, ST_YMax(e) + 5000 "
    "FROM (SELECT ST_Envelope(ST_Union_Agg(geom)) AS e FROM communes_dep)").fetchone()
emprise = f"ST_MakeEnvelope({x0}, {ya}, {x1}, {yb})"

# Zonages réduits à l'emprise du département
for nom, src in ZONES.items():
    con.execute(f"""
        CREATE TABLE z_{nom} AS
        SELECT ST_MakeValid(geom) AS geom FROM ST_Read('{src}') WHERE ST_Intersects(geom, {emprise})
    """)

# 1. Béton
con.execute(f"""
    CREATE TABLE beton AS
    SELECT fid, cs_{y0} AS cs0, ST_MakeValid(geom) AS geom, ST_Area(geom) / 1e4 AS ha
    FROM ST_Read('{RACINE / fen['couche']}') WHERE artificialisation = 1
""")
for nom in ZONES:
    con.execute(f"""
        CREATE TABLE b_{nom} AS
        WITH u AS (SELECT b.fid, ST_Union_Agg(z.geom) AS g FROM beton b JOIN z_{nom} z ON ST_Intersects(b.geom, z.geom) GROUP BY b.fid)
        SELECT u.fid, ST_Area(ST_Intersection(b.geom, u.g)) / 1e4 AS ha FROM u JOIN beton b USING (fid)
    """)

# Béton en milieux potentiellement humides : part des pixels du polygone dans les classes 1 à 3
mph_beton = []
with rasterio.open(MPH) as r:
    for fid, gj, x, y, ha in con.execute(
            "SELECT fid, ST_AsGeoJSON(geom), ST_X(ST_PointOnSurface(geom)), ST_Y(ST_PointOnSurface(geom)), ha FROM beton").fetchall():
        try:
            a, _ = rasterio.mask.mask(r, [json.loads(gj)], crop=True, filled=False)
            v = a.compressed()
        except ValueError:
            v = []
        if len(v) == 0:
            v = [next(r.sample([(x, y)]))[0]]
        n = sum(1 for p in v if 1 <= p <= 3)
        mph_beton.append((fid, ha * n / len(v)))
con.execute("CREATE TABLE b_mph (fid BIGINT, ha DOUBLE)")
con.executemany("INSERT INTO b_mph VALUES (?, ?)", mph_beton)

con.execute("""
    CREATE TABLE beton_e AS
    SELECT b.fid, b.ha, b.cs0, c.insee, c.epci_code, c.epci_nom
    FROM beton b LEFT JOIN communes c ON ST_Within(ST_PointOnSurface(b.geom), c.geom)
""")
con.execute("ALTER TABLE beton_e ADD COLUMN geom GEOMETRY")
con.execute("UPDATE beton_e SET geom = b.geom FROM beton b WHERE beton_e.fid = b.fid")
rattacher_plus_proche(con, "beton_e", "fid", "ST_PointOnSurface(t.geom)")

# 2. Charrue : nombre de retournements stricts par LCP sur 2015->2024, toutes PP et prairies anciennes
# (classes et prairies anciennes : definitions.py, comme retournements_epci.py)
# Une année non déclarée vaut 'non déclaré' et non NULL : avec NULL, un seul terme vide rendait toute la somme
# NULL, et coalesce(..., 0) effaçait tous les retournements de la LCP, y compris ceux des autres années.
con.execute(f"""
    CREATE TABLE lcp AS
    SELECT l.id_lcp, l.area_lcp AS ha, ST_PointOnSurface(l.wkb_geometry) AS pt, {classes_sql(non_declare="'non déclaré'")}
    FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{DEP}.gpkg'}') l
    {jointures_ref()}
""")
toutes = " + ".join(f"({retournement_sql(YEARS[i], YEARS[i + 1])})::INT" for i in range(len(YEARS) - 1))
anc = " + ".join(f"({pp_ancienne_sql(YEARS[i])} AND {retournement_sql(YEARS[i], YEARS[i + 1])})::INT"
                 for i in range(len(YEARS) - 1))
con.execute(f"""
    CREATE TABLE retour AS
    SELECT id_lcp, ha, pt, coalesce({toutes}, 0) AS n_toutes, coalesce({anc}, 0) AS n_anc FROM lcp
""")
con.execute("DELETE FROM retour WHERE n_toutes = 0")
for nom in ("zh", "natura2000", "znieff1"):
    con.execute(f"CREATE TABLE r_{nom} AS SELECT DISTINCT l.id_lcp FROM retour l JOIN z_{nom} z ON ST_Within(l.pt, z.geom)")
with rasterio.open(MPH) as r:
    pts = con.execute("SELECT id_lcp, ST_X(pt), ST_Y(pt) FROM retour").fetchall()
    vals = [v[0] for v in r.sample([(x, y) for _, x, y in pts])]
con.execute("CREATE TABLE r_mph (id_lcp VARCHAR)")
con.executemany("INSERT INTO r_mph VALUES (?)", [(p[0],) for p, v in zip(pts, vals) if 1 <= v <= 3])

con.execute("""
    CREATE TABLE retour_e AS
    SELECT l.*, c.insee, c.epci_code, c.epci_nom FROM retour l LEFT JOIN communes c ON ST_Within(l.pt, c.geom)
""")
rattacher_plus_proche(con, "retour_e", "id_lcp", "t.pt")

# 3. Agrégation par EPCI
bq = ",\n".join(f"sum(coalesce(b_{n}.ha, 0)) AS beton_{n}" for n in (*ZONES, "mph"))
bj = "\n".join(f"LEFT JOIN b_{n} ON b_{n}.fid = e.fid" for n in (*ZONES, "mph"))
cq = ",\n".join(
    f"sum(ha * n_toutes) FILTER (WHERE id_lcp IN (SELECT id_lcp FROM r_{n})) AS charrue_{n},\n"
    f"sum(ha * n_anc) FILTER (WHERE id_lcp IN (SELECT id_lcp FROM r_{n})) AS charrue_{n}_anc"
    for n in ("zh", "mph", "natura2000", "znieff1"))
con.execute(f"""
    CREATE TABLE resultat AS
    WITH e AS (
        -- EPCI du département, plus ceux des communes voisines où tombent des objets du département
        SELECT DISTINCT epci_code, epci_nom FROM (
            SELECT epci_code, epci_nom FROM communes_dep UNION ALL
            SELECT epci_code, epci_nom FROM beton_e UNION ALL
            SELECT epci_code, epci_nom FROM retour_e)
        WHERE epci_code IS NOT NULL),
    b AS (SELECT e.epci_code, sum(e.ha) FILTER (WHERE e.cs0 LIKE 'CS2.1%') AS beton_ligneux, {bq}
          FROM beton_e e {bj} GROUP BY e.epci_code),
    c AS (SELECT epci_code, {cq} FROM retour_e GROUP BY epci_code)
    SELECT e.epci_code, e.epci_nom, {y0} AS debut, {y1} AS fin, COLUMNS(* EXCLUDE (epci_code, epci_nom))
    FROM e LEFT JOIN b USING (epci_code) LEFT JOIN c USING (epci_code)
""")
cols = [c[0] for c in con.execute("DESCRIBE resultat").fetchall()]
num = [c for c in cols if c.startswith(("beton_", "charrue_"))]
con.execute(f"CREATE TABLE sortie AS SELECT epci_code, epci_nom, debut, fin, "
            + ", ".join(f"round(coalesce({c}, 0), 1) AS {c}" for c in num) + " FROM resultat ORDER BY epci_nom")
con.execute(f"COPY sortie TO '{OUT}' (HEADER, DELIMITER ';')")
tot = con.execute("SELECT " + ", ".join(f"round(sum({c}))" for c in num) + " FROM sortie").fetchone()
print(f"Département {DEP} ({y0}->{y1}) :", dict(zip(num, tot)))
