"""Trois trajectoires par EPCI et pour la Normandie : prairies anciennes jusqu'en 2035, foncier jusqu'en 2031.

Usage :
    python src/trajectoires.py

À lancer après pipeline.py, sensibilite_prl.py et cohorte_epci.py. Écrit dans data/processed/ (agrégats seulement) :
  trajectoires_epci.csv        une ligne par EPCI et une ligne epci_code = normandie
  trajectoires_annuelles.csv   labour cumulé depuis 2025 : territoire, trajectoire, annee, bas (5e centile), median, haut (95e centile)
  trajectoires_validation.csv  épreuves sur le passé et tests de sensibilité (une ligne par mesure)
  trajectoires_parametres.json hypothèses utilisées, reprises par export_web.py

Ce sont des trajectoires conditionnelles, pas des prévisions : « si tel comportement se poursuit, voici le résultat ».

Prairies anciennes (cohorte de cohorte_epci.py, prairie permanente chaque année depuis 2015) :
  T1 on laisse faire    chaque année future ressemble à une année observée de CALIBRATION. C'est la seule vraie projection.
  T2 on protège le plus fragile   plus aucun labour dans ZONE_T2. L'effet se déduit de la part du labour qui y a eu lieu.
  T3 on vise un objectif    aucun territoire ne laboure plus de OBJECTIF_PERTE_2035 de sa cohorte de 2024 d'ici 2035 (exemple à
                        remplacer par l'objectif de la Région). Donne l'effort requis par territoire.
À chaque pas, le stock perd le labour et les autres sorties (prairie temporaire, non déclaré), qui ne sont pas comptées comme des
labours. Les autres sorties de 2023 viennent en partie de la refonte du RPG et sont remplacées par la moyenne des autres années.
Le rythme de chaque EPCI est rapproché de celui de son profil quand ses années sont irrégulières, sans changer le total régional :
les épreuves sur le passé montrent une erreur plus faible qu'avec son seul taux.
La fourchette (5e à 95e centile) tire les années futures avec remise, après un premier tirage de la période de calibration, pour
inclure l'incertitude sur le rythme moyen. Mêmes années tirées pour tous les EPCI : les bonnes et mauvaises années sont communes,
et le total normand est la somme des EPCI tirage par tirage. Pour les EPCI, la fourchette est élargie du facteur K qui aurait contenu
90 % des résultats réels des épreuves. Elle suppose malgré tout un avenir semblable au passé.

Foncier (CONSOENAF, base légale du ZAN ; enveloppe de référence nationale = moitié de 2011-2021) :
  F1 on laisse faire    les années à venir ressemblent aux flux annuels 2021-2024.
  F2 on densifie        au moins DENSITE_CIBLE logements par ha : réduit la part habitat de la consommation (exemple à confirmer).
  F3 on tient l'enveloppe   rythme requis du 1/1/2025 au 1/1/2031 et densité qui suffirait, à logements constants.
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import duckdb
import numpy as np

RACINE = Path(__file__).resolve().parent.parent
PROC, RAW = RACINE / "data" / "processed", RACINE / "data" / "raw"
DEPS = ["14", "27", "50", "61", "76"]
ANNEES = list(range(2016, 2025))
CALIBRATION = (2017, 2024)  # 2016 écartée : la cohorte de 2015 n'a qu'une année d'ancienneté
FUTUR = list(range(2025, 2036))
JALON = FUTUR.index(2031)
ZONE_T2 = "vers_culture_etendue"  # zones reconnues + milieux potentiellement humides (voir cohorte_epci.py)
OBJECTIF_PERTE_2035 = 0.05
DENSITE_CIBLE = 20
DENSITE_MAX = 100  # au-delà, la densité requise n'a plus de sens : densifier seul ne suffit pas
SEUIL_EXPLOITABLE, SEUIL_INDICATIF = 1.0, 2.0  # largeur de la fourchette T1 2035, rapportée au médian (1 = environ ± 50 %)
N = 4000
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
rng = np.random.default_rng(2026)

epci = {r["epci_code"]: r for r in csv.DictReader(open(PROC / "tableau_regional_epci.csv", encoding="utf-8"), delimiter=";")}
sobriete = {r["epci_code"]: r for r in csv.DictReader(open(PROC / "sobriete_epci.csv", encoding="utf-8"), delimiter=";")}
codes = sorted(epci)
E, Y = len(codes), len(ANNEES)
pos_e, pos_a = {c: i for i, c in enumerate(codes)}, {a: i for i, a in enumerate(ANNEES)}
profils = np.array([epci[c]["profil"] for c in codes])
A = defaultdict(lambda: np.zeros((E, Y)))
for r in csv.DictReader(open(PROC / "cohorte_epci.csv", encoding="utf-8"), delimiter=";"):
    for k, v in r.items():
        if k not in ("epci_code", "annee"):
            A[k][pos_e[r["epci_code"]], pos_a[int(r["annee"])]] = float(v)
with np.errstate(divide="ignore", invalid="ignore"):
    H = np.nan_to_num(A["vers_culture"] / A["stock_debut"])
    X = np.nan_to_num((A["stock_debut"] - A["vers_culture"] - A["stock_fin"]) / A["stock_debut"])
autres = [pos_a[a] for a in ANNEES if a != 2023 and a >= CALIBRATION[0]]
X[:, pos_a[2023]] = X[:, autres].mean(axis=1)
S0 = A["stock_fin"][:, -1]
resultats = []


def note(theme, test, mesure, valeur, lecture=""):
    resultats.append({"theme": theme, "test": test, "mesure": mesure, "valeur": valeur, "lecture": lecture})
    print(f"[{theme}] {test} | {mesure} = {valeur}{' | ' + lecture if lecture else ''}")


def tirages(n_annees, pas, deux_niveaux=True):
    """Indices d'années (tirages × pas). Le premier niveau retire la période de calibration, le second les années futures."""
    if not deux_niveaux:
        return rng.integers(0, n_annees, (N, pas))
    base = rng.integers(0, n_annees, (N, n_annees))
    return np.take_along_axis(base, rng.integers(0, n_annees, (N, pas)), axis=1)


