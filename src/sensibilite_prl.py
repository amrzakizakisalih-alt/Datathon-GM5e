"""Poids du code PRL (prairie en rotation longue, supprimé en 2023) dans la charrue.

Usage :
    python src/sensibilite_prl.py

À lancer après pipeline.py. Recalcule les retournements par EPCI et par an en séparant les codes PPH et PRL, vérifie que
les totaux redonnent ceux de retournements_epci_XX.csv, puis fait varier la définition des prairies permanentes :
  - référence        : PPH et PRL sont des prairies permanentes (choix de l'outil) ;
  - sans PRL         : PRL n'est plus une prairie permanente, ni au numérateur ni dans le stock ;
  - sans PRL en 2023 : seuls les passages PRL -> culture de 2022 -> 2023, l'année où le code disparaît, sont retirés ;
  - PPH seule (anciennes) : prairies déclarées PPH chaque année depuis 2015.
Écrit data/processed/sensibilite_prl.csv (une ligne par mesure) et sensibilite_prl_epci.csv (fourchette de chaque EPCI), agrégats seulement.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import duckdb
import numpy as np

from definitions import ANNEES as YEARS, CODE_PPH, CODE_PRL, classes_sql, jointures_ref, pp_ancienne_sql, retournement_sql
from geo_utils import charger_communes, rattacher_plus_proche

RACINE = Path(__file__).resolve().parent.parent
RAW, OUT = RACINE / "data" / "raw", RACINE / "data" / "processed"
DEPS = ["14", "27", "50", "61", "76"]
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

CHAMPS = ["toutes", "anciennes", "prl", "anciennes_prl", "anciennes_pph", "stock_pph", "stock_prl"]
epci = defaultdict(lambda: defaultdict(float))  # (epci, annee) -> champ -> ha
devenir = defaultdict(float)  # (annee, code d'origine, devenir) -> ha
codes_2023 = defaultdict(float)  # code déclaré en 2023 sur une PRL de 2022 -> ha
for d in DEPS:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute(f"CREATE TABLE ref AS SELECT crop, CAST(grp AS INTEGER) AS grp FROM read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true)")
    charger_communes(con, RAW / "geo")  # les 5 départements, comme la pipeline
    classes = ", ".join(f"l.crop{y} AS c{y}" for y in YEARS) + ", " + classes_sql()
    joins = jointures_ref()
    con.execute(f"""CREATE TABLE lcp AS SELECT l.id_lcp, l.area_lcp AS ha, ST_PointOnSurface(l.wkb_geometry) AS pt, {classes}
        FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{d}.gpkg'}') l {joins}""")
    con.execute("CREATE TABLE lcp_epci AS SELECT l.*, c.insee, c.epci_code, c.epci_nom FROM lcp l LEFT JOIN communes c ON ST_Within(l.pt, c.geom)")
    rattacher_plus_proche(con, "lcp_epci", "id_lcp", "t.pt")
    for i in range(len(YEARS) - 1):
        a, b = YEARS[i], YEARS[i + 1]
        annee = 2000 + int(b)
        anciennes = pp_ancienne_sql(a)
        pph_seule = " AND ".join(f"c{y} = '{CODE_PPH}'" for y in YEARS[: i + 1])
        retourne = retournement_sql(a, b)
        for code, *v in con.execute(f"""SELECT epci_code,
                sum(ha) FILTER (WHERE {retourne}),
                sum(ha) FILTER (WHERE {anciennes} AND {retourne}),
                sum(ha) FILTER (WHERE c{a} = '{CODE_PRL}' AND {retourne}),
                sum(ha) FILTER (WHERE {anciennes} AND c{a} = '{CODE_PRL}' AND {retourne}),
                sum(ha) FILTER (WHERE {pph_seule} AND k{b} = 'culture'),
                sum(ha) FILTER (WHERE c{a} = '{CODE_PPH}'),
                sum(ha) FILTER (WHERE c{a} = '{CODE_PRL}')
                FROM lcp_epci WHERE epci_code IS NOT NULL GROUP BY 1""").fetchall():
            for champ, x in zip(CHAMPS, v):
                epci[(code, annee)][champ] += x or 0
        for orig, dev, ha in con.execute(f"""SELECT c{a}, CASE WHEN c{b} IN ('PPH', 'PRL') THEN c{b} ELSE coalesce(k{b}, 'non déclaré') END, sum(ha)
                FROM lcp_epci WHERE epci_code IS NOT NULL AND c{a} IN ('PPH', 'PRL') GROUP BY 1, 2""").fetchall():
            devenir[(annee, orig, dev)] += ha
    for code, ha in con.execute("SELECT coalesce(c23, 'non déclaré'), sum(ha) FROM lcp_epci WHERE epci_code IS NOT NULL AND c22 = 'PRL' GROUP BY 1").fetchall():
        codes_2023[code] += ha
    con.close()
    print(f"{d} fait")

# Contrôle : mêmes totaux que le pipeline
ref = duckdb.sql(f"SELECT sum(strict_toutes), sum(strict_anciennes) FROM read_csv_auto('{OUT / 'retournements_epci_*.csv'}', delim=';', header=true)").fetchone()
tout = sum(v["toutes"] for v in epci.values())
anc = sum(v["anciennes"] for v in epci.values())
resultats = []


def note(theme, test, mesure, valeur, lecture=""):
    resultats.append({"theme": theme, "test": test, "mesure": mesure, "valeur": valeur, "lecture": lecture})
    print(f"[{theme}] {test} | {mesure} = {valeur}{' | ' + lecture if lecture else ''}")


def rangs_moyens(x):
    """Rangs de x, les ex aequo recevant la moyenne de leurs rangs (définition standard de Spearman)."""
    o = x.argsort(kind="mergesort")
    rg = np.empty(len(x))
    rg[o] = np.arange(len(x))
    for val in np.unique(x):
        rg[x == val] = rg[x == val].mean()
    return rg


def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = ~(np.isnan(a) | np.isnan(b))
    return round(float(np.corrcoef(rangs_moyens(a[ok]), rangs_moyens(b[ok]))[0, 1]), 3)


note("Contrôle", "total charrue toutes PP, écart au pipeline", "ha", round(tout - ref[0], 1), "doit valoir environ 0")
note("Contrôle", "total charrue anciennes, écart au pipeline", "ha", round(anc - ref[1], 1), "doit valoir environ 0")

ANNEES = range(2016, 2025)
par_an = {y: defaultdict(float) for y in ANNEES}
for (_, y), v in epci.items():
    for c in CHAMPS:
        par_an[y][c] += v[c]
for y in ANNEES:
    p = par_an[y]
    note("Par année", f"{y - 1} -> {y}", "charrue / dont depuis PRL / part PRL",
         f"{p['toutes']:.0f} / {p['prl']:.0f} / {100 * p['prl'] / p['toutes']:.1f} %", f"stock PRL {p['stock_prl']:.0f} ha, PPH {p['stock_pph']:.0f} ha")


def total(f):
    return sum(f(y, par_an[y]) for y in ANNEES) / 9


bases = {"toutes": total(lambda y, p: p["toutes"]), "anciennes": total(lambda y, p: p["anciennes"])}
scen = {
    "sans PRL (toutes années)": (total(lambda y, p: p["toutes"] - p["prl"]), total(lambda y, p: p["anciennes"] - p["anciennes_prl"])),
    "sans PRL en 2023": (total(lambda y, p: p["toutes"] - (p["prl"] if y == 2023 else 0)), total(lambda y, p: p["anciennes"] - (p["anciennes_prl"] if y == 2023 else 0))),
    "PPH seule chaque année depuis 2015": (None, total(lambda y, p: p["anciennes_pph"])),
}
note("Région", "référence (moyenne 2015->2024)", "charrue toutes / anciennes, ha/an", f"{bases['toutes']:.0f} / {bases['anciennes']:.0f}")
for nom, (t, a) in scen.items():
    if t is not None:
        note("Région", nom, "charrue toutes, ha/an (écart)", f"{t:.0f} ({100 * (t / bases['toutes'] - 1):+.1f} %)")
    note("Région", nom, "charrue anciennes, ha/an (écart)", f"{a:.0f} ({100 * (a / bases['anciennes'] - 1):+.1f} %)")

for y in (2022, 2023, 2024):
    for orig in ("PRL", "PPH"):
        d = {k[2]: v for k, v in devenir.items() if k[0] == y and k[1] == orig}
        s = sum(d.values())
        if s:
            note("Devenir", f"{orig} de {y - 1}, déclaré en {y}", "répartition", ", ".join(f"{k} {100 * v / s:.1f} %" for k, v in sorted(d.items(), key=lambda x: -x[1])), f"{s:.0f} ha")
s = sum(codes_2023.values())
note("Devenir", "codes déclarés en 2023 sur les PRL de 2022", "principaux", ", ".join(f"{k} {100 * v / s:.1f} %" for k, v in sorted(codes_2023.items(), key=lambda x: -x[1])[:8]), f"{s:.0f} ha")

# Classement des EPCI : charrue moyenne rapportée au stock de 2015
t = duckdb.sql(f"SELECT epci_code::VARCHAR, epci_nom, exclu_comparaisons FROM read_csv_auto('{OUT / 'tableau_regional_epci.csv'}', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})").fetchall()
codes = [r[0] for r in t if not r[2]]
noms = {r[0]: r[1] for r in t}


def v(code, champ, annees=ANNEES):
    return sum(epci[(code, y)][champ] for y in annees)


s_pp = {c: epci[(c, 2016)]["stock_pph"] + epci[(c, 2016)]["stock_prl"] for c in codes}
s_ph = {c: epci[(c, 2016)]["stock_pph"] for c in codes}
ind = {
    "ref": [v(c, "toutes") / 9 / s_pp[c] for c in codes],
    "sans": [(v(c, "toutes") - v(c, "prl")) / 9 / s_ph[c] if s_ph[c] else np.nan for c in codes],
    "sans23": [(v(c, "toutes") - epci[(c, 2023)]["prl"]) / 9 / s_pp[c] for c in codes],
    "anc": [v(c, "anciennes") / 9 / s_pp[c] for c in codes],
    "anc_sans": [(v(c, "anciennes") - v(c, "anciennes_prl")) / 9 / s_ph[c] if s_ph[c] else np.nan for c in codes],
}


def top(cle, n=10):
    a = np.nan_to_num(np.asarray(ind[cle], float), nan=-1)
    return {codes[i] for i in a.argsort()[-n:]}


note("Classement EPCI", "toutes PP : référence vs sans PRL", "Spearman / top 10 commun", f"{spearman(ind['ref'], ind['sans'])} / {len(top('ref') & top('sans'))}", f"{len(codes)} EPCI")
note("Classement EPCI", "toutes PP : référence vs sans PRL en 2023", "Spearman / top 10 commun", f"{spearman(ind['ref'], ind['sans23'])} / {len(top('ref') & top('sans23'))}")
note("Classement EPCI", "anciennes : référence vs sans PRL", "Spearman / top 10 commun", f"{spearman(ind['anc'], ind['anc_sans'])} / {len(top('anc') & top('anc_sans'))}")
parts = sorted(((100 * v(c, "prl") / v(c, "toutes"), c) for c in codes if v(c, "toutes") >= 9), reverse=True)
note("EPCI", "part de la charrue venant de PRL", "médiane / max", f"{np.median([p for p, _ in parts]):.1f} % / {parts[0][0]:.1f} %", noms[parts[0][1]])
for p, c in parts[:5]:
    note("EPCI", f"part PRL la plus forte : {noms[c]}", "part / charrue moyenne", f"{p:.1f} % / {v(c, 'toutes') / 9:.0f} ha/an")

with open(OUT / "sensibilite_prl_epci.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, delimiter=";")
    w.writerow(["epci_code", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_sans_prl_ha_an", "part_prl_charrue_pct"])
    for c, *_ in t:
        tot = v(c, "toutes")
        w.writerow([c, round((tot - v(c, "prl")) / 9, 1), round((v(c, "anciennes") - v(c, "anciennes_prl")) / 9, 1), round(100 * v(c, "prl") / tot, 1) if tot else ""])

with open(OUT / "sensibilite_prl.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=["theme", "test", "mesure", "valeur", "lecture"], delimiter=";")
    w.writeheader()
    w.writerows(resultats)
print(f"Écrit : {OUT / 'sensibilite_prl.csv'} ({len(resultats)} lignes)")
