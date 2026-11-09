"""Tests de bout en bout : retournements_epci.py et beton_charrue_epci.py sur un territoire fictif.

Chaque LCP fictive illustre un cas, et le résultat attendu est calculé à la main (voir les commentaires).
"""
import pytest

from conftest import ecrire_communes, ecrire_lcp, ecrire_ocsge, ecrire_ref, lancer, lire_csv, rect

PP, PT, CU, GEL = "PPH", "PTR", "BTH", "JAC"


def par_cle(lignes, *cles):
    return {tuple(l[c] for c in cles): l for l in lignes}


@pytest.fixture
def retournements(dossier):
    lcp = [
        # L1 (A) : prairie ancienne retournée en 2020
        ("L1", rect(600_000, 600_100), 1, [PP] * 5 + [CU] * 5),
        # L2 (A) : PT jusqu'en 2017, PP de 2018 à 2021 (cas du reclassement de 2018), culture en 2022
        ("L2", rect(600_200, 600_300), 1, [PT] * 3 + [PP] * 4 + [CU] * 3),
        # L3 (A) : PP mise en jachère en 2020, ce n'est pas un retournement
        ("L3", rect(600_400, 600_500), 1, [PP] * 5 + [GEL] * 5),
        # L4 (B) : PP non déclarée en 2023 (trou de déclaration), de nouveau PP en 2024
        ("L4", rect(601_000, 601_100), 1, [PP] * 8 + [None, PP]),
        # L5 : hors des contours, juste à l'est de B ; prairie ancienne retournée en 2017
        ("L5", rect(602_010, 602_110), 1, [PP] * 2 + [CU] * 8),
    ]
    sortie = dossier / "ret.csv"
    lancer("retournements_epci.py", ecrire_lcp(dossier, lcp), ecrire_ref(dossier), ecrire_communes(dossier), sortie)
    return par_cle(lire_csv(sortie), "epci_code", "annee")


def test_retournement_ancien(retournements):
    r = retournements[("E1", "2020")]
    assert float(r["stock_pp"]) == 3          # L1, L2 et L3 sont en PP en 2019
    assert float(r["strict_toutes"]) == 1     # L1
    assert float(r["strict_anciennes"]) == 1  # L1 est en PP depuis 2015


def test_gel_hors_charrue_mais_dans_la_borne_haute(retournements):
    r = retournements[("E1", "2020")]
    assert float(r["vers_gel"]) == 1                          # L3
    assert float(r["borne_haute"]) == 2                       # L1 + L3


def test_reclassement_2018_pas_ancien(retournements):
    r = retournements[("E1", "2022")]
    assert float(r["strict_toutes"]) == 1      # L2
    assert float(r["strict_anciennes"]) == 0   # L2 était en PT en 2015


def test_trou_de_declaration(retournements):
    r = retournements[("E2", "2023")]
    assert float(r["devenir_inconnu"]) == 1   # L4
    assert float(r["strict_toutes"]) == 0


def test_rattachement_hors_contours(retournements):
    r = retournements[("E2", "2017")]
    assert float(r["strict_toutes"]) == 1     # L5, rattachée à B, la commune la plus proche
    assert float(r["stock_pp"]) == 2          # L4 + L5


@pytest.fixture
def beton(dossier):
    lcp = [
        # L1 (A, 2 ha) : prairie ancienne retournée en 2020, dont la moitié est bétonnée
        ("L1", rect(600_000, 600_200), 2, [PP] * 5 + [CU] * 5),
        # L2 (B) : prairie ancienne retournée en 2021, sans béton
        ("L2", rect(601_000, 601_100), 1, [PP] * 6 + [CU] * 4),
        # L3 (B) : PP mise en jachère en 2020
        ("L3", rect(601_200, 601_300), 1, [PP] * 5 + [GEL] * 5),
    ]
    ocsge = [
        # béton sur la moitié est de L1 (1 ha d'herbe agricole, déclarée)
        (1, rect(600_100, 600_200), 1, "CS2.2.1", "US1.1"),
        # béton sur 1 ha d'herbe agricole hors de toute parcelle déclarée, dans B
        (2, rect(601_500, 601_600, 6_900_500, 6_900_600), 1, "CS2.2.1", "US1.1"),
        # désartificialisation dans A : un sol revêtu rendu (1 ha), puis un simple changement d'usage (1 ha)
        (3, rect(600_500, 600_600, 6_900_500, 6_900_600), -1, "CS1.1.1.1", "US235"),
        (4, rect(600_700, 600_800, 6_900_500, 6_900_600), -1, "CS2.2.1", "US235"),
    ]
    sortie = dossier / "bc.csv"
    lancer("beton_charrue_epci.py", ecrire_ocsge(dossier, ocsge), 2019, 2022, ecrire_lcp(dossier, lcp),
           ecrire_ref(dossier), ecrire_communes(dossier), sortie)
    return par_cle(lire_csv(sortie), "epci_code")