def projeter(depart, h, x, idx):
    """Labour cumulé (tirages × EPCI × pas de temps)."""
    S = np.tile(depart, (len(idx), 1))
    total, cumul = np.zeros_like(S), np.zeros((len(idx), len(depart), idx.shape[1]))
    for t in range(idx.shape[1]):
        labour = S * h[:, idx[:, t]].T
        S = S - labour - S * x[:, idx[:, t]].T
        total += labour
        cumul[:, :, t] = total
    return cumul


def en_points(depart, r, x, pas):
    """Labour cumulé sur `pas` années avec des taux constants."""
    S, total = depart.copy(), np.zeros_like(depart)
    for _ in range(pas):
        total += S * r
        S = S - S * r - S * x
    return total


def taux_groupes(C, S, groupes):
    return np.array([C[groupes == g].sum() / max(S[groupes == g].sum(), 1) for g in groupes])


def retrecir(C, S, annuels):
    """Rapproche le taux d'un EPCI de celui de son profil, d'autant plus que ses années sont irrégulières. Le total régional ne change pas."""
    propre = np.nan_to_num(C / np.maximum(S, 1))
    profil = taux_groupes(C, S, profils)
    v = annuels.var(axis=1, ddof=1) / annuels.shape[1]
    v = np.where(v > 0, v, np.median(v))  # un EPCI sans aucun labour observé n'est pas pour autant un EPCI sûr
    tau2 = max(np.var(propre - profil, ddof=1) - np.median(v), 1e-9)
    poids = tau2 / (tau2 + v)
    r = poids * propre + (1 - poids) * profil
    return propre, profil, r, r * (S * propre).sum() / (S * r).sum()


