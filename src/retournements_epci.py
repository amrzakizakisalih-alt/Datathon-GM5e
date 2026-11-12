"""Retournements de prairies permanentes par EPCI et par an, à partir de RPG Explorer.

Usage :
    python src/retournements_epci.py <seq1524_dXX.gpkg> <ref_fr_en.csv> <communes_XX.geojson> <sortie.csv>

Chaque LCP (plus petite parcelle commune) est rattachée à la commune qui contient un point
intérieur de sa géométrie, ou à défaut à la commune la plus proche, puis à l'EPCI de cette
commune (geo.api.gouv.fr).
Pour chaque paire d'années N -> N+1 :
  - stock_pp            : surface en prairie permanente (groupe 18 : PPH, PRL) l'année N
  - strict_anciennes    : PP anciennes (PP chaque année depuis 2015) passées en culture en N+1
  - strict_toutes       : toutes PP passées en culture en N+1
  - vers_pt / vers_fourrage / vers_gel : PP passées en prairie temporaire, en fourrage ou en gel
                          (groupe 11, surfaces gelées sans production : pas forcément un labour)
  - devenir_inconnu     : PP non déclarées en N+1 (sorties de la PAC, jamais comptées comme retournées)
  - borne_haute         : strict_toutes + vers_pt + vers_fourrage + vers_gel + devenir_inconnu
Une LCP qui alterne prairie et culture compte à chaque retournement : on compte des événements de labour,
pas des surfaces distinctes (1,3 % de la surface retournée 2015-2024 ; les prairies anciennes n'y sont pas sujettes).
"""
import sys

import duckdb

from geo_utils import rattacher_plus_proche

GPKG, REF, COMMUNES, OUT = sys.argv[1:5]
YEARS = [f"{y:02d}" for y in range(15, 25)]
CULTURE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 24, 25)  # le gel (groupe 11) est une classe à part

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")

con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{REF}', header=true)")
con.execute(f"""
    CREATE TABLE communes AS
    SELECT code AS insee, nom, codeEpci AS epci_code, json_extract_string(epci, '$.nom') AS epci_nom,
           ST_Transform(geom, 'EPSG:4326', 'EPSG:2154', always_xy := true) AS geom
    FROM ST_Read('{COMMUNES}')
""")

# Classe de chaque année : PP, PT, culture, fourrage, autre, ou NULL (non déclaré)
classes = ",\n".join(
    f"""CASE WHEN l.crop{y} IS NULL THEN NULL
             WHEN r{y}.grp = 18 THEN 'PP' WHEN r{y}.grp = 19 THEN 'PT'
             WHEN r{y}.grp IN {CULTURE} THEN 'culture' WHEN r{y}.grp = 16 THEN 'fourrage'
             WHEN r{y}.grp = 11 THEN 'gel' ELSE 'autre' END AS k{y}"""
    for y in YEARS
)
joins = "\n".join(f"LEFT JOIN ref r{y} ON r{y}.crop = l.crop{y}" for y in YEARS)
con.execute(f"""
    CREATE TABLE lcp AS
    SELECT l.id_lcp, l.area_lcp AS ha, ST_PointOnSurface(l.wkb_geometry) AS pt, {classes}
    FROM ST_Read('{GPKG}') l
    {joins}
""")

con.execute("""
    CREATE TABLE lcp_epci AS
    SELECT l.*, c.insee, c.epci_code, c.epci_nom
    FROM lcp l LEFT JOIN communes c ON ST_Within(l.pt, c.geom)
""")

n_tot, n_sans = con.execute(
    "SELECT count(*), count(*) FILTER (WHERE insee IS NULL) FROM lcp_epci").fetchone()
ha_sans = con.execute("SELECT coalesce(sum(ha), 0) FROM lcp_epci WHERE insee IS NULL").fetchone()[0]
print(f"LCP : {n_tot:,} ; sans commune : {n_sans:,} ({ha_sans:,.0f} ha)")
rattacher_plus_proche(con, "lcp_epci", "id_lcp", "t.pt")

pairs = []
for i in range(len(YEARS) - 1):
    a, b = YEARS[i], YEARS[i + 1]
    anciennes = " AND ".join(f"k{y} = 'PP'" for y in YEARS[: i + 1])
    pairs.append(f"""
        SELECT epci_code, epci_nom, 2000 + {int(b)} AS annee,
               sum(ha) FILTER (WHERE k{a} = 'PP') AS stock_pp,
               sum(ha) FILTER (WHERE {anciennes} AND k{b} = 'culture') AS strict_anciennes,
               sum(ha) FILTER (WHERE k{a} = 'PP' AND k{b} = 'culture') AS strict_toutes,
               sum(ha) FILTER (WHERE k{a} = 'PP' AND k{b} = 'PT') AS vers_pt,
               sum(ha) FILTER (WHERE k{a} = 'PP' AND k{b} = 'fourrage') AS vers_fourrage,
               sum(ha) FILTER (WHERE k{a} = 'PP' AND k{b} = 'gel') AS vers_gel,
               sum(ha) FILTER (WHERE k{a} = 'PP' AND k{b} IS NULL) AS devenir_inconnu
        FROM lcp_epci WHERE epci_code IS NOT NULL GROUP BY ALL""")

con.execute(f"""
    CREATE TABLE resultat AS
    SELECT epci_code, epci_nom, annee,
           round(coalesce(stock_pp, 0), 1) AS stock_pp,
           round(coalesce(strict_anciennes, 0), 1) AS strict_anciennes,
           round(coalesce(strict_toutes, 0), 1) AS strict_toutes,
           round(coalesce(vers_pt, 0), 1) AS vers_pt,
           round(coalesce(vers_fourrage, 0), 1) AS vers_fourrage,
           round(coalesce(vers_gel, 0), 1) AS vers_gel,
           round(coalesce(devenir_inconnu, 0), 1) AS devenir_inconnu,
           round(coalesce(strict_toutes, 0) + coalesce(vers_pt, 0) + coalesce(vers_fourrage, 0)
                 + coalesce(vers_gel, 0) + coalesce(devenir_inconnu, 0), 1) AS borne_haute
    FROM ({' UNION ALL '.join(pairs)})
    ORDER BY epci_nom, annee
""")
con.execute(f"COPY resultat TO '{OUT}' (HEADER, DELIMITER ';')")
print(f"Écrit : {OUT}")
