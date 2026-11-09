"""Tests de geo_utils.py : chargement des communes et rattachement à la commune la plus proche."""
import pytest

from conftest import connexion, ecrire_communes
from geo_utils import charger_communes, rattacher_plus_proche


def test_charger_communes_lit_tous_les_fichiers(dossier):
    geo = ecrire_communes(dossier)
    # un second département fictif : charger_communes doit lire les deux fichiers
    (geo / "communes_98.geojson").write_text((geo / "communes_99.geojson").read_text()
                                             .replace("99001", "98001").replace("99002", "98002"))
    con = connexion()
    charger_communes(con, geo)
    assert con.execute("SELECT count(*) FROM communes").fetchone()[0] == 4


def test_charger_communes_reprojette_en_lambert93(dossier):
    con = connexion()
    charger_communes(con, ecrire_communes(dossier))
    surface = con.execute("SELECT ST_Area(geom) FROM communes WHERE insee = '99001'").fetchone()[0]
    assert surface == pytest.approx(1e6, rel=1e-3)   # 1 km² en m²


def test_charger_communes_dossier_vide(dossier):
    with pytest.raises(FileNotFoundError):
        charger_communes(connexion(), dossier)


def test_rattacher_plus_proche(dossier):
    con = connexion()
    charger_communes(con, ecrire_communes(dossier))
    con.execute("""CREATE TABLE objets AS SELECT * FROM (VALUES
        ('dedans', ST_Point(600500, 6900500), '99001', 'E1', 'EPCI E1'),
        ('pres_de_B', ST_Point(602050, 6900500), NULL, NULL, NULL),
        ('pres_de_A', ST_Point(599900, 6900500), NULL, NULL, NULL)) t(id, pt, insee, epci_code, epci_nom)""")
    rattacher_plus_proche(con, "objets", "id", "t.pt")
    res = dict(con.execute("SELECT id, epci_code FROM objets").fetchall())
    assert res == {"dedans": "E1", "pres_de_B": "E2", "pres_de_A": "E1"}