def annuels_retrecis(annuels, propre, r):
    """Taux annuels ramenés au rythme r ; un EPCI sans labour observé reçoit r chaque année."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(propre[:, None] > 0, annuels * (r / propre)[:, None], r[:, None])


def epreuve(fin_app):
    """Apprend sur CALIBRATION[0]..fin_app, prédit le labour des années suivantes depuis le stock réel de départ.
    Renvoie, par EPCI, l'écart entre l'observé et le médian, rapporté à la demi-largeur de la fourchette du même côté."""
    app = [pos_a[a] for a in ANNEES if CALIBRATION[0] <= a <= fin_app]
    test = [pos_a[a] for a in ANNEES if a > fin_app]
    depart, obs, pas = A["stock_debut"][:, test[0]], A["vers_culture"][:, test].sum(axis=1), len(test)
    C, S = A["vers_culture"][:, app].sum(axis=1), A["stock_debut"][:, app].sum(axis=1)
    x = X[:, app].mean(axis=1)
    propre, profil, retreci, recale = retrecir(C, S, H[:, app])
    nom = f"apprend {CALIBRATION[0]}-{fin_app}, prédit {ANNEES[test[0]]}-2024"
    ok = obs > 0
    for lib, r in (("taux propre de l'EPCI", propre), ("taux du profil", profil), ("taux régional", np.full(E, C.sum() / S.sum())), ("taux rétréci vers le profil", retreci), ("taux rétréci, total régional conservé", recale)):
        p = en_points(depart, r, x, pas)
        note("Épreuve", f"{nom} : {lib}", "écart région / erreur absolue pondérée / erreur médiane EPCI",
             f"{100 * (p.sum() / obs.sum() - 1):+.1f} % / {100 * np.abs(p - obs).sum() / obs.sum():.0f} % / {100 * np.median(np.abs(p[ok] - obs[ok]) / obs[ok]):.0f} %")
    c = projeter(depart, annuels_retrecis(H[:, app], propre, recale), np.repeat(x[:, None], len(app), axis=1), tirages(len(app), pas))[:, :, -1]
    bas, med, haut = np.percentile(c, [5, 50, 95], axis=0)
    rb, rh = np.percentile(c.sum(axis=1), [5, 95])
    note("Épreuve", f"{nom} : fourchette à 90 % avant élargissement", "EPCI dans la fourchette / région dedans",
         f"{100 * ((obs >= bas) & (obs <= haut)).mean():.0f} % / {'oui' if rb <= obs.sum() <= rh else 'non'}", f"observé {obs.sum():,.0f} ha, fourchette {rb:,.0f} à {rh:,.0f}")
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.nan_to_num(np.where(obs >= med, (obs - med) / (haut - med), (med - obs) / (med - bas)), nan=0, posinf=10)


# Facteur d'élargissement des fourchettes par EPCI : celui qui aurait contenu 90 % des résultats réels. Il est aussi testé en
# l'apprenant sur deux épreuves pour le vérifier sur la troisième.
ECARTS = [epreuve(fin) for fin in (2019, 2020, 2021)]
K = float(np.quantile(np.concatenate(ECARTS), 0.9))
note("Fourchettes", "facteur d'élargissement des fourchettes EPCI", "K", round(K, 2), "1 = aucune correction")
for i in range(3):
    k = np.quantile(np.concatenate([e for j, e in enumerate(ECARTS) if j != i]), 0.9)
    note("Fourchettes", f"facteur appris sans l'épreuve {i + 1}, vérifié sur elle", "EPCI dans la fourchette élargie", f"{100 * (ECARTS[i] <= k).mean():.0f} %", "objectif 90 %")

# ---------- Prairies : les trois trajectoires ----------
cal = [pos_a[a] for a in ANNEES if CALIBRATION[0] <= a <= CALIBRATION[1]]
C_cal, S_cal = A["vers_culture"][:, cal].sum(axis=1), A["stock_debut"][:, cal].sum(axis=1)
taux_propre, _, _, taux = retrecir(C_cal, S_cal, H[:, cal])
h, x = annuels_retrecis(H[:, cal], taux_propre, taux), X[:, cal]
x_moy = x.mean(axis=1)
part_t2 = np.nan_to_num(A[ZONE_T2][:, cal].sum(axis=1) / np.maximum(C_cal, 1))
part_prl = np.nan_to_num(A["vers_culture_prl"][:, cal].sum(axis=1) / np.maximum(C_cal, 1))

# Facteur de T3 : plus grande part du labour actuel compatible avec l'objectif (recherche par dichotomie sur les taux moyens)
bas_f, haut_f = np.zeros(E), np.ones(E)
for _ in range(50):
    milieu = (bas_f + haut_f) / 2
    trop = en_points(np.ones(E), taux * milieu, x_moy, len(FUTUR)) > OBJECTIF_PERTE_2035
    haut_f, bas_f = np.where(trop, milieu, haut_f), np.where(trop, bas_f, milieu)
facteur_t3 = bas_f

idx = tirages(len(cal), len(FUTUR))
TRAJ = {"T1": projeter(S0, h, x, idx), "T2": projeter(S0, h * (1 - part_t2)[:, None], x, idx), "T3": projeter(S0, h * facteur_t3[:, None], x, idx)}
sans_prl = projeter(S0, h * (1 - part_prl)[:, None], x, idx)


def centiles(c, axe=0):
    return np.percentile(c, [5, 50, 95], axis=axe)


def elargir(c):
    return np.stack([np.maximum(c[1] - K * (c[1] - c[0]), 0), c[1], c[1] + K * (c[2] - c[1])])


stats, region = {}, {}
for t, c in TRAJ.items():
    stats[t] = {"jalon": elargir(centiles(c[:, :, JALON])), "fin": elargir(centiles(c[:, :, -1])), "toutes": elargir(centiles(c))}
    tot = c.sum(axis=1)
    region[t] = {"jalon": centiles(tot[:, JALON]), "fin": centiles(tot[:, -1]), "toutes": centiles(tot)}
sp_fin, sp_reg = np.median(sans_prl[:, :, -1], axis=0), np.median(sans_prl[:, :, -1].sum(axis=1))

largeur = (stats["T1"]["fin"][2] - stats["T1"]["fin"][0]) / np.maximum(stats["T1"]["fin"][1], 1)
labour_actuel = taux * S0
exclu = np.array([epci[c]["exclu_comparaisons"].lower() == "true" for c in codes])


def fiabilite(i):
    if exclu[i] or labour_actuel[i] < 5:
        return "fragile"
    return "exploitable" if largeur[i] <= SEUIL_EXPLOITABLE else "indicative" if largeur[i] <= SEUIL_INDICATIF else "fragile"


# ---------- Foncier ----------
con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute("CREATE TABLE geo (insee VARCHAR, epci_code VARCHAR)")
for d in DEPS:
    con.execute(f"INSERT INTO geo SELECT code, codeEpci FROM ST_Read('{RAW / 'geo' / f'communes_{d}.geojson'}')")
flux = ", ".join(f"sum(naf{a}art{a + 1}) / 1e4" for a in range(21, 25))
lig = con.execute(f"""SELECT coalesce(g.epci_code, c.epci25), {flux}, sum(art16hab22) / 1e4, sum(naf16art22) / 1e4
    FROM read_csv('{RAW / 'consoenaf' / 'conso_com.csv'}', header=true, types={{'idcom': 'VARCHAR', 'iddep': 'VARCHAR', 'epci25': 'VARCHAR'}}) c
    LEFT JOIN geo g ON g.insee = c.idcom WHERE c.iddep IN {tuple(DEPS)} GROUP BY 1""").fetchall()
F, hab, tot16 = np.zeros((E, 4)), np.zeros(E), np.zeros(E)
for code, *v in lig:
    F[pos_e[code]] = v[:4]
    hab[pos_e[code]], tot16[pos_e[code]] = v[4], v[5]


def num(r, k):
    return float(r[k]) if r[k] != "" else np.nan


enveloppe = np.array([num(sobriete[c], "enveloppe_2021_2031_ha") for c in codes])
conso = np.array([num(sobriete[c], "conso_2021_2025_ha") for c in codes])
densite = np.array([num(sobriete[c], "logements_par_ha_habitat") for c in codes])
note("Contrôle", "flux annuels 2021-2024 contre conso_2021_2025_ha", "écart, ha", round(float(F.sum() - conso.sum()), 1), "doit valoir environ 0")
reste, rythme = enveloppe - conso, F.mean(axis=1)
part_hab = np.minimum(np.nan_to_num(hab / np.maximum(tot16, 1)), 1)
gain = np.where((densite > 0) & (densite < DENSITE_CIBLE), 1 - densite / DENSITE_CIBLE, 0)
facteur_f2 = 1 - part_hab * gain
idx_f = tirages(4, 6)
flux_f = F[:, idx_f]  # EPCI × tirages × années
f1 = conso[:, None] + flux_f.sum(axis=2)
f2 = conso[:, None] + flux_f.sum(axis=2) * facteur_f2[:, None]
moy_tirage = flux_f.mean(axis=2)


def epuisement(r, v):
    """Année décimale d'atteinte de l'enveloppe depuis le 1/1/2025 ; inférieure à 2025 si elle l'est déjà."""
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(r <= 0, 2025.0, 2025 + r / np.where(v > 0, v, np.nan))


