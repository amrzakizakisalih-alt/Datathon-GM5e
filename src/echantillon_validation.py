"""Échantillon de vérification sur photo aérienne des retournements de prairies détectés dans le RPG.

Usage :
    python src/echantillon_validation.py [n_par_strate_et_dep] [n_temoins_par_dep]

Tire au hasard (ordre fixé par une empreinte md5, donc reproductible), dans chaque département, des LCP d'au moins 1 ha :
  - RETOURNEMENTS : prairie permanente l'année N, culture l'année N+1, où N+1 est l'ANNÉE MÊME de la photo IGN
    (mosaïque 2021-2023). La déclaration de culture est donc confrontée à une photo de la même année, sans condition
    sur ce que devient la parcelle ensuite. Deux strates : « ancienne » (prairie permanente chaque année de 2015 à N)
    et « récente » (les autres). La parcelle doit aussi être déclarée en prairie l'année de la photo d'avant (mosaïque 2016-2020) ;
  - TÉMOINS : prairie permanente déclarée chaque année de 2018 à 2024.
Les dates de vol viennent du graphe de mosaïquage de l'IGN. Un point dont le graphe donne plusieurs années est écarté.

Écrit dans data/validation/ :
  - echantillon_retournements.csv : la clé de lecture (type, strate, codes), à ne pas ouvrir avant d'avoir lu les photos ;
  - poids_strates.csv : surface de chaque strate, pour pondérer le résultat ;
  - cache_dates.csv : dates déjà interrogées, pour que le tirage reste identique si on le relance.
Usage interne : ces fichiers localisent des parcelles agricoles ; ils ne doivent être ni publiés ni affichés.
Le protocole est décrit dans data/validation/LISEZ-MOI.md.
"""
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import duckdb

from definitions import ANNEES as YEARS, GRP_CULTURE as CULTURE, GRP_PP

N_STRATE = int(sys.argv[1]) if len(sys.argv) > 1 else 10
N_TEMOINS = int(sys.argv[2]) if len(sys.argv) > 2 else 10
RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
OUT = RACINE / "data" / "validation"
DEPS = ["14", "27", "50", "61", "76"]
GRAINE = "datathon-2026"
WFS = "https://data.geopf.fr/wfs/ows"
UA = {"User-Agent": "datathon-normandie-validation/1.0"}
GRAPHES = {"avant": "ORTHOIMAGERY.ORTHOPHOTOS.GRAPHE.2016-2020:graphe_bdortho", "apres": "ORTHOIMAGERY.ORTHOPHOTOS.GRAPHE.2021-2023:graphe_bdortho"}
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
OUT.mkdir(parents=True, exist_ok=True)

CACHE = OUT / "cache_dates.csv"
cache = {}
if CACHE.exists():
    for r in csv.DictReader(open(CACHE, encoding="utf-8"), delimiter=";"):
        cache[(r["periode"], r["lon"], r["lat"])] = r["dates"]


def dates_vol(periode, lon, lat):
    """Dates de vol du graphe de mosaïquage au point. Liste vide si le service échoue ou si le point n'est pas couvert."""
    cle = (periode, str(lon), str(lat))
    if cle in cache:
        return cache[cle].split(",") if cache[cle] else []
    p = {"SERVICE": "WFS", "VERSION": "2.0.0", "REQUEST": "GetFeature", "TYPENAMES": GRAPHES[periode], "OUTPUTFORMAT": "application/json",
         "COUNT": 20, "PROPERTYNAME": "dep,pva,date_vol", "BBOX": f"{lat - 1e-5},{lon - 1e-5},{lat + 1e-5},{lon + 1e-5},urn:ogc:def:crs:EPSG::4326"}
    for essai in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(WFS + "?" + urllib.parse.urlencode(p), headers=UA), timeout=45) as f:
                dates = sorted({x["properties"]["date_vol"][:10] for x in json.load(f)["features"]})
            cache[cle] = ",".join(dates)
            return dates
        except Exception:
            time.sleep(2 * (essai + 1))
    return []


def tirer(lignes, quota, eligible):
    """Parcourt les candidats dans leur ordre fixe et garde les `quota` premiers éligibles."""
    gardes, ecartes = [], 0
    for i in range(0, len(lignes), 30):
        lot = lignes[i:i + 30]
        with ThreadPoolExecutor(3) as ex:
            av = list(ex.map(lambda x: dates_vol("avant", x["lon"], x["lat"]), lot))
            ap = list(ex.map(lambda x: dates_vol("apres", x["lon"], x["lat"]), lot))
        for x, da, dp in zip(lot, av, ap):
            ya, yp = {d[:4] for d in da}, {d[:4] for d in dp}
            if len(ya) == 1 and len(yp) == 1 and eligible(x, int(ya.pop()), int(yp.pop())):
                x["date_photo_avant"], x["date_photo_apres"] = da[0], dp[0]
                gardes.append(x)
                if len(gardes) == quota:
                    return gardes, ecartes
            else:
                ecartes += 1
    return gardes, ecartes


