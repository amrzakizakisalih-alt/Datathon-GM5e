"""Fichiers légers pour l'interface web, à partir de data/processed/.

Usage :
    python src/export_web.py

À lancer après pipeline.py, sensibilite.py, sensibilite_prl.py et trajectoires.py. Écrit dans web/data/ (format décrit dans web/data/LISEZ-MOI.md) :
  - regional.json          : totaux normands, trajectoires, sources, avertissements ;
  - epci_index.json        : une ligne légère par EPCI, pour la carte et la recherche ;
  - epci_contours.geojson  : contours simplifiés, sans trous entre voisins ;
  - epci/<code>.json       : la fiche complète d'un EPCI, avec ses trajectoires ;
  - friches.geojson        : un point par friche d'au moins 0,1 ha ;
  - friches/<code>.json    : le détail des friches d'un EPCI, chargé à la demande.
Seulement des agrégats : aucune parcelle agricole. Les noms de friches ne sont pas repris, car certains contiennent un nom de
personne, une adresse ou une mention de succession : le libellé est reconstruit (activité passée et commune). Les petites friches
(< 0,1 ha, souvent des maisons) ne comptent que dans les totaux.
"""
import csv
import glob
import gzip
import json
import shutil
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

import duckdb

RACINE = Path(__file__).resolve().parent.parent
PROC, RAW, OUT = RACINE / "data" / "processed", RACINE / "data" / "raw", RACINE / "web" / "data"
TOLERANCE_M = 200  # simplification des contours d'EPCI
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GROUPES = {
    "territoire": ["population_2022", "surface_km2", "densite_2022", "part_pp_territoire_pct", "stock_pp_2015", "stock_pp_debut_fenetre",
                   "stock_pp_anciennes_debut_fenetre"],
    "charrue": ["charrue_toutes_ha_an", "charrue_anciennes_ha_an", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_sans_prl_ha_an",
                "part_prl_charrue_pct", "charrue_fenetre_ha_an", "charrue_anciennes_fenetre_ha_an"],
    "beton": ["beton_total_ha_an", "beton_sur_pp_ha_an", "beton_sur_pp_anciennes_ha_an", "beton_herbe_hors_pac_ha_an", "beton_hors_rpg_ha_an", "beton_ligneux_ha_an"],
    # Les champs « anciennes » sont le chiffre principal ; les autres comptent toutes les prairies permanentes (borne haute)
    "bilan": ["prairies_anciennes_perdues_ha_an", "prairies_anciennes_perdues_haute_ha_an", "part_beton_anciennes_pct", "part_beton_anciennes_haute_pct",
              "perte_anciennes_pct_stock_an", "prairies_perdues_ha_an", "prairies_perdues_haute_ha_an", "part_beton_pct", "part_beton_haute_pct", "perte_pct_stock_an"],
    "sols_rendus": ["desartif_sols_ha_an", "desartif_usage_ha_an"],
    "milieux_beton": ["beton_zh_ha_an", "beton_mph_ha_an", "beton_natura2000_ha_an", "beton_znieff1_ha_an", "beton_znieff2_ha_an"],
    "milieux_charrue": ["charrue_zh_ha_an", "charrue_zh_anc_ha_an", "charrue_mph_ha_an", "charrue_mph_anc_ha_an", "charrue_natura2000_ha_an",
                        "charrue_natura2000_anc_ha_an", "charrue_znieff1_ha_an", "charrue_znieff1_anc_ha_an",
                        "charrue_zh_fen_ha_an", "charrue_mph_fen_ha_an", "charrue_natura2000_fen_ha_an", "charrue_znieff1_fen_ha_an"],
    "sobriete": ["conso_ref_ha", "conso_2021_2025_ha", "rythme_ref_ha_an", "rythme_actuel_ha_an", "enveloppe_2021_2031_ha", "enveloppe_consommee_pct",
                 "projection_2031_pct", "principal_flux_2021_2025", "part_principal_flux_pct", "alerte_flux_unique", "projection_2031_pct_hors_principal",
                 "conso_habitat_2016_2022_ha", "conso_activite_2016_2022_ha", "delta_logements", "delta_menages", "delta_population", "delta_emplois",
                 "logements_par_ha_habitat", "emplois_par_ha_activite"],
    "friches": ["n_friches", "friches_ha", "n_gain_rapide", "friches_gain_rapide_ha", "friches_fort_potentiel_contraintes_ha", "friches_projet_engage_ha",
                "annees_beton_friches", "annees_beton_gain_rapide"],
}
PROFIL = ["profil", "n_profil", "rang_perte_profil", "perte_anciennes_pct_stock_an_mediane_profil", "part_beton_anciennes_pct_mediane_profil"]
IDENTITE = ["departements", "perimetre", "hors_normandie", "part_hors_normandie_surface_pct", "part_hors_normandie_population_pct", "exclu_comparaisons", "fenetre_ocsge"]
TEXTE = {"epci_code", "epci_nom", "departements", "perimetre", "fenetre_ocsge", "profil", "principal_flux_2021_2025"}
# Ce qui s'additionne d'un EPCI à l'autre pour le total régional (les taux sont recalculés)
NON_SOMMABLE = {"densite_2022", "part_pp_territoire_pct", "part_prl_charrue_pct", "part_beton_pct", "part_beton_haute_pct", "perte_pct_stock_an",
                "part_beton_anciennes_pct", "part_beton_anciennes_haute_pct", "perte_anciennes_pct_stock_an",
                "enveloppe_consommee_pct", "projection_2031_pct", "principal_flux_2021_2025", "part_principal_flux_pct", "alerte_flux_unique",
                "projection_2031_pct_hors_principal", "logements_par_ha_habitat", "emplois_par_ha_activite", "annees_beton_friches", "annees_beton_gain_rapide"}