ep = epuisement(reste, rythme)
ep_b, ep_h = np.nanpercentile(epuisement(reste[:, None], moy_tirage), [5, 95], axis=1)
rythme_cible = np.maximum(reste, 0) / 6
with np.errstate(divide="ignore", invalid="ignore"):
    effort_f3 = np.nan_to_num(np.clip(1 - rythme_cible / rythme, 0, 1))
    delta = rythme - rythme_cible
    flux_hab = part_hab * rythme
    densite_req = np.where((densite > 0) & (delta > 0) & (delta < flux_hab), densite * flux_hab / (flux_hab - delta), np.nan)
densite_req = np.where(densite_req > DENSITE_MAX, np.nan, densite_req)

# ---------- Sorties ----------
COLS = ["epci_code", "epci_nom", "perimetre", "fiabilite", "stock_anciennes_2024_ha", "taux_labour_pct_an", "labour_actuel_ha_an", "part_labour_zones_fragiles_pct", "part_labour_prl_pct",
        "t1_2031_ha", "t1_2031_bas", "t1_2031_haut", "t1_2035_ha", "t1_2035_bas", "t1_2035_haut", "t1_2035_pct_stock", "t1_2035_sans_prl_ha", "t2_2035_ha", "t2_2035_bas", "t2_2035_haut", "t2_epargne_2035_ha",
        "t3_2035_ha", "t3_2035_bas", "t3_2035_haut", "t3_epargne_2035_ha", "t3_effort_pct", "t3_labour_cible_ha_an",
        "enveloppe_ha", "conso_2021_2025_ha", "reste_ha", "rythme_actuel_ha_an", "f1_conso_2031_ha", "f1_conso_2031_bas", "f1_conso_2031_haut", "f1_pct_enveloppe", "f1_annee_atteinte", "f1_annee_atteinte_bas", "f1_annee_atteinte_haut",
        "part_habitat_pct", "densite_actuelle_logements_ha", "f2_conso_2031_ha", "f2_pct_enveloppe", "f3_rythme_cible_ha_an", "f3_effort_pct", "f3_densite_requise_logements_ha", "alerte_flux_unique"]


