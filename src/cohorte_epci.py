"""Cohorte des prairies anciennes par EPCI et par an : entrée de src/trajectoires.py.

Usage :
    python src/cohorte_epci.py <sortie.csv>

La cohorte de l'année N regroupe les LCP déclarées en prairie permanente (groupe 18) chaque année de 2015 à N,
même définition que strict_anciennes dans retournements_epci.py. Rattachement à l'EPCI et aux zones par point intérieur.
Une ligne par EPCI et par passage N -> N+1 (annee = N+1), en ha :
  stock_debut            cohorte de l'année N
  vers_culture           cohorte de N déclarée en culture en N+1 (la charrue)
  vers_culture_prl       dont les LCP codées PRL (prairie en rotation longue) l'année N
  vers_culture_reconnue  dont en zone humide inventoriée (DREAL), Natura 2000 ou ZNIEFF de type 1
  vers_culture_etendue   dont en zone reconnue ou en milieu potentiellement humide (MPH, classes 1 à 3)
  stock_reconnue, stock_etendue   part de stock_debut dans ces zones
  stock_fin              cohorte de l'année N+1. stock_debut - vers_culture - stock_fin = autres sorties (prairie temporaire,
                         non déclaré, autre), dont on ignore le devenir réel : elles ne sont jamais comptées comme des labours.
  stock_ha2              somme des carrés des surfaces de la cohorte de N : stock_debut² / stock_ha2 est son nombre de parcelles équivalent
Les zones superposées ne comptent qu'une fois. Agrégats seulement.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import duckdb
import rasterio

from geo_utils import rattacher_plus_proche

OUT = sys.argv[1]
RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
DEPS = ["14", "27", "50", "61", "76"]
YEARS = [f"{y:02d}" for y in range(15, 25)]
CULTURE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 24, 25)
MPH = RAW / "mph" / "mph_normandie.tif"
ZONES = {
    "znieff1": RAW / "zonages" / "znieff1.geojson",
    "natura2000": RAW / "zonages" / "natura2000.geojson",
    "zh": RAW / "zones_humides" / "dataset" / "drealnorm_zh_s_r28.shp",
}
CHAMPS = ["stock_debut", "vers_culture", "vers_culture_prl", "vers_culture_reconnue", "vers_culture_etendue", "stock_reconnue", "stock_etendue", "stock_fin", "stock_ha2"]
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

lignes = defaultdict(lambda: [0.0] * len(CHAMPS))
for d in DEPS:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true)")
    con.execute(f"""CREATE TABLE communes AS
        SELECT code AS insee, codeEpci AS epci_code, json_extract_string(epci, '$.nom') AS epci_nom,
               ST_Transform(geom, 'EPSG:4326', 'EPSG:2154', always_xy := true) AS geom
        FROM ST_Read('{RAW / 'geo' / f'communes_{d}.geojson'}')""")
    x0, ya, x1, yb = con.execute("SELECT ST_XMin(e) - 5000, ST_YMin(e) - 5000, ST_XMax(e) + 5000, ST_YMax(e) + 5000 FROM (SELECT ST_Envelope(ST_Union_Agg(geom)) AS e FROM communes)").fetchone()
    for nom, src in ZONES.items():
        con.execute(f"CREATE TABLE z_{nom} AS SELECT ST_MakeValid(geom) AS geom FROM ST_Read('{src}') WHERE ST_Intersects(geom, ST_MakeEnvelope({x0}, {ya}, {x1}, {yb}))")
    classes = ", ".join(f"l.crop{y} AS c{y}, CASE WHEN l.crop{y} IS NULL THEN NULL WHEN r{y}.grp = 18 THEN 'PP' WHEN r{y}.grp IN {CULTURE} THEN 'culture' ELSE 'autre' END AS k{y}" for y in YEARS)
    joins = " ".join(f"LEFT JOIN ref r{y} ON r{y}.crop = l.crop{y}" for y in YEARS)
    con.execute(f"""CREATE TABLE lcp AS SELECT l.id_lcp, l.area_lcp AS ha, ST_PointOnSurface(l.wkb_geometry) AS pt, {classes}
        FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{d}.gpkg'}') l {joins} WHERE r15.grp = 18""")
    for nom in ZONES:
        con.execute(f"CREATE TABLE r_{nom} AS SELECT DISTINCT l.id_lcp FROM lcp l JOIN z_{nom} z ON ST_Within(l.pt, z.geom)")
    with rasterio.open(MPH) as r:
        pts = con.execute("SELECT id_lcp, ST_X(pt), ST_Y(pt) FROM lcp").fetchall()
        vals = [v[0] for v in r.sample([(x, y) for _, x, y in pts])]
    con.execute("CREATE TABLE r_mph (id_lcp VARCHAR)")
    con.executemany("INSERT INTO r_mph VALUES (?)", [(p[0],) for p, v in zip(pts, vals) if 1 <= v <= 3])
    reconnue = " OR ".join(f"l.id_lcp IN (SELECT id_lcp FROM r_{nom})" for nom in ZONES)
    con.execute(f"""CREATE TABLE lcp_epci AS
        SELECT l.*, c.insee, c.epci_code, c.epci_nom, ({reconnue}) AS reconnue, ({reconnue} OR l.id_lcp IN (SELECT id_lcp FROM r_mph)) AS etendue
        FROM lcp l LEFT JOIN communes c ON ST_Within(l.pt, c.geom)""")
    rattacher_plus_proche(con, "lcp_epci", "id_lcp", "t.pt")
    for i in range(len(YEARS) - 1):
        a, b = YEARS[i], YEARS[i + 1]
        cohorte = " AND ".join(f"k{y} = 'PP'" for y in YEARS[: i + 1])
        for code, *v in con.execute(f"""SELECT epci_code, sum(ha),
                sum(ha) FILTER (WHERE k{b} = 'culture'),
                sum(ha) FILTER (WHERE k{b} = 'culture' AND c{a} = 'PRL'),
                sum(ha) FILTER (WHERE k{b} = 'culture' AND reconnue),
                sum(ha) FILTER (WHERE k{b} = 'culture' AND etendue),
                sum(ha) FILTER (WHERE reconnue),
                sum(ha) FILTER (WHERE etendue),
                sum(ha) FILTER (WHERE k{b} = 'PP'),
                sum(ha * ha)
                FROM lcp_epci WHERE epci_code IS NOT NULL AND {cohorte} GROUP BY 1""").fetchall():
            cle = (code, 2000 + int(b))
            lignes[cle] = [x + (y or 0) for x, y in zip(lignes[cle], v)]
    con.close()
    print(f"{d} fait")

with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["epci_code", "annee", *CHAMPS])
    for (code, annee), v in sorted(lignes.items()):
        w.writerow([code, annee, *(round(x, 2) for x in v)])
print(f"Écrit : {OUT} ({len(lignes)} lignes) ; total vers_culture : {sum(v[1] for v in lignes.values()):,.0f} ha (attendu : environ 44 281)")
