"""Tests de sensibilité des choix méthodologiques (voir docs/registre_choix_methodologiques.md).

Usage :
    python src/sensibilite.py

À lancer après pipeline.py. Lit data/processed/ et data/raw/, n'écrit rien d'autre que son rapport à l'écran
et data/processed/sensibilite.csv (une ligne par test). Chaque test fait varier UN choix et mesure l'effet
sur ce que l'outil affiche : totaux, classements d'EPCI (corrélation de Spearman), profils, friches « gain rapide »
(indice de Jaccard entre l'ensemble de référence et l'ensemble obtenu).
"""
import csv
import sys
from pathlib import Path

import duckdb
import numpy as np
import rasterio

from definitions import GRP_PP

RACINE = Path(__file__).resolve().parent.parent
RAW, OUT = RACINE / "data" / "raw", RACINE / "data" / "processed"
DEPS = ["14", "27", "50", "61", "76"]
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute(f"CREATE TABLE t AS SELECT * FROM read_csv_auto('{OUT / 'tableau_regional_epci.csv'}', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")
resultats = []


def note(theme, test, mesure, valeur, lecture):
    resultats.append({"theme": theme, "test": test, "mesure": mesure, "valeur": valeur, "lecture": lecture})
    print(f"[{theme}] {test} | {mesure} = {valeur} | {lecture}")


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


# 1. Classement des EPCI selon la définition des pertes de prairies
cmp = con.execute("""SELECT perte_pct_stock_an, 100 * prairies_perdues_haute_ha_an / stock_pp_2015,
                            100 * (beton_sur_pp_ha_an + charrue_anciennes_fenetre_ha_an) / stock_pp_2015,
                            100 * (beton_sur_pp_ha_an + charrue_toutes_ha_an) / stock_pp_2015,
                            part_beton_pct, part_beton_haute_pct
                     FROM t WHERE NOT exclu_comparaisons""").fetchnumpy()
v = [np.asarray(x, float) for x in cmp.values()]
note("Classement EPCI", "perte de prairies : borne basse vs borne haute (avec prairies hors PAC)", "Spearman", spearman(v[0], v[1]), "")
note("Classement EPCI", "perte de prairies : toutes PP vs prairies anciennes seulement", "Spearman", spearman(v[0], v[2]), "")
note("Classement EPCI", "perte de prairies : fenêtre OCS GE vs moyenne 2015-2024", "Spearman", spearman(v[0], v[3]), "")
note("Classement EPCI", "part du béton : borne basse vs borne haute", "Spearman", spearman(v[4], v[5]), "")

# 2. Seuils des profils
base = con.execute("SELECT epci_code, densite_2022, part_pp_territoire_pct, profil FROM t ORDER BY epci_code").fetchall()


def profil(dens, pp, su, sp, sh):
    return "urbain" if dens >= su else "périurbain" if dens >= sp else "rural herbager" if pp >= sh else "rural de grandes cultures"


for su, sp, sh in [(300, 100, 15), (300, 100, 25), (300, 100, 30), (250, 100, 20), (400, 100, 20), (300, 80, 20), (300, 150, 20)]:
    n = sum(profil(r[1], r[2], su, sp, sh) != r[3] for r in base)
    note("Profils", f"seuils urbain {su} / périurbain {sp} hab/km², herbager {sh} % (réf. 300 / 100 / 20)",
         "EPCI changeant de profil", f"{n} / {len(base)}", "")

# 3. Friches : seuils de classe et rayon des prairies
f = con.execute(f"""SELECT gid, dist_reservoir_m, part_humide_pct, part_prairies_500m_pct, surface_ha, contexte_urbain,
                          potentiel_epfn_renaturation, projet_engage, classe FROM read_csv_auto('{OUT / 'friches.csv'}', delim=';', header=true)
                   ORDER BY gid""").fetchall()
gid = np.array([r[0] for r in f])
ref_gain = set(gid[[r[8] == "gain rapide" for r in f]])


def centile(x):
    x = np.asarray(x, float)
    o = x.argsort(kind="mergesort")
    rg = np.empty(len(x))
    rg[o] = np.arange(len(x))
    for val in np.unique(x):
        rg[x == val] = rg[x == val].mean()
    return 100 * rg / (len(x) - 1)


def gains(prairies, surface_min=0.1, cent=0.75, poids=(0.35, 0.20, 0.30, 0.15)):
    C = np.column_stack([centile([-r[1] for r in f]), centile([r[2] for r in f]), centile(prairies),
                         centile([np.log1p(r[4] * 1e4) for r in f])])
    pot = C @ np.array(poids)
    faisa = np.array([r[6] for r in f], float)
    eng = np.array([bool(r[7]) for r in f])
    elig = ~eng & ~np.array([r[4] < surface_min for r in f])
    s, m = np.quantile(pot[elig], cent), np.median(faisa[elig])
    return set(gid[elig & (pot >= s) & (faisa >= m)])