def arr(v, n=1):
    return "" if v is None or not np.isfinite(v) else round(float(v), n)


def ligne_epci(i):
    c, s, tj = codes[i], sobriete[codes[i]], stats
    return dict(zip(COLS, [c, epci[c]["epci_nom"], epci[c]["perimetre"], fiabilite(i), arr(S0[i], 0), arr(100 * taux[i], 2), arr(labour_actuel[i]), arr(100 * part_t2[i]), arr(100 * part_prl[i]),
                           arr(tj["T1"]["jalon"][1, i]), arr(tj["T1"]["jalon"][0, i]), arr(tj["T1"]["jalon"][2, i]), arr(tj["T1"]["fin"][1, i]), arr(tj["T1"]["fin"][0, i]), arr(tj["T1"]["fin"][2, i]),
                           arr(100 * tj["T1"]["fin"][1, i] / max(S0[i], 1)), arr(sp_fin[i]), arr(tj["T2"]["fin"][1, i]), arr(tj["T2"]["fin"][0, i]), arr(tj["T2"]["fin"][2, i]), arr(tj["T1"]["fin"][1, i] - tj["T2"]["fin"][1, i]),
                           arr(tj["T3"]["fin"][1, i]), arr(tj["T3"]["fin"][0, i]), arr(tj["T3"]["fin"][2, i]), arr(tj["T1"]["fin"][1, i] - tj["T3"]["fin"][1, i]), arr(100 * (1 - facteur_t3[i])), arr(taux[i] * facteur_t3[i] * S0[i]),
                           arr(enveloppe[i]), arr(conso[i]), arr(reste[i]), arr(rythme[i]), arr(np.median(f1[i])), arr(np.percentile(f1[i], 5)), arr(np.percentile(f1[i], 95)), arr(100 * (conso[i] + 6 * rythme[i]) / enveloppe[i] if enveloppe[i] else None),
                           arr(ep[i]), arr(ep_b[i]), arr(ep_h[i]), arr(100 * part_hab[i]), arr(densite[i]), arr(np.median(f2[i])), arr(100 * np.median(f2[i]) / enveloppe[i] if enveloppe[i] else None),
                           arr(rythme_cible[i]), arr(100 * effort_f3[i]), arr(densite_req[i]), s["alerte_flux_unique"]]))