CLASSES = {"gain rapide": "gain_rapide", "fort potentiel, contraintes": "fort_potentiel_contraintes", "potentiel modéré": "potentiel_modere", "projet engagé": "projet_engage"}


def valeur(col, x):
    if x == "":
        return None
    if col in TEXTE:
        return x
    if x.lower() in ("true", "false"):
        return x.lower() == "true"
    try:
        n = float(x)
    except ValueError:
        return x
    return int(n) if n.is_integer() else n


def lire(chemin):
    return [{k: valeur(k, v) for k, v in r.items()} for r in csv.DictReader(open(chemin, encoding="utf-8"), delimiter=";")]


def a_commune(nom):
    """« à Rouen », « au Trait », « aux Andelys »."""
    if not nom:
        return ""
    if nom.startswith("Le "):
        return "au " + nom[3:]
    if nom.startswith("Les "):
        return "aux " + nom[4:]
    return "à " + nom


def ecrire(nom, objet):
    chemin = OUT / nom
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(objet, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if OUT.exists():
    for sous in ("epci", "friches"):
        shutil.rmtree(OUT / sous, ignore_errors=True)
OUT.mkdir(parents=True, exist_ok=True)

prl = {r["epci_code"]: r for r in csv.DictReader(open(PROC / "sensibilite_prl_epci.csv", encoding="utf-8"), delimiter=";")}
epci = []
for r in lire(PROC / "tableau_regional_epci.csv"):
    p = prl[r["epci_code"]]
    r.update({k: valeur(k, p[k]) for k in ("charrue_toutes_sans_prl_ha_an", "charrue_anciennes_sans_prl_ha_an", "part_prl_charrue_pct")})
    epci.append(r)
serie = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0, 0.0, 0.0]))
for f in glob.glob(str(PROC / "retournements_epci_*.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
        s = serie[r["epci_code"]][int(r["annee"])]
        for i, k in enumerate(("stock_pp", "strict_toutes", "strict_anciennes", "borne_haute")):
            s[i] += float(r[k])


def format_serie(s):
    return [{"annee": a, "stock_pp": round(v[0], 1), "charrue_toutes": round(v[1], 1), "charrue_anciennes": round(v[2], 1), "borne_haute": round(v[3], 1)} for a, v in sorted(s.items())]


traj = {r["epci_code"]: r for r in lire(PROC / "trajectoires_epci.csv")}
courbes = defaultdict(lambda: defaultdict(dict))
for r in csv.DictReader(open(PROC / "trajectoires_annuelles.csv", encoding="utf-8"), delimiter=";"):
    courbes[r["territoire"]][r["trajectoire"]][int(r["annee"])] = [valeur("", r[k]) for k in ("bas", "median", "haut")]
params = json.loads((PROC / "trajectoires_parametres.json").read_text(encoding="utf-8"))


def courbe(code, t):
    d = courbes[code][t]
    return {k: [d[a][i] for a in sorted(d)] for i, k in enumerate(("bas", "median", "haut"))}


def format_trajectoires(code):
    r = traj[code]
    return {
        "fiabilite": r["fiabilite"],
        "prairies": {
            **{k: r[k] for k in ("stock_anciennes_2024_ha", "taux_labour_pct_an", "labour_actuel_ha_an", "part_labour_zones_fragiles_pct", "part_labour_prl_pct")},
            "annees": sorted(courbes[code]["T1"]),
            "on_laisse_faire": {**courbe(code, "T1"), "pct_stock_2035": r["t1_2035_pct_stock"], "sans_prl_2035_ha": r["t1_2035_sans_prl_ha"]},
            "proteger_fragile": {**courbe(code, "T2"), "epargne_2035_ha": r["t2_epargne_2035_ha"]},
            "objectif": {**courbe(code, "T3"), "epargne_2035_ha": r["t3_epargne_2035_ha"], "effort_pct": r["t3_effort_pct"], "labour_cible_ha_an": r["t3_labour_cible_ha_an"]},
        },
        "foncier": {
            **{k: r[k] for k in ("enveloppe_ha", "conso_2021_2025_ha", "reste_ha", "rythme_actuel_ha_an", "alerte_flux_unique")},
            "deja_depassee": r["reste_ha"] < 0,
            "on_laisse_faire": {"conso_2031_ha": r["f1_conso_2031_ha"], "bas": r["f1_conso_2031_bas"], "haut": r["f1_conso_2031_haut"], "pct_enveloppe": r["f1_pct_enveloppe"],
                                "annee_atteinte": r["f1_annee_atteinte"], "annee_atteinte_bas": r["f1_annee_atteinte_bas"], "annee_atteinte_haut": r["f1_annee_atteinte_haut"]},
            "densifier": {"conso_2031_ha": r["f2_conso_2031_ha"], "pct_enveloppe": r["f2_pct_enveloppe"], "part_habitat_pct": r["part_habitat_pct"], "densite_actuelle_logements_ha": r["densite_actuelle_logements_ha"]},
            "tenir_enveloppe": {"rythme_cible_ha_an": r["f3_rythme_cible_ha_an"], "effort_pct": r["f3_effort_pct"], "densite_requise_logements_ha": r["f3_densite_requise_logements_ha"]},
        },
    }


for r in epci:
    ecrire(f"epci/{r['epci_code']}.json", {"code": r["epci_code"], "nom": r["epci_nom"], **{k: r[k] for k in IDENTITE},
                                           "comparaison": {k: r[k] for k in PROFIL}, **{g: {k: r[k] for k in cols} for g, cols in GROUPES.items()},
                                           "serie": format_serie(serie[r["epci_code"]]), "trajectoires": format_trajectoires(r["epci_code"])})
ecrire("epci_index.json", [{"code": r["epci_code"], "nom": r["epci_nom"], "profil": r["profil"], "perimetre": r["perimetre"], "exclu_comparaisons": r["exclu_comparaisons"],
                            **{k: r[k] for k in ("stock_pp_2015", "charrue_toutes_ha_an", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_ha_an", "beton_total_ha_an", "beton_sur_pp_ha_an", "beton_sur_pp_anciennes_ha_an", "perte_anciennes_pct_stock_an",
                                                 "perte_pct_stock_an", "part_beton_pct",
                                                 "rang_perte_profil", "enveloppe_consommee_pct", "friches_ha", "friches_gain_rapide_ha", "n_gain_rapide")},
                            "surface_km2": r["surface_km2"], "trajectoire_fiabilite": traj[r["epci_code"]]["fiabilite"], **{k: traj[r["epci_code"]][k] for k in ("t1_2035_pct_stock", "t3_effort_pct", "f1_annee_atteinte")}} for r in epci])

# Totaux régionaux
totaux = {g: {k: round(sum(r[k] or 0 for r in epci), 1) for k in cols if k not in NON_SOMMABLE} for g, cols in GROUPES.items()}
c, b, bi, so, fr, te = totaux["charrue"], totaux["beton"], totaux["bilan"], totaux["sobriete"], totaux["friches"], totaux["territoire"]
bi["part_beton_pct"] = round(100 * b["beton_sur_pp_ha_an"] / bi["prairies_perdues_ha_an"], 1)
bi["part_beton_haute_pct"] = round(100 * (b["beton_sur_pp_ha_an"] + b["beton_herbe_hors_pac_ha_an"]) / bi["prairies_perdues_haute_ha_an"], 1)
bi["perte_pct_stock_an"] = round(100 * bi["prairies_perdues_ha_an"] / te["stock_pp_debut_fenetre"], 2)
bi["part_beton_anciennes_pct"] = round(100 * b["beton_sur_pp_anciennes_ha_an"] / bi["prairies_anciennes_perdues_ha_an"], 1)
bi["part_beton_anciennes_haute_pct"] = round(100 * (b["beton_sur_pp_anciennes_ha_an"] + b["beton_herbe_hors_pac_ha_an"]) / bi["prairies_anciennes_perdues_haute_ha_an"], 1)
bi["perte_anciennes_pct_stock_an"] = round(100 * bi["prairies_anciennes_perdues_ha_an"] / te["stock_pp_anciennes_debut_fenetre"], 2)
c["part_prl_charrue_pct"] = round(100 * (1 - c["charrue_toutes_sans_prl_ha_an"] / c["charrue_toutes_ha_an"]), 1)
so["enveloppe_consommee_pct"] = round(100 * so["conso_2021_2025_ha"] / so["enveloppe_2021_2031_ha"], 1)
so["projection_2031_pct"] = round(250 * so["conso_2021_2025_ha"] / so["enveloppe_2021_2031_ha"], 1)
fr["annees_beton_friches"] = round(fr["friches_ha"] / b["beton_total_ha_an"], 1)
fr["annees_beton_gain_rapide"] = round(fr["friches_gain_rapide_ha"] / b["beton_total_ha_an"], 1)
te["densite_2022"] = round(te["population_2022"] / te["surface_km2"], 1)
sens = {r["test"]: r for r in csv.DictReader(open(PROC / "sensibilite.csv", encoding="utf-8"), delimiter=";")}
noyau = next(v for k, v in sens.items() if k.startswith("noyau stable"))
reg_serie = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
for s in serie.values():
    for a, v in s.items():
        for i in range(4):
            reg_serie[a][i] += v[i]
profils = defaultdict(int)
for r in epci:
    profils[r["profil"]] += 1
ecrire("regional.json", {
    "genere_le": date.today().isoformat(), "n_epci": len(epci), "totaux": totaux, "serie": format_serie(reg_serie), "profils": dict(profils),
    "friches_noyau_stable": {"n_sur_gains_rapides": noyau["valeur"], "surface": noyau["lecture"]},
    "trajectoires": {
        **format_trajectoires("normandie"), "hypotheses": params,
        "avertissements": [
            "Ce sont des trajectoires conditionnelles, pas des prévisions : si tel comportement se poursuit, voici le résultat.",
            "Seules les trajectoires « on laisse faire » prolongent des données observées. Les autres traduisent des hypothèses.",
            f"L'objectif de {params['objectif_perte_2035_pct']:g} % et la densité de {params['densite_cible_logements_ha']} logements par hectare sont des exemples, à remplacer par ceux de la Région.",
            "La fourchette suppose un avenir semblable aux années observées. Elle ne tient compte ni des prix agricoles, ni d'un changement de règles.",
            "Les années 2017-2024 comprennent des campagnes où la PAC a restreint les retournements en Normandie : régime d'autorisation en 2017, interdiction décidée fin 2023 puis levée fin 2024. « On laisse faire » prolonge donc aussi ces restrictions.",
            "Les hectares labourés sont déduits des déclarations PAC. Les autres sorties des déclarations ne sont jamais comptées comme des labours.",
            "Le repère foncier applique l'objectif national à chaque territoire, avec les fichiers fonciers du Cerema. L'objectif réel est fixé par le SRADDET : un taux par territoire, mesuré avec la CCF de l'EPF Normandie, puis réduit de 15 % pour une enveloppe régionale.",
        ],
    },
    "avertissements": [
        "La charrue est déduite des déclarations PAC (RPG) : un changement de code d'une année à l'autre, pas un labour observé.",
        "Le chiffre principal ne compte que les prairies anciennes, déclarées permanentes sans interruption depuis 2015. Compter toutes les prairies permanentes donne presque le double sur 2019-2023 : c'est la borne haute, qui inclut des prairies semées dans une rotation.",
        "Pic 2018 -> 2019 : effet du reclassement PAC de 2018 en prairies permanentes, à lire avec les prairies anciennes.",
        "Fourchette PRL : le chiffre bas retire les prairies en rotation longue, dont le retournement peut relever d'une rotation prévue.",
        "Un retournement en Natura 2000 ou en ZNIEFF n'est pas une infraction en soi.",
        "Le code PRL et la refonte du RPG de 2023 rendent la comparaison avant / après 2023 délicate.",
        "Les chiffres d'un EPCI à cheval sur une autre région ne portent que sur sa partie normande, indiquée dans sa fiche.",
        "« Pollution non renseignée » ne veut pas dire « site sain ». Toute friche se vérifie sur place avant décision.",
    ],
    "sources": [
        "RPG Explorer, INRAE / AgroParisTech (Girault & Martin), d'après le RPG IGN-ASP, Licence Etalab 2.0", "OCS GE Artificialisation, IGN",
        "Communes et EPCI, geo.api.gouv.fr", "ZNIEFF et Natura 2000, MNHN via IGN", "Inventaire des zones humides, DREAL Normandie",
        "Milieux potentiellement humides, INRAE", "Observatoire des friches, EPF Normandie, Licence ouverte 2.0", "Consommation d'espaces, Cerema",
        "Séries historiques du recensement, INSEE",
    ],
})

# Contours : la simplification de couverture garde les limites communes entre voisins
con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
srcs = " UNION ALL ".join(f"SELECT codeEpci AS epci, ST_Transform(ST_MakeValid(geom), 'EPSG:4326', 'EPSG:2154', always_xy := true) AS g FROM ST_Read('{RAW / 'geo' / f'communes_{d}.geojson'}')"
                          for d in ["14", "27", "50", "61", "76"])
con.execute(f"CREATE TABLE e AS SELECT epci, ST_Union_Agg(g) AS g FROM ({srcs}) GROUP BY epci")
con.execute(f"CREATE TABLE s AS SELECT unnest(ST_Dump(ST_CoverageSimplify(list(g), {TOLERANCE_M}.0))).geom AS g FROM e")
con.execute("""CREATE TABLE r AS SELECT epci, ST_Collect(list(g)) AS g FROM (
        SELECT s.g, arg_min(e.epci, ST_Distance(ST_PointOnSurface(s.g), e.g)) AS epci FROM s, e GROUP BY s.g) GROUP BY epci""")
noms = {r["epci_code"]: r["epci_nom"] for r in epci}
features = []
for code, gj in con.execute("SELECT epci, ST_AsGeoJSON(ST_Transform(g, 'EPSG:2154', 'EPSG:4326', always_xy := true)) FROM r").fetchall():
    geom = json.loads(gj)
    arrondi = lambda x: [round(x[0], 4), round(x[1], 4)] if isinstance(x[0], (int, float)) else [arrondi(y) for y in x]
    features.append({"type": "Feature", "properties": {"code": code, "nom": noms[code]}, "geometry": {"type": geom["type"], "coordinates": arrondi(geom["coordinates"])}})
ecrire("epci_contours.geojson", {"type": "FeatureCollection", "features": features})

# Friches : points pour la carte, détail par EPCI
friches = lire(PROC / "friches.csv")
points, details = [], defaultdict(list)
for f in friches:
    if f["classe"] not in CLASSES:
        continue
    classe = CLASSES[f["classe"]]
    points.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [round(float(f["lon"]), 4), round(float(f["lat"]), 4)]},
                   "properties": {"id": f["gid"], "epci": f["epci_code"], "ha": round(float(f["surface_ha"]), 2), "classe": classe, "bio": round(f["score_biodiversite"]),
                                  "eau": round(f["score_eau"]), "ville": round(f["score_ville"]), "faisabilite": f["potentiel_epfn_renaturation"], "robustesse": round(f["robustesse_pct"])}})
    details[f["epci_code"]].append({
        "id": f["gid"], "libelle": f"{f['activite_ancienne'] or 'Friche'} {a_commune(f['commune'])}".strip(), "commune": f["commune"], "surface_ha": round(float(f["surface_ha"]), 2), "classe": classe,
        "activite_ancienne": f["activite_ancienne"], "etat_bati": f["etat_bati"], "pollution": f["pollution"], "zonage": f["zonage_classe"], "avancement_projet": f["avancement_projet"],
        "faisabilite_epfn": f["potentiel_epfn_renaturation"], "dist_reservoir_m": f["dist_reservoir_m"], "part_humide_pct": f["part_humide_pct"], "part_prairies_500m_pct": f["part_prairies_500m_pct"],
        "score_biodiversite": f["score_biodiversite"], "score_eau": f["score_eau"], "score_ville": f["score_ville"], "robustesse_pct": f["robustesse_pct"],
        "raisons": (f["raisons"] or "").split("; ") if f["raisons"] else [], "vigilance": f["vigilance"].split("; ") if f["vigilance"] else []})
