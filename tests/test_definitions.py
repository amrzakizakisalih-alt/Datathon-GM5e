"""Tests de definitions.py : classes RPG, retournement strict, prairies anciennes."""
import duckdb

from conftest import ANNEES, REF
from definitions import annees_entre, classes_sql, jointures_ref, pp_ancienne_sql, retournement_sql


def classer(crops, non_declare="NULL"):
    """Classe une LCP fictive avec les expressions SQL de definitions.py."""
    con = duckdb.connect()
    con.execute("CREATE TABLE ref (crop VARCHAR, grp INTEGER)")
    con.executemany("INSERT INTO ref VALUES (?, ?)", list(REF.items()))
    valeurs = ", ".join("NULL" if c is None else f"'{c}'" for c in crops)
    con.execute(f"CREATE TABLE l AS SELECT " + ", ".join(
        f"{v}::VARCHAR AS crop{y}" for v, y in zip(valeurs.split(", "), ANNEES)))
    con.execute(f"CREATE TABLE k AS SELECT {classes_sql(non_declare=non_declare)} FROM l {jointures_ref()}")
    return con, con.execute("SELECT * FROM k").fetchone()


def test_classes():
    _, k = classer(["PPH", "PTR", "BTH", "JAC", "FOU", "VRG", None, "PPH", "PPH", "PPH"])
    assert k == ("PP", "PT", "culture", "gel", "fourrage", "autre", None, "PP", "PP", "PP")


def test_non_declare_personnalise():
    _, k = classer([None] * 10, non_declare="'non déclaré'")
    assert set(k) == {"non déclaré"}


def test_gel_n_est_pas_un_retournement():
    con, _ = classer(["PPH"] * 5 + ["JAC"] * 5)
    assert con.execute(f"SELECT {retournement_sql('19', '20')} FROM k").fetchone()[0] is False


def test_retournement_strict():
    con, _ = classer(["PPH"] * 5 + ["BTH"] * 5)
    assert con.execute(f"SELECT {retournement_sql('19', '20')} FROM k").fetchone()[0] is True
    assert con.execute(f"SELECT {retournement_sql('18', '19')} FROM k").fetchone()[0] is False


def test_prairie_ancienne():
    # PP chaque année de 2015 à 2019 : ancienne pour le passage 2019 -> 2020
    con, _ = classer(["PPH"] * 5 + ["BTH"] * 5)
    assert con.execute(f"SELECT {pp_ancienne_sql('19')} FROM k").fetchone()[0] is True
    # PT en 2015 puis PP (comme le reclassement de 2018) : jamais ancienne
    con, _ = classer(["PTR"] + ["PPH"] * 4 + ["BTH"] * 5)
    assert con.execute(f"SELECT {pp_ancienne_sql('19')} FROM k").fetchone()[0] is False
    # Un trou de déclaration casse aussi l'ancienneté
    con, _ = classer(["PPH", "PPH", None, "PPH", "PPH"] + ["BTH"] * 5)
    assert not con.execute(f"SELECT {pp_ancienne_sql('19')} FROM k").fetchone()[0]


def test_annees_entre():
    assert annees_entre(2019, 2022) == ["19", "20", "21", "22"]


def test_prl_est_une_prairie_permanente():
    # PRL (prairie en rotation longue) fait partie du groupe 18 : c'est une PP pour toutes les définitions communes
    _, k = classer(["PRL"] * 5 + ["BTH"] * 5)
    assert k[:5] == ("PP",) * 5 and k[5] == "culture"


def test_annee_non_declaree_n_efface_pas_les_autres_retournements():
    # PP en 2015, culture en 2016 (un retournement), PP en 2017, non déclarée en 2018.
    # Avec non_declare = NULL, le terme 2017 -> 2018 vaut NULL et rend toute la somme NULL.
    somme = " + ".join(f"({retournement_sql(a, b)})::INT" for a, b in zip(ANNEES, ANNEES[1:4]))
    crops = ["PPH", "BTH", "PPH", None] + ["PPH"] * 6
    con, _ = classer(crops)
    assert con.execute(f"SELECT {somme} FROM k").fetchone()[0] is None          # le piège
    con, _ = classer(crops, non_declare="'non déclaré'")
    assert con.execute(f"SELECT {somme} FROM k").fetchone()[0] == 1             # la bonne pratique