# La densité et le rythme régionaux se recalculent sur les totaux : un taux moyen d'EPCI n'aurait pas de sens
tot_S, tot_lab = S0.sum(), labour_actuel.sum()
tot_reste, tot_rythme, tot_env, tot_conso = reste.sum(), rythme.sum(), enveloppe.sum(), conso.sum()
s_log = sum(float(sobriete[c]["delta_logements"] or 0) for c in codes)
s_hab = sum(float(sobriete[c]["conso_habitat_2016_2022_ha"] or 0) for c in codes)
d_reg, ph_reg = s_log / s_hab, hab.sum() / tot16.sum()
cible_reg = max(tot_reste, 0) / 6
ep_reg_b, ep_reg_h = np.percentile(epuisement(np.array([tot_reste]), moy_tirage.sum(axis=0)), [5, 95])
de = tot_rythme - cible_reg
fh = ph_reg * tot_rythme
R = region
ligne_reg = dict(zip(COLS, ["normandie", "Normandie", "71 EPCI, parties normandes", "région", arr(tot_S, 0), arr(100 * tot_lab / tot_S, 2), arr(tot_lab), arr(100 * (part_t2 * labour_actuel).sum() / tot_lab), arr(100 * (part_prl * labour_actuel).sum() / tot_lab),
                            arr(R["T1"]["jalon"][1]), arr(R["T1"]["jalon"][0]), arr(R["T1"]["jalon"][2]), arr(R["T1"]["fin"][1]), arr(R["T1"]["fin"][0]), arr(R["T1"]["fin"][2]), arr(100 * R["T1"]["fin"][1] / tot_S), arr(sp_reg),
                            arr(R["T2"]["fin"][1]), arr(R["T2"]["fin"][0]), arr(R["T2"]["fin"][2]), arr(R["T1"]["fin"][1] - R["T2"]["fin"][1]), arr(R["T3"]["fin"][1]), arr(R["T3"]["fin"][0]), arr(R["T3"]["fin"][2]), arr(R["T1"]["fin"][1] - R["T3"]["fin"][1]),
                            arr(100 * (1 - (taux * facteur_t3 * S0).sum() / tot_lab)), arr((taux * facteur_t3 * S0).sum()),
                            arr(tot_env), arr(tot_conso), arr(tot_reste), arr(tot_rythme), arr(np.median(f1.sum(axis=0))), arr(np.percentile(f1.sum(axis=0), 5)), arr(np.percentile(f1.sum(axis=0), 95)), arr(100 * (tot_conso + 6 * tot_rythme) / tot_env),
                            arr(float(epuisement(np.array([tot_reste]), np.array([tot_rythme]))[0])), arr(ep_reg_b), arr(ep_reg_h), arr(100 * ph_reg), arr(d_reg), arr(np.median(f2.sum(axis=0))), arr(100 * np.median(f2.sum(axis=0)) / tot_env),
                            arr(cible_reg), arr(100 * max(0, 1 - cible_reg / tot_rythme)), arr(d_reg * fh / (fh - de) if 0 < de < fh and d_reg * fh / (fh - de) <= DENSITE_MAX else None), ""]))