ecrire("friches.geojson", {"type": "FeatureCollection", "features": points})
for r in epci:
    ecrire(f"friches/{r['epci_code']}.json", sorted(details[r["epci_code"]], key=lambda x: -(x["score_biodiversite"] or 0)))

# Contrôles
assert len(epci) == 71 and len(list((OUT / "epci").glob("*.json"))) == 71 and len(features) == 71, "il faut 71 EPCI"
assert len(points) == sum(1 for f in friches if f["classe"] in CLASSES) and all(p["properties"]["epci"] for p in points), "friches sans EPCI"
for code in [r["epci_code"] for r in epci] + ["normandie"]:
    assert code in traj, f"trajectoire absente : {code}"
    for t, cle in (("T1", "t1_2035_ha"), ("T2", "t2_2035_ha"), ("T3", "t3_2035_ha")):
        cb = courbe(code, t)
        assert all(len(v) == 11 for v in cb.values()) and all(a <= b <= c for a, b, c in zip(cb["bas"], cb["median"], cb["haut"])), f"courbe {t} incohérente : {code}"
        assert abs(cb["median"][-1] - traj[code][cle]) <= 1, f"courbe {t} différente du résumé : {code}"
for chemin in OUT.rglob("*"):
    if chemin.is_file() and chemin.suffix in (".json", ".geojson"):
        t = chemin.read_text(encoding="utf-8")
        for interdit in ("id_lcp", "nom_friche", "wkb_geometry", "NaN"):
            assert interdit not in t, f"{interdit} dans {chemin}"
print("totaux :", {k: c[k] for k in ("charrue_toutes_ha_an", "charrue_anciennes_ha_an", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_sans_prl_ha_an")}, b, totaux["sols_rendus"])
print("bilan :", bi, "| sobriété :", so["conso_ref_ha"], so["conso_2021_2025_ha"], so["enveloppe_consommee_pct"], so["projection_2031_pct"], "| friches :", fr, "| profils :", dict(profils))
print("points friches :", len(points), "| sommets contours :", sum(json.dumps(x["geometry"]["coordinates"]).count("],") for x in features))
for chemin in sorted(OUT.iterdir()):
    if chemin.is_file() and chemin.suffix != ".md":
        print(f"{chemin.name} : {chemin.stat().st_size / 1024:.0f} Ko ({len(gzip.compress(chemin.read_bytes())) / 1024:.0f} Ko compressé)")
for sous in ("epci", "friches"):
    tailles = [x.stat().st_size for x in (OUT / sous).glob("*.json")]
    print(f"{sous}/ : {len(tailles)} fichiers, {sum(tailles) / 1024:.0f} Ko au total, maximum {max(tailles) / 1024:.0f} Ko")
