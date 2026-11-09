"""Fichiers légers pour l'interface web, à partir de data/processed/.

Usage :
    python src/export_web.py

À lancer après pipeline.py, sensibilite.py et sensibilite_prl.py. Écrit dans web/data/ (format décrit dans web/data/LISEZ-MOI.md) :
  - regional.json          : totaux normands, sources, avertissements ;
  - epci_index.json        : une ligne légère par EPCI, pour la carte et la recherche ;
  - epci_contours.geojson  : contours simplifiés, sans trous entre voisins ;
  - epci/<code>.json       : la fiche complète d'un EPCI ;
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
    "territoire": ["population_2022", "surface_km2", "densite_2022", "part_pp_territoire_pct", "stock_pp_2015"],
    "charrue": ["charrue_toutes_ha_an", "charrue_anciennes_ha_an", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_sans_prl_ha_an",
                "part_prl_charrue_pct", "charrue_fenetre_ha_an", "charrue_anciennes_fenetre_ha_an"],
    "beton": ["beton_total_ha_an", "beton_sur_pp_ha_an", "beton_herbe_hors_pac_ha_an", "beton_hors_rpg_ha_an", "beton_ligneux_ha_an"],
    "bilan": ["prairies_perdues_ha_an", "prairies_perdues_haute_ha_an", "part_beton_pct", "part_beton_haute_pct", "perte_pct_stock_an"],
    "sols_rendus": ["desartif_sols_ha_an", "desartif_usage_ha_an"],
    "milieux_beton": ["beton_zh_ha_an", "beton_mph_ha_an", "beton_natura2000_ha_an", "beton_znieff1_ha_an", "beton_znieff2_ha_an"],
    "milieux_charrue": ["charrue_zh_ha_an", "charrue_zh_anc_ha_an", "charrue_mph_ha_an", "charrue_mph_anc_ha_an", "charrue_natura2000_ha_an",
                        "charrue_natura2000_anc_ha_an", "charrue_znieff1_ha_an", "charrue_znieff1_anc_ha_an"],
    "sobriete": ["conso_ref_ha", "conso_2021_2025_ha", "rythme_ref_ha_an", "rythme_actuel_ha_an", "enveloppe_2021_2031_ha", "enveloppe_consommee_pct",
                 "projection_2031_pct", "principal_flux_2021_2025", "part_principal_flux_pct", "alerte_flux_unique", "projection_2031_pct_hors_principal",
                 "conso_habitat_2016_2022_ha", "conso_activite_2016_2022_ha", "delta_logements", "delta_menages", "delta_population", "delta_emplois",
                 "logements_par_ha_habitat", "emplois_par_ha_activite"],
    "friches": ["n_friches", "friches_ha", "n_gain_rapide", "friches_gain_rapide_ha", "friches_fort_potentiel_contraintes_ha", "friches_projet_engage_ha",
                "annees_beton_friches", "annees_beton_gain_rapide"],
}
PROFIL = ["profil", "n_profil", "rang_perte_profil", "perte_pct_stock_an_mediane_profil", "part_beton_pct_mediane_profil"]
IDENTITE = ["departements", "perimetre", "hors_normandie", "part_hors_normandie_surface_pct", "part_hors_normandie_population_pct", "exclu_comparaisons", "fenetre_ocsge"]
TEXTE = {"epci_code", "epci_nom", "departements", "perimetre", "fenetre_ocsge", "profil", "principal_flux_2021_2025"}
# Ce qui s'additionne d'un EPCI à l'autre pour le total régional (les taux sont recalculés)
NON_SOMMABLE = {"densite_2022", "part_pp_territoire_pct", "part_prl_charrue_pct", "part_beton_pct", "part_beton_haute_pct", "perte_pct_stock_an",
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


for r in epci:
    ecrire(f"epci/{r['epci_code']}.json", {"code": r["epci_code"], "nom": r["epci_nom"], **{k: r[k] for k in IDENTITE},
                                           "comparaison": {k: r[k] for k in PROFIL}, **{g: {k: r[k] for k in cols} for g, cols in GROUPES.items()},
                                           "serie": format_serie(serie[r["epci_code"]])})
ecrire("epci_index.json", [{"code": r["epci_code"], "nom": r["epci_nom"], "profil": r["profil"], "perimetre": r["perimetre"], "exclu_comparaisons": r["exclu_comparaisons"],
                            **{k: r[k] for k in ("stock_pp_2015", "charrue_toutes_ha_an", "charrue_toutes_sans_prl_ha_an", "charrue_anciennes_ha_an", "beton_total_ha_an", "beton_sur_pp_ha_an", "perte_pct_stock_an", "part_beton_pct",
                                                 "rang_perte_profil", "enveloppe_consommee_pct", "friches_ha", "friches_gain_rapide_ha", "n_gain_rapide")}} for r in epci])

# Totaux régionaux
totaux = {g: {k: round(sum(r[k] or 0 for r in epci), 1) for k in cols if k not in NON_SOMMABLE} for g, cols in GROUPES.items()}
c, b, bi, so, fr, te = totaux["charrue"], totaux["beton"], totaux["bilan"], totaux["sobriete"], totaux["friches"], totaux["territoire"]
bi["part_beton_pct"] = round(100 * b["beton_sur_pp_ha_an"] / bi["prairies_perdues_ha_an"], 1)
bi["part_beton_haute_pct"] = round(100 * (b["beton_sur_pp_ha_an"] + b["beton_herbe_hors_pac_ha_an"]) / bi["prairies_perdues_haute_ha_an"], 1)
bi["perte_pct_stock_an"] = round(100 * bi["prairies_perdues_ha_an"] / te["stock_pp_2015"], 2)
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
    "avertissements": [
        "La charrue est déduite des déclarations PAC (RPG) : un changement de code d'une année à l'autre, pas un labour observé.",
        "Pic 2018 -> 2019 : effet du reclassement PAC de 2018 en prairies permanentes, à lire avec les prairies anciennes.",
        "Fourchette PRL : les chiffres sans_prl retirent les prairies en rotation longue, qui peuvent relever d'une rotation prévue.",
        "Un retournement en Natura 2000 ou en ZNIEFF n'est pas une infraction en soi.",
        "Le code PRL et la refonte du RPG de 2023 rendent la comparaison avant / après 2023 délicate.",
        "Les chiffres d'un EPCI à cheval sur une autre région ne portent que sur sa partie normande (voir perimetre).",
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
        "id": f["gid"], "libelle": f"{f['activite_ancienne'] or 'Friche'} à {f['commune']}", "commune": f["commune"], "surface_ha": round(float(f["surface_ha"]), 2), "classe": classe,
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
