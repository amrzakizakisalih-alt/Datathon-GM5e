"""Compare le bootstrap de trajectoires.py à un modèle hiérarchique bayésien, sur les mêmes épreuves.

Usage :
    python src/validation_glmm.py

À lancer après cohorte_epci.py et trajectoires.py. N'écrit que data/processed/glmm_validation.csv : aucune trajectoire n'est modifiée.

Modèle, pour l'EPCI e et l'année y, sur la cohorte de cohorte_epci.py :
    y_ey = L_ey n_ey / S_ey ~ Binomiale(n_ey, p_ey)      n_ey = S_ey² / Σ a_i², nombre de parcelles équivalent
    logit p_ey = β_p(e) + u_e + v_y + ε_ey
    u_e ~ N(0, σ_u²)    v_y ~ N(0, σ_v²)    ε_ey ~ N(0, σ_ε²)    β_p ~ N(-4,7 ; 2²)    σ ~ demi-normale(0, s)
ε_ey absorbe ce que la binomiale ne voit pas : les morceaux d'une parcelle et d'une exploitation sont décidés ensemble.
Échantillonneur de Gibbs écrit à la main, en numpy : (β, u, v) | η en un seul bloc gaussien, η_ey | reste par Metropolis indépendant
autour du mode (cellule par cellule), σ | reste exactement sur une grille. 4 chaînes, convergence contrôlée par le R-hat.
Prédictive d'un EPCI : tirages a posteriori de (β, u, σ), nouveaux v* et ε* pour chaque année future, puis bruit binomial. Les autres
sorties restent le taux moyen de l'EPCI, comme dans les épreuves de trajectoires.py.

Mesures, pour 90 % : couverture, score d'intervalle de Winkler et CRPS (deux règles propres, normalisées par le labour observé).
Règle fixée avant de lire les résultats : le modèle hiérarchique remplacerait le bootstrap s'il a un score d'intervalle et un CRPS plus
faibles sur au moins 2 épreuves sur 3, sans couverture plus éloignée de 90 % que le bootstrap élargi. Les épreuves se recouvrent et les
EPCI sont dépendants : un écart de quelques points n'est pas significatif.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parent.parent
PROC = RACINE / "data" / "processed"
ANNEES = list(range(2016, 2025))
CALIBRATION = (2017, 2024)
ORIGINES = (2019, 2020, 2021)
HORIZON = 11
N, CHAINES, ITER, CHAUFFE, PAS = 4000, 4, 4000, 1000, 3
B0, TAU = -4.7, 2.0
GRILLE = np.exp(np.linspace(np.log(0.01), np.log(4), 500))
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
rng = np.random.default_rng(2026)

epci = {r["epci_code"]: r for r in csv.DictReader(open(PROC / "tableau_regional_epci.csv", encoding="utf-8"), delimiter=";")}
codes = sorted(epci)
E, Y = len(codes), len(ANNEES)
pos_e, pos_a = {c: i for i, c in enumerate(codes)}, {a: i for i, a in enumerate(ANNEES)}
profils = np.array([epci[c]["profil"] for c in codes])
noms_p = sorted(set(profils))
idx_p = np.array([noms_p.index(p) for p in profils])
A = defaultdict(lambda: np.zeros((E, Y)))
for r in csv.DictReader(open(PROC / "cohorte_epci.csv", encoding="utf-8"), delimiter=";"):
    for k, v in r.items():
        if k not in ("epci_code", "annee"):
            A[k][pos_e[r["epci_code"]], pos_a[int(r["annee"])]] = float(v)
with np.errstate(divide="ignore", invalid="ignore"):
    H = np.nan_to_num(A["vers_culture"] / A["stock_debut"])
    X = np.nan_to_num((A["stock_debut"] - A["vers_culture"] - A["stock_fin"]) / A["stock_debut"])
X[:, pos_a[2023]] = X[:, [pos_a[a] for a in ANNEES if a != 2023 and a >= CALIBRATION[0]]].mean(axis=1)
resultats = []


def note(theme, test, mesure, valeur, lecture=""):
    resultats.append({"theme": theme, "test": test, "mesure": mesure, "valeur": valeur, "lecture": lecture})
    print(f"[{theme}] {test} | {mesure} = {valeur}{' | ' + lecture if lecture else ''}")


def expit(z):
    return 1 / (1 + np.exp(-z))


# ---------- La méthode actuelle, identique à trajectoires.py ----------
def retrecir(C, S, annuels):
    propre = np.nan_to_num(C / np.maximum(S, 1))
    profil = np.array([C[profils == g].sum() / max(S[profils == g].sum(), 1) for g in profils])
    v = annuels.var(axis=1, ddof=1) / annuels.shape[1]
    v = np.where(v > 0, v, np.median(v))
    tau2 = max(np.var(propre - profil, ddof=1) - np.median(v), 1e-9)
    poids = tau2 / (tau2 + v)
    r = poids * propre + (1 - poids) * profil
    return propre, r * (S * propre).sum() / (S * r).sum()


def bootstrap(app, depart, x, pas):
    C, S = A["vers_culture"][:, app].sum(axis=1), A["stock_debut"][:, app].sum(axis=1)
    propre, r = retrecir(C, S, H[:, app])
    with np.errstate(divide="ignore", invalid="ignore"):
        h = np.where(propre[:, None] > 0, H[:, app] * (r / propre)[:, None], r[:, None])
    base = rng.integers(0, len(app), (N, len(app)))
    idx = np.take_along_axis(base, rng.integers(0, len(app), (N, pas)), axis=1)
    St, total = np.tile(depart, (N, 1)), np.zeros((N, E))
    for t in range(pas):
        labour = St * h[:, idx[:, t]].T
        St = St - labour - St * x
        total += labour
    return total


# ---------- Le modèle hiérarchique ----------
def tirer_sigma(somme, nb, s, g):
    logp = -nb * np.log(GRILLE) - somme / (2 * GRILLE ** 2) - GRILLE ** 2 / (2 * s ** 2) + np.log(GRILLE)
    p = np.exp(logp - logp.max())
    return GRILLE[np.searchsorted(np.cumsum(p), g.random() * p.sum())]


def maj_eta(eta, mu, y, n, s, g):
    pr = 1 / s ** 2
    m = eta.copy()
    for _ in range(3):
        p = expit(m)
        m += np.clip((y - n * p - (m - mu) * pr) / (n * p * (1 - p) + pr), -2, 2)
    p = expit(m)
    q = 1.2 / np.sqrt(n * p * (1 - p) + pr)
    prop = m + q * g.standard_normal(len(m))
    cible = lambda z: y * z - n * np.log1p(np.exp(z)) - 0.5 * pr * (z - mu) ** 2
    instrument = lambda z: -0.5 * ((z - m) / q) ** 2
    acc = np.log(g.random(len(m))) < cible(prop) - cible(eta) + instrument(eta) - instrument(prop)
    return np.where(acc, prop, eta), acc.mean()


def rhat(c):
    """R-hat par paramètre ; c : chaînes × tirages × paramètres."""
    n = c.shape[1]
    w = c.var(axis=1, ddof=1).mean(axis=0)
    b = n * c.mean(axis=1).var(axis=0, ddof=1)
    return np.sqrt(((n - 1) / n * w + b / n) / np.maximum(w, 1e-12))


def ajuster(app, s_v):
    Sa, La, Sa2 = A["stock_debut"][:, app], A["vers_culture"][:, app], A["stock_ha2"][:, app]
    e, a = np.nonzero(Sa > 0)
    n = Sa[e, a] ** 2 / Sa2[e, a]
    y = La[e, a] * n / Sa[e, a]
    P, nb_a, M = len(noms_p), len(app), len(e)
    dim = P + E + nb_a
    Z = np.zeros((M, dim))
    Z[np.arange(M), idx_p[e]] = Z[np.arange(M), P + e] = Z[np.arange(M), P + E + a] = 1
    ZtZ = Z.T @ Z
    gam, sig, taux_acc = [], [], []
    for ch in range(CHAINES):
        g = np.random.default_rng(1000 + ch)
        eta = np.log((y + .5) / (n - y + .5)) + g.normal(0, .1, M)
        s_e, s_u, s_y = g.uniform(.2, .8, 3)
        gc, sc = [], []
        for it in range(ITER):
            Q = ZtZ / s_e ** 2
            Q[np.diag_indices(dim)] += np.r_[np.full(P, 1 / TAU ** 2), np.full(E, 1 / s_u ** 2), np.full(nb_a, 1 / s_y ** 2)]
            b = Z.T @ eta / s_e ** 2
            b[:P] += B0 / TAU ** 2
            L = np.linalg.cholesky(Q)
            gamma = np.linalg.solve(L.T, np.linalg.solve(L, b) + g.standard_normal(dim))
            mu = Z @ gamma
            eta, acc = maj_eta(eta, mu, y, n, s_e, g)
            s_e = tirer_sigma(((eta - mu) ** 2).sum(), M, 1.0, g)
            s_u = tirer_sigma((gamma[P:P + E] ** 2).sum(), E, 1.0, g)
            s_y = tirer_sigma((gamma[P + E:] ** 2).sum(), nb_a, s_v, g)
            if it >= CHAUFFE and (it - CHAUFFE) % PAS == 0:
                gc.append(gamma)
                sc.append((s_u, s_y, s_e))
                taux_acc.append(acc)
        gam.append(gc)
        sig.append(sc)
    gam, sig = np.array(gam), np.array(sig)
    return {"beta": gam[:, :, :P].reshape(-1, P), "u": gam[:, :, P:P + E].reshape(-1, E), "v": gam[:, :, P + E:].reshape(-1, nb_a), "sig": sig.reshape(-1, 3),
            "rhat": float(max(rhat(gam).max(), rhat(sig).max())), "acc": float(np.mean(taux_acc))}


def predire(fit, depart, x, phi, pas):
    D = len(fit["beta"])
    St, total = np.tile(depart, (D, 1)), np.zeros((D, E))
    su, sv, se = fit["sig"].T
    for _ in range(pas):
        eta = fit["beta"][:, idx_p] + fit["u"] + rng.normal(0, sv)[:, None] + rng.normal(0, 1, (D, E)) * se[:, None]
        n = np.maximum(np.round(St / np.maximum(phi, .01)), 1)
        labour = rng.binomial(n.astype(np.int64), expit(eta)) * St / n
        St = St - labour - St * x
        total += labour
    return total


# ---------- Mesures ----------
def elargir(ech, k):
    med = np.median(ech, axis=0)
    return np.maximum(med + k * (ech - med), 0)


def ecart_normalise(ech, obs):
    bas, med, haut = np.percentile(ech, [5, 50, 95], axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.nan_to_num(np.where(obs >= med, (obs - med) / (haut - med), (med - obs) / (med - bas)), nan=0, posinf=10)


def crps(ech, o):
    n = len(ech)
    return np.abs(ech - o).mean(axis=0) - np.sort(ech, axis=0).T @ (2 * np.arange(1, n + 1) - n - 1) / n ** 2


def scores(ech, obs):
    bas, med, haut = np.percentile(ech, [5, 50, 95], axis=0)
    ok = obs > 0
    winkler = (haut - bas) + 20 * np.maximum(bas - obs, 0) + 20 * np.maximum(obs - haut, 0)
    reg = ech.sum(axis=1)
    rb, rm, rh = np.percentile(reg, [5, 50, 95])
    return {"biais": 100 * (rm / obs.sum() - 1), "wape": 100 * np.abs(med - obs).sum() / obs.sum(), "mdape": 100 * np.median(np.abs(med[ok] - obs[ok]) / obs[ok]), "couv": 100 * ((obs >= bas) & (obs <= haut)).mean(),
            "largeur": float(np.median((haut[ok] - bas[ok]) / np.maximum(med[ok], 1))), "winkler": float(winkler.sum() / obs.sum()), "crps": 100 * float(crps(ech, obs).sum() / obs.sum()),
            "reg": (rb, rm, rh), "reg_dedans": bool(rb <= obs.sum() <= rh), "reg_crps": 100 * float(crps(reg[:, None], np.array([obs.sum()]))[0] / obs.sum())}


echantillons = defaultdict(dict)
obs_par_origine, ajustements = {}, {}
for fin in ORIGINES:
    app = [pos_a[a] for a in ANNEES if CALIBRATION[0] <= a <= fin]
    test = [pos_a[a] for a in ANNEES if a > fin]
    depart, pas = A["stock_debut"][:, test[0]], len(test)
    x = X[:, app].mean(axis=1)
    phi = A["stock_ha2"][:, app[-1]] / np.maximum(A["stock_debut"][:, app[-1]], 1)
    obs_par_origine[fin] = A["vers_culture"][:, test].sum(axis=1)
    echantillons["bootstrap"][fin] = bootstrap(app, depart, x, pas)
    for lib, s_v in (("GLMM", 1.0), ("GLMM, a priori σ_v plus serré", 0.5)):
        fit = ajuster(app, s_v)
        echantillons[lib][fin] = predire(fit, depart, x, phi, pas)
        q = np.percentile(fit["sig"], [5, 50, 95], axis=0).round(2)
        note("Convergence", f"origine {fin}, {lib}", "R-hat maximal / acceptation de η", f"{fit['rhat']:.3f} / {100 * fit['acc']:.0f} %", "R-hat < 1,05 attendu")
        note("A posteriori", f"origine {fin}, {lib}", "médianes σ_u / σ_v / σ_ε (5e-95e)", f"{q[1, 0]} ({q[0, 0]}-{q[2, 0]}) / {q[1, 1]} ({q[0, 1]}-{q[2, 1]}) / {q[1, 2]} ({q[0, 2]}-{q[2, 2]})")

# Facteur d'élargissement de chaque méthode, appris sans l'épreuve évaluée
for lib in list(echantillons):
    ec = {f: ecart_normalise(echantillons[lib][f], obs_par_origine[f]) for f in ORIGINES}
    for f in ORIGINES:
        k = float(np.quantile(np.concatenate([ec[g] for g in ORIGINES if g != f]), 0.9))
        echantillons[f"{lib}, élargi"][f] = elargir(echantillons[lib][f], k)
        note("Facteur K", f"{lib}, évaluation sur l'origine {f}", "K appris sur les deux autres", round(k, 2))

tab = defaultdict(dict)
for lib in echantillons:
    for f in ORIGINES:
        s = tab[lib][f] = scores(echantillons[lib][f], obs_par_origine[f])
        note("Épreuve", f"origine {f} : {lib}", "biais région / WAPE / MdAPE / couverture 90 % / largeur relative / score d'intervalle / CRPS",
             f"{s['biais']:+.1f} % / {s['wape']:.0f} % / {s['mdape']:.0f} % / {s['couv']:.0f} % / {s['largeur']:.2f} / {s['winkler']:.2f} / {s['crps']:.1f}")
        note("Épreuve région", f"origine {f} : {lib}", "observé / fourchette / dedans / CRPS", f"{obs_par_origine[f].sum():,.0f} / {s['reg'][0]:,.0f} à {s['reg'][2]:,.0f} / {'oui' if s['reg_dedans'] else 'non'} / {s['reg_crps']:.1f}")

ref = "bootstrap, élargi"
for lib in ("GLMM", "GLMM, élargi", "GLMM, a priori σ_v plus serré", "GLMM, a priori σ_v plus serré, élargi"):
    gagne = sum(tab[lib][f]["winkler"] < tab[ref][f]["winkler"] and tab[lib][f]["crps"] < tab[ref][f]["crps"] for f in ORIGINES)
    moy = lambda l, c: np.mean([tab[l][f][c] for f in ORIGINES])
    ecart_c = np.mean([abs(tab[lib][f]["couv"] - 90) for f in ORIGINES])
    ecart_r = np.mean([abs(tab[ref][f]["couv"] - 90) for f in ORIGINES])
    note("Décision", f"{lib} contre {ref}", "épreuves gagnées (score d'intervalle et CRPS) / écart moyen de couverture à 90 % / score d'intervalle moyen / CRPS moyen",
         f"{gagne} sur 3 / {ecart_c:.1f} contre {ecart_r:.1f} / {moy(lib, 'winkler'):.2f} contre {moy(ref, 'winkler'):.2f} / {moy(lib, 'crps'):.1f} contre {moy(ref, 'crps'):.1f}",
         "remplacement si 2 sur 3 au moins, sans couverture plus éloignée")

# Projection à 2035 sur toute la calibration, pour voir ce qui changerait
cal = [pos_a[a] for a in ANNEES if CALIBRATION[0] <= a <= CALIBRATION[1]]
fit = ajuster(cal, 1.0)
note("Convergence", "calibration 2017-2024, GLMM", "R-hat maximal / acceptation de η", f"{fit['rhat']:.3f} / {100 * fit['acc']:.0f} %")
q = np.percentile(fit["sig"], [5, 50, 95], axis=0).round(2)
note("A posteriori", "calibration 2017-2024", "médianes σ_u / σ_v / σ_ε (5e-95e)", f"{q[1, 0]} ({q[0, 0]}-{q[2, 0]}) / {q[1, 1]} ({q[0, 1]}-{q[2, 1]}) / {q[1, 2]} ({q[0, 2]}-{q[2, 2]})")
S0 = A["stock_fin"][:, -1]
phi = A["stock_ha2"][:, -1] / np.maximum(A["stock_debut"][:, -1], 1)
xc = X[:, cal].mean(axis=1)
pg = predire(fit, S0, xc, phi, HORIZON)
actuel = {r["epci_code"]: r for r in csv.DictReader(open(PROC / "trajectoires_epci.csv", encoding="utf-8"), delimiter=";")}
reg = np.percentile(pg.sum(axis=1), [5, 50, 95])
n_ = actuel["normandie"]
note("Projection 2035", "labour cumulé en Normandie", "GLMM / méthode actuelle", f"{reg[1]:,.0f} ({reg[0]:,.0f} à {reg[2]:,.0f}) / {float(n_['t1_2035_ha']):,.0f} ({float(n_['t1_2035_bas']):,.0f} à {float(n_['t1_2035_haut']):,.0f})")
bas, med, haut = np.percentile(pg, [5, 50, 95], axis=0)
acm = np.array([float(actuel[c]["t1_2035_ha"]) for c in codes])
rang = lambda v: v.argsort().argsort()
note("Projection 2035", "médianes des EPCI, GLMM contre méthode actuelle", "Spearman / rapport médian / plus grand écart relatif", f"{np.corrcoef(rang(med), rang(acm))[0, 1]:.3f} / {np.median(med / np.maximum(acm, 1)):.2f} / {np.max(np.abs(med - acm) / np.maximum(acm, 1)):.2f}")
fragile = np.array([actuel[c]["fiabilite"] == "fragile" for c in codes])
ec = np.abs(med - acm) / np.maximum(acm, 1)
note("Projection 2035", "écart relatif des médianes EPCI", "plus grand, tous EPCI / plus grand et médian, hors EPCI fragiles", f"{ec.max():.2f} ({epci[codes[int(ec.argmax())]]['epci_nom']}) / {ec[~fragile].max():.2f} et {np.median(ec[~fragile]):.2f}")
lg = (haut - bas) / np.maximum(med, 1)
acl = np.array([(float(actuel[c]["t1_2035_haut"]) - float(actuel[c]["t1_2035_bas"])) / max(float(actuel[c]["t1_2035_ha"]), 1) for c in codes])
note("Projection 2035", "largeur relative des fourchettes EPCI", "médiane GLMM brut / médiane actuelle / EPCI sous 1 pour le GLMM / pour l'actuelle", f"{np.median(lg):.2f} / {np.median(acl):.2f} / {int((lg <= 1).sum())} / {int((acl <= 1).sum())}")
with open(PROC / "glmm_validation.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=["theme", "test", "mesure", "valeur", "lecture"], delimiter=";")
    w.writeheader()
    w.writerows(resultats)
print(f"Écrit : {PROC / 'glmm_validation.csv'} ({len(resultats)} lignes)")