def jaccard(a, b):
    return round(len(a & b) / len(a | b), 3) if a | b else 1.0


prairies500 = [r[3] for r in f]
recalc = gains(prairies500)
variantes = [recalc]  # ensembles « gain rapide » des variantes de réglage (même objectif biodiversité)
note("Friches", "recalcul de référence (contrôle)", "Jaccard avec friches.csv", jaccard(recalc, ref_gain), "doit valoir 1")
for cent in (0.70, 0.80):
    g = gains(prairies500, cent=cent)
    variantes.append(g)
    note("Friches", f"seuil de potentiel au {int(cent * 100)}e centile (réf. 75e)", "gains rapides / Jaccard",
         f"{len(g)} / {jaccard(g, recalc)}", f"réf. {len(recalc)}")
for smin in (0.05, 0.5):
    g = gains(prairies500, surface_min=smin)
    note("Friches", f"surface minimale {smin} ha (réf. 0,1)", "gains rapides / Jaccard", f"{len(g)} / {jaccard(g, recalc)}", "")
for nom, w in {"poids égaux": (0.25, 0.25, 0.25, 0.25), "préréglage eau": (0.15, 0.60, 0.10, 0.15)}.items():
    g = gains(prairies500, poids=w)
    note("Friches", f"pondération {nom} (réf. biodiversité)", "gains rapides / Jaccard", f"{len(g)} / {jaccard(g, recalc)}", "")

# Rayon des prairies : recalcul de la part de prairies permanentes 2024 à 300 m et 1 000 m
con.execute(f"CREATE TABLE fg AS SELECT gid, ST_MakeValid(geom) AS geom, surface / 1e4 AS ha FROM ST_Read('{RAW / 'friches' / 'friches_epfn.geojson'}')")
con.execute("CREATE TABLE pp (pt GEOMETRY, ha DOUBLE)")
for d in DEPS:
    con.execute(f"""INSERT INTO pp SELECT ST_PointOnSurface(l.wkb_geometry), l.area_lcp
        FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{d}.gpkg'}') l
        JOIN read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true) r ON r.crop = l.crop24
        WHERE CAST(r.grp AS INTEGER) = {GRP_PP}""")
for rayon in (300, 1000):
    part = dict(con.execute(f"""
        SELECT fg.gid, 100 * least(coalesce(sum(pp.ha), 0) / nullif(ST_Area(ST_Buffer(any_value(fg.geom), {rayon})) / 1e4 - any_value(fg.ha), 0), 1)
        FROM fg LEFT JOIN pp ON ST_DWithin(pp.pt, fg.geom, {rayon}) GROUP BY fg.gid""").fetchall())
    g = gains([part.get(int(x), 0) or 0 for x in gid])
    variantes.append(g)
    note("Friches", f"rayon des prairies {rayon} m (réf. 500 m)", "gains rapides / Jaccard", f"{len(g)} / {jaccard(g, recalc)}", "")
variantes.append(gains(prairies500, poids=(0.25, 0.25, 0.25, 0.25)))
noyau = set.intersection(*variantes)
note("Friches", "noyau stable : gain rapide dans toutes les variantes (seuil 70/75/80e, rayon 300/500/1 000 m, poids égaux)",
     "friches du noyau", f"{len(noyau)} / {len(recalc)}",
     f"{sum(r[4] for r in f if r[0] in noyau):.0f} ha sur {sum(r[4] for r in f if r[0] in recalc):.0f} ha")

# 4. Milieux potentiellement humides : poids de chaque classe de confiance dans le béton « humide »
pts = []
with open(RAW / "ocsge_artif" / "fenetres.csv", encoding="utf-8") as fo:
    fenetres = [(x["dep"], x) for x in csv.DictReader(fo, delimiter=";")]
for d, fen in fenetres:
    pts += con.execute(f"""SELECT ST_X(ST_PointOnSurface(geom)), ST_Y(ST_PointOnSurface(geom)), ST_Area(geom) / 1e4
                           FROM ST_Read('{RACINE / fen['couche']}') WHERE artificialisation = 1""").fetchall()
with rasterio.open(RAW / "mph" / "mph_normandie.tif") as r:
    cl = np.array([v[0] for v in r.sample([(x, y) for x, y, _ in pts])])
ha = np.array([p[2] for p in pts])
tot = ha[(cl >= 1) & (cl <= 3)].sum()
for k in (1, 2, 3):
    note("Zones humides", f"béton en milieu potentiellement humide, classe {k} (point intérieur)", "part du béton humide",
         f"{100 * ha[cl == k].sum() / tot:.0f} %", "classes 1 à 3 retenues ; 3 = probabilité la plus forte")

with open(OUT / "sensibilite.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=["theme", "test", "mesure", "valeur", "lecture"], delimiter=";")
    w.writeheader()
    w.writerows(resultats)
print(f"Écrit : {OUT / 'sensibilite.csv'} ({len(resultats)} tests)")
