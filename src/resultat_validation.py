"""Calcule le taux de confirmation à partir des lectures de photos.

Usage :
    python src/resultat_validation.py [dossier_reponses]

Lit data/validation/reponses/*.csv (exportés par lecture.html), cle_codes.csv, echantillon_retournements.csv et poids_strates.csv.
Écrit data/validation/resultat_validation.csv (agrégats seulement, sans localisation). La règle est fixée avant lecture, voir LISEZ-MOI.md :
  - sur les points lus par plusieurs lecteurs, la réponse retenue est la majorité ; une égalité donne « Incertain » ;
  - Confirmé = « Culture » sur la photo d'après. Confirmé strict = « Herbe » avant et « Culture » après ;
  - un point « Incertain » est retiré du calcul principal, et compté comme non confirmé dans la variante prudente ;
  - dans chaque strate (département × ancienneté), le taux est pondéré par la surface des parcelles lues. Les strates sont
    ensuite combinées selon leur surface réelle (poids_strates.csv). L'intervalle à 95 % vient d'un bootstrap par strate.
"""
import csv
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parent.parent
VAL = RACINE / "data" / "validation"
REPONSES = Path(sys.argv[1]) if len(sys.argv) > 1 else VAL / "reponses"
N_BOOT = 5000
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
resultats = []


def note(mesure, valeur, lecture=""):
    resultats.append({"mesure": mesure, "valeur": valeur, "lecture": lecture})
    print(f"{mesure} : {valeur}{' | ' + lecture if lecture else ''}")


cle = {r["code"]: r["num"] for r in csv.DictReader(open(VAL / "cle_codes.csv", encoding="utf-8"), delimiter=";")}
ech = {r["num"]: r for r in csv.DictReader(open(VAL / "echantillon_retournements.csv", encoding="utf-8"), delimiter=";")}
poids = {(r["dep"], r["strate"]): float(r["ha_lcp_1ha_et_plus"]) for r in csv.DictReader(open(VAL / "poids_strates.csv", encoding="utf-8"), delimiter=";")}
tout = sum(float(r["ha_toutes_lcp"]) for r in csv.DictReader(open(VAL / "poids_strates.csv", encoding="utf-8"), delimiter=";"))

lectures = defaultdict(dict)
for chemin in sorted(REPONSES.glob("*.csv")):
    for r in csv.DictReader(open(chemin, encoding="utf-8-sig"), delimiter=";"):
        if r["avant"] and r["apres"]:
            lectures[r["code"]][r["lecteur"]] = r
if not lectures:
    sys.exit(f"Aucune réponse dans {REPONSES}.")


def majorite(valeurs):
    (v1, n1), *reste = Counter(valeurs).most_common()
    return "Incertain" if reste and reste[0][1] == n1 else v1


def kappa(paires):
    """Kappa de Cohen entre deux séries de réponses."""
    obs = sum(a == b for a, b in paires) / len(paires)
    ca, cb = Counter(a for a, _ in paires), Counter(b for _, b in paires)
    att = sum(ca[k] * cb[k] for k in ca) / len(paires) ** 2
    return None if att == 1 else (obs - att) / (1 - att)


lecteurs = sorted({l for r in lectures.values() for l in r})
note("lecteurs", len(lecteurs))
note("points lus", f"{len(lectures)} / {len(ech)}")
for q in ("avant", "apres"):
    valeurs = []
    for a, b in combinations(lecteurs, 2):
        paires = [(r[a][q], r[b][q]) for r in lectures.values() if a in r and b in r]
        if len(paires) >= 10:
            valeurs.append((kappa(paires), len(paires), sum(x == y for x, y in paires) / len(paires)))
    if valeurs:
        k = [v[0] for v in valeurs if v[0] is not None]
        note(f"accord entre lecteurs, photo {q}", f"{100 * np.mean([v[2] for v in valeurs]):.0f} % de réponses identiques, kappa {np.mean(k):.2f}" if k else "kappa non calculable",
             f"{valeurs[0][1]} points communs")

points = []
for code, r in lectures.items():
    e = ech[cle[code]]
    points.append({"type": e["type"], "dep": e["dep"], "strate": e["strate"], "ha": float(e["ha"]),
                   "avant": majorite([x["avant"] for x in r.values()]), "apres": majorite([x["apres"] for x in r.values()])})
pos = [p for p in points if p["type"] == "retournement détecté"]
tem = [p for p in points if p["type"] == "prairie maintenue"]
note("retournements : réponses sur la photo d'après", dict(Counter(p["apres"] for p in pos)))
note("témoins : réponses sur la photo d'après", dict(Counter(p["apres"] for p in tem)))


def taux(pts, succes, retirer):
    """Taux pondéré en surface, combiné entre strates, avec intervalle à 95 %."""
    rng = np.random.default_rng(2026)
    gardes = [p for p in pts if not retirer(p)]
    strates = defaultdict(list)
    for p in gardes:
        strates[(p["dep"], p["strate"])].append((p["ha"], 1.0 if succes(p) else 0.0))
    if not strates:
        return None
    vides = [s for s in poids if s not in strates and poids[s] > 0 and s[1] in {p["strate"] for p in pts}]
    if vides:
        print(f"  attention : strates sans aucun point lu, leur poids est reporté sur les autres : {vides}")
    tot = sum(poids.get(s, 0) for s in strates)
    w = {s: poids.get(s, 0) / tot for s in strates}
    arr = {s: np.array(v) for s, v in strates.items()}
    estim = sum(w[s] * np.average(a[:, 1], weights=a[:, 0]) for s, a in arr.items())
    boot = np.zeros(N_BOOT)
    for s, a in arr.items():
        idx = rng.integers(0, len(a), (N_BOOT, len(a)))
        boot += w[s] * (a[idx, 1] * a[idx, 0]).sum(axis=1) / a[idx, 0].sum(axis=1)
    b, h = np.percentile(boot, [2.5, 97.5])
    return f"{100 * estim:.0f} % (IC 95 % : {100 * b:.0f} à {100 * h:.0f} %), {len(gardes)} points"


culture = lambda p: p["apres"] == "Culture"
strict = lambda p: p["avant"] == "Herbe" and p["apres"] == "Culture"
incertain = lambda p: p["apres"] == "Incertain"
incertain_strict = lambda p: "Incertain" in (p["avant"], p["apres"])
jamais = lambda p: False
note("CONFIRMÉ : culture sur la photo d'après", taux(pos, culture, incertain), "résultat principal")
note("confirmé, incertains comptés comme non confirmés", taux(pos, culture, jamais), "variante prudente")
note("confirmé strict : herbe avant et culture après", taux(pos, strict, incertain_strict))
for s in ("ancienne", "récente"):
    note(f"confirmé, prairies {s}s", taux([p for p in pos if p["strate"] == s], culture, incertain))
n_t = [p for p in tem if p["apres"] != "Incertain"]
if n_t:
    fa = sum(p["apres"] == "Culture" for p in n_t)
    note("témoins lus en culture (fausses alertes)", f"{fa} / {len(n_t)}", "si ce nombre est élevé, la lecture elle-même est en cause")
note("couverture : part de la surface des retournements 2021-2023 sur des parcelles d'au moins 1 ha", f"{100 * sum(poids.values()) / tout:.0f} %",
     "le résultat ne vaut que pour cette part")

SORTIE = REPONSES.parent / "resultat_validation.csv"
with open(SORTIE, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["mesure", "valeur", "lecture"], delimiter=";")
    w.writeheader()
    w.writerows(resultats)
print(f"Écrit : {SORTIE}")