with open(PROC / "trajectoires_epci.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS, delimiter=";")
    w.writeheader()
    w.writerow(ligne_reg)
    w.writerows(ligne_epci(i) for i in range(E))
with open(PROC / "trajectoires_annuelles.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["territoire", "trajectoire", "annee", "bas", "median", "haut"])
    for t in TRAJ:
        for j, a in enumerate(FUTUR):
            w.writerow(["normandie", t, a, *(round(float(v[j])) for v in region[t]["toutes"])])
        for i, c in enumerate(codes):
            for j, a in enumerate(FUTUR):
                w.writerow([c, t, a, *(round(float(v[i, j]), 1) for v in stats[t]["toutes"])])

# ---------- Sensibilité régionale ----------
med = R["T1"]["fin"][1]
pentes = np.polyfit(np.array(ANNEES)[cal], 100 * A["vers_culture"][:, cal].sum(axis=0) / A["stock_debut"][:, cal].sum(axis=0), 1)
note("Hypothèses", "rythme de labour de la cohorte, 2017-2024", "pente (points de % par an)", round(float(pentes[0]), 3), "proche de 0 : pas de tendance nette, le rythme constant est défendable")
for lib, deb, fin in (("calibration 2019-2024", 2019, 2024), ("calibration 2017-2023, sans 2024, année basse", 2017, 2023)):
    c_ = [pos_a[a] for a in ANNEES if deb <= a <= fin]
    v = np.median(projeter(S0, H[:, c_], X[:, c_], tirages(len(c_), len(FUTUR)))[:, :, -1].sum(axis=1))
    note("Sensibilité T1", lib, "labour cumulé 2035, ha (écart)", f"{v:,.0f} ({100 * (v / med - 1):+.1f} %)")
v = np.median(projeter(S0, h, np.zeros_like(x), idx)[:, :, -1].sum(axis=1))
note("Sensibilité T1", "sans les autres sorties", "labour cumulé 2035, ha (écart)", f"{v:,.0f} ({100 * (v / med - 1):+.1f} %)")
note("Sensibilité T1", "labours de PRL exclus", "labour cumulé 2035, ha (écart)", f"{sp_reg:,.0f} ({100 * (sp_reg / med - 1):+.1f} %)")
for z, lib in (("vers_culture_reconnue", "zones reconnues : zones humides inventoriées, Natura 2000, ZNIEFF 1"), ("vers_culture_etendue", "zones reconnues + milieux potentiellement humides")):
    cz, sz = A[z][:, cal].sum(), A["stock_reconnue" if "reconnue" in z else "stock_etendue"][:, cal].sum()
    cn, sn = C_cal.sum() - cz, S_cal.sum() - sz
    note("Zones fragiles", lib, "part du labour / part du stock / rythme dedans / rythme dehors", f"{100 * cz / C_cal.sum():.1f} % / {100 * sz / S_cal.sum():.1f} % / {100 * cz / sz:.2f} % / {100 * cn / sn:.2f} %")
    v = np.median(projeter(S0, h * (1 - np.nan_to_num(A[z][:, cal].sum(axis=1) / np.maximum(C_cal, 1)))[:, None], x, idx)[:, :, -1].sum(axis=1))
    note("Zones fragiles", f"T2 avec {lib}", "labour cumulé 2035, ha (écart à T1)", f"{v:,.0f} ({100 * (v / med - 1):+.1f} %)")
note("Fiabilité EPCI", "largeur relative de la fourchette T1 2035", "médiane / min / max", f"{np.median(largeur):.2f} / {largeur.min():.2f} / {largeur.max():.2f}")
note("Fiabilité EPCI", "répartition", "exploitable / indicative / fragile", " / ".join(str(sum(fiabilite(i) == k for i in range(E))) for k in ("exploitable", "indicative", "fragile")))
note("T3", f"objectif : au plus {100 * OBJECTIF_PERTE_2035:.0f} % de la cohorte labourés d'ici 2035", "EPCI à effort nul / avec effort", f"{int((facteur_t3 >= .999).sum())} / {int((facteur_t3 < .999).sum())}")
note("F", "EPCI ayant déjà dépassé l'enveloppe au 1/1/2025", "nombre", int((reste < 0).sum()))
note("F", "EPCI atteignant l'enveloppe avant 2031 au rythme actuel", "nombre", int((ep < 2031).sum()))
with open(PROC / "trajectoires_validation.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.DictWriter(fo, fieldnames=["theme", "test", "mesure", "valeur", "lecture"], delimiter=";")
    w.writeheader()
    w.writerows(resultats)

(PROC / "trajectoires_parametres.json").write_text(json.dumps({
    "calibration": list(CALIBRATION), "horizon_prairies": FUTUR[-1], "jalon_prairies": FUTUR[JALON], "horizon_foncier": 2031, "objectif_perte_2035_pct": round(100 * OBJECTIF_PERTE_2035, 1),
    "densite_cible_logements_ha": DENSITE_CIBLE, "facteur_k_fourchettes_epci": round(K, 2)}, ensure_ascii=False), encoding="utf-8")

print("\nNormandie :", {k: ligne_reg[k] for k in COLS[4:27]})
print("Foncier :", {k: ligne_reg[k] for k in COLS[27:45]})