def test_le_beton_l_emporte_sur_la_charrue(beton):
    r = beton[("E1",)]
    assert float(r["beton_sur_pp"]) == pytest.approx(1)
    assert float(r["charrue_pp"]) == pytest.approx(1)            # 2 ha retournés - 1 ha bétonné
    assert float(r["charrue_pp_anciennes"]) == pytest.approx(1)
    assert float(r["prairies_perdues"]) == pytest.approx(2)
    assert float(r["part_beton_pct"]) == pytest.approx(50)
    assert float(r["beton_herbe_hors_pac"]) == pytest.approx(0)  # l'herbe bétonnée est déclarée


def test_desartificialisation(beton):
    r = beton[("E1",)]
    assert float(r["desartif_sols"]) == pytest.approx(1)
    assert float(r["desartif_usage"]) == pytest.approx(1)


def test_prairies_probables_hors_pac(beton):
    r = beton[("E2",)]
    assert float(r["beton_total"]) == pytest.approx(1)
    assert float(r["beton_herbe_hors_pac"]) == pytest.approx(1)
    assert float(r["beton_hors_rpg"]) == pytest.approx(1)
    assert float(r["charrue_pp"]) == pytest.approx(1)            # L2 seulement : L3 est en jachère
    assert float(r["part_beton_pct"]) == pytest.approx(0)        # borne basse : aucun béton sur PP déclarée
    assert float(r["part_beton_haute_pct"]) == pytest.approx(50)  # borne haute : 1 ha hors PAC / 2 ha


@pytest.fixture
def beton_a_cheval(dossier):
    # L4 (A, 2 ha) : PP déclarée toute la période, jamais retournée
    lcp = [("L4", rect(600_800, 601_000), 2, [PP] * 10)]
    # Un polygone de béton de 3 ha à cheval sur A et B (x de 600 900 à 601 200) : son point intérieur tombe dans B.
    # Il recouvre 1 ha de L4, dans A.
    ocsge = [(1, rect(600_900, 601_200), 1, "CS2.2.1", "US1.1")]
    sortie = dossier / "bc_cheval.csv"
    lancer("beton_charrue_epci.py", ecrire_ocsge(dossier, ocsge), 2019, 2022, ecrire_lcp(dossier, lcp),
           ecrire_ref(dossier), ecrire_communes(dossier), sortie)
    return par_cle(lire_csv(sortie), "epci_code")


def test_beton_a_cheval_ventile_selon_l_epci_du_polygone(beton_a_cheval):
    b = beton_a_cheval[("E2",)]
    # Tout le béton du polygone, y compris la partie posée sur la PP de A, est compté dans l'EPCI du polygone
    assert float(b["beton_total"]) == pytest.approx(3)
    assert float(b["beton_sur_pp"]) == pytest.approx(1)
    assert float(b["beton_hors_rpg"]) == pytest.approx(2)        # jamais négatif : les parts s'additionnent
    assert float(b["beton_herbe_hors_pac"]) == pytest.approx(2)  # 3 ha d'herbe agricole - 1 ha déclaré
    a = beton_a_cheval[("E1",)]
    assert float(a["beton_total"]) == pytest.approx(0) and float(a["beton_sur_pp"]) == pytest.approx(0)