con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true)")
echantillon, poids = [], []
for d in DEPS:
    g = ", ".join(f"r{y}.grp AS g{y}, l.crop{y} AS c{y}" for y in YEARS)
    j = " ".join(f"LEFT JOIN ref r{y} ON r{y}.crop = l.crop{y}" for y in YEARS)
    con.execute(f"""CREATE OR REPLACE TABLE l AS
        SELECT l.id_lcp, l.area_lcp AS ha, l.wkb_geometry AS geom, {g}
        FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{d}.gpkg'}') l {j}""")
    # N+1 de 2021 à 2023 : les années couvertes par la mosaïque 2021-2023
    pos = " UNION ALL ".join(f"""SELECT id_lcp, ha, geom, 2000 + {int(YEARS[i])} AS annee_avant, c{YEARS[i]} AS code_avant, c{YEARS[i + 1]} AS code_apres,
            CASE WHEN {' AND '.join(f'g{y} = {GRP_PP}' for y in YEARS[:i + 1])} THEN 'ancienne' ELSE 'récente' END AS strate,
            [{', '.join(f'g{y}' for y in YEARS)}] AS grp
        FROM l WHERE g{YEARS[i]} = {GRP_PP} AND g{YEARS[i + 1]} IN {CULTURE}""" for i in (5, 6, 7))
    con.execute(f"CREATE OR REPLACE TABLE pos AS {pos}")
    for strate, ha_ge1, ha_tout, n in con.execute("SELECT strate, sum(ha) FILTER (WHERE ha >= 1), sum(ha), count(*) FILTER (WHERE ha >= 1) FROM pos GROUP BY 1").fetchall():
        poids.append({"dep": d, "strate": strate, "ha_lcp_1ha_et_plus": round(ha_ge1 or 0, 1), "ha_toutes_lcp": round(ha_tout or 0, 1), "n_lcp_1ha_et_plus": n})

    def candidats(requete):
        cols = ["id_lcp", "ha", "lat", "lon", "annee_avant", "code_avant", "code_apres", "strate", "grp", "wkt"]
        return [dict(zip(cols, r)) for r in con.execute(requete).fetchall()]

    pt = "ST_Transform(ST_PointOnSurface(geom), 'EPSG:2154', 'EPSG:4326', always_xy := true)"
    for strate in ("ancienne", "récente"):
        lignes = candidats(f"""SELECT id_lcp, round(ha, 2), round(ST_Y({pt}), 6), round(ST_X({pt}), 6), annee_avant, code_avant, code_apres, strate, grp, ST_AsText(geom)
            FROM pos WHERE strate = '{strate}' AND ha >= 1 ORDER BY md5(id_lcp || annee_avant || '{GRAINE}')""")
        # La photo d'après est de l'année N+1, et la parcelle est déclarée en prairie l'année de la photo d'avant
        gardes, ecartes = tirer(lignes, N_STRATE, lambda x, ya, yp: yp == x["annee_avant"] + 1 and ya <= x["annee_avant"] and x["grp"][ya - 2015] == GRP_PP)
        print(f"{d} {strate} : {len(gardes)} retenus, {ecartes} candidats écartés sur {len(lignes)} disponibles")
        echantillon += [{**x, "dep": d, "type": "retournement détecté"} for x in gardes]
    neg = " AND ".join(f"g{y} = {GRP_PP}" for y in YEARS[3:])
    lignes = candidats(f"""SELECT id_lcp, round(ha, 2), round(ST_Y({pt}), 6), round(ST_X({pt}), 6), NULL, c18, c24, 'témoin', NULL, ST_AsText(geom)
        FROM l WHERE ha >= 1 AND {neg} ORDER BY md5(id_lcp || '{GRAINE}')""")
    gardes, ecartes = tirer(lignes, N_TEMOINS, lambda x, ya, yp: True)
    print(f"{d} témoins : {len(gardes)} retenus, {ecartes} candidats écartés sur {len(lignes)} disponibles")
    echantillon += [{**x, "dep": d, "type": "prairie maintenue"} for x in gardes]

with open(CACHE, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["periode", "lon", "lat", "dates"])
    w.writerows([*k, v] for k, v in cache.items())
with open(OUT / "poids_strates.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(poids[0]), delimiter=";")
    w.writeheader()
    w.writerows(poids)
COLS = ["num", "dep", "type", "strate", "id_lcp", "ha", "lat", "lon", "annee_avant", "code_avant", "code_apres", "date_photo_avant", "date_photo_apres", "wkt"]
with open(OUT / "echantillon_retournements.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, delimiter=";", extrasaction="ignore")
    w.writeheader()
    for i, x in enumerate(echantillon, 1):
        w.writerow({**x, "num": i})
print(f"Écrit : {OUT / 'echantillon_retournements.csv'} ({len(echantillon)} points)")
