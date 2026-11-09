"""Outils des tests : fabriquent de mini-jeux de données dont on connaît le résultat à l'avance.

Le territoire fictif fait 2 km sur 1 km, en Lambert 93 :
  commune A (insee 99001, EPCI E1) : x de 600 000 à 601 000
  commune B (insee 99002, EPCI E2) : x de 601 000 à 602 000
  y de 6 900 000 à 6 901 000 pour les deux.
Les LCP sont des rectangles de 100 m de côté (1 ha), sauf indication contraire.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

import duckdb
import pytest

RACINE = Path(__file__).resolve().parent.parent
SRC = RACINE / "src"
sys.path.insert(0, str(SRC))

ANNEES = [f"{y:02d}" for y in range(15, 25)]
# Codes de culture fictifs et leur groupe RPG (seules les colonnes crop et grp sont lues)
REF = {"PPH": 18, "PRL": 18, "PTR": 19, "BTH": 1, "JAC": 11, "FOU": 16, "VRG": 20}
Y0 = 6_900_000


def rect(x0, x1, y0=Y0, y1=Y0 + 100):
    return f"POLYGON(({x0} {y0},{x1} {y0},{x1} {y1},{x0} {y1},{x0} {y0}))"


def connexion():
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    return con


def ecrire_ref(dossier):
    chemin = dossier / "ref.csv"
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["crop", "grp"])
        w.writerows(REF.items())
    return chemin


def ecrire_communes(dossier):
    """communes_99.geojson, au format de geo.api.gouv.fr (WGS84, epci en objet JSON)."""
    con = connexion()
    objets = []
    for code, nom, epci, x0 in [("99001", "A", "E1", 600_000), ("99002", "B", "E2", 601_000)]:
        gj = con.execute(f"""SELECT ST_AsGeoJSON(ST_Transform(ST_GeomFromText('{rect(x0, x0 + 1000, Y0, Y0 + 1000)}'),
                             'EPSG:2154', 'EPSG:4326', always_xy := true))""").fetchone()[0]
        objets.append({"type": "Feature", "geometry": json.loads(gj),
                       "properties": {"code": code, "nom": nom, "codeEpci": epci,
                                      "epci": {"code": epci, "nom": f"EPCI {epci}"}}})
    dossier_geo = dossier / "geo"
    dossier_geo.mkdir(exist_ok=True)
    with open(dossier_geo / "communes_99.geojson", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": objets}, f)
    return dossier_geo


def ecrire_lcp(dossier, lcp):
    """seq1524_d99.gpkg au format de RPG Explorer. lcp : liste de (id, wkt, ha, [10 codes ou None])."""
    con = connexion()
    lignes = []
    for id_lcp, wkt, ha, crops in lcp:
        valeurs = ", ".join("NULL" if c is None else f"'{c}'" for c in crops)
        lignes.append(f"SELECT '{id_lcp}' AS id_lcp, {ha}::DOUBLE AS area_lcp, "
                      + ", ".join(f"{v} AS crop{y}" for v, y in zip(valeurs.split(", "), ANNEES))
                      + f", ST_GeomFromText('{wkt}') AS wkb_geometry")
    chemin = dossier / "seq1524_d99.gpkg"
    con.execute(f"""COPY ({' UNION ALL '.join(lignes)}) TO '{chemin}'
                    WITH (FORMAT GDAL, DRIVER 'GPKG', SRS 'EPSG:2154', LAYER_CREATION_OPTIONS 'GEOMETRY_NAME=wkb_geometry')""")
    return chemin


def ecrire_ocsge(dossier, polygones, a0=2019, a1=2022):
    """Couche OCS GE différentielle. polygones : liste de (fid, wkt, artificialisation, cs_debut, us_debut)."""
    con = connexion()
    # pas de colonne fid : le GeoPackage numérote lui-même les objets, et ST_Read la renvoie sous ce nom
    lignes = [f"SELECT {art} AS artificialisation, '{cs}' AS cs_{a0}, '{us}' AS us_{a0}, "
              f"'CS1.1.1.1' AS cs_{a1}, 'US235' AS us_{a1}, ST_GeomFromText('{wkt}') AS geom"
              for _, wkt, art, cs, us in polygones]
    chemin = dossier / "ocsge.gpkg"
    con.execute(f"""COPY ({' UNION ALL '.join(lignes)}) TO '{chemin}'
                    WITH (FORMAT GDAL, DRIVER 'GPKG', SRS 'EPSG:2154', LAYER_CREATION_OPTIONS 'GEOMETRY_NAME=geom')""")
    return chemin


def lancer(script, *args):
    res = subprocess.run([sys.executable, str(SRC / script), *map(str, args)], cwd=RACINE,
                         capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    return res.stdout


def lire_csv(chemin):
    with open(chemin, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


@pytest.fixture
def dossier(tmp_path):
    return tmp_path
