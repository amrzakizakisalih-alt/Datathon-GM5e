"""Écran 2 « Où rendre » : potentiel écologique de renaturation des friches normandes.

Usage :
    python src/friches.py <friches.csv> <friches_epci.csv>

Source principale : observatoire des friches de l'EPF Normandie (DataNormandie, Licence ouverte 2.0,
5 068 sites). Son « potentiel de renaturation » (méthode ADEME : propriétaire, surface, bâti, pollution,
centralité, viabilisation…) mesure la FAISABILITÉ ; il ne regarde pas l'intérêt écologique. Ce script
ajoute un POTENTIEL ÉCOLOGIQUE calculé pour toutes les friches à partir de nos couches :
  dist_reservoir_m          distance à la ZNIEFF de type 1 ou au site Natura 2000 le plus proche (0 = dedans)
  part_humide_pct           part de la friche en zone humide inventoriée (DREAL) ou potentielle (MPH, classes 1-3)
  part_prairies_500m_pct    surface de prairies permanentes déclarées en 2024 (RPG Explorer) à moins de 500 m,
                            rapportée à la couronne de 500 m autour de la friche
  surface_ha
  contexte_urbain           friche en centre-bourg ou en quartier d'habitation (préréglage « nature en ville »)
Chaque critère est converti en rang centile (0-100), puis combiné par une somme pondérée selon trois
préréglages (score_biodiversite, score_eau, score_ville). Le préréglage par défaut est la biodiversité.
  robustesse_pct            part de 1 000 jeux de poids tirés au hasard (loi de Dirichlet sur les 4 critères
                            écologiques) où la friche reste dans les 10 % de potentiel le plus élevé
  classe                    « projet engagé » si un projet de reconversion est en démarches ou finalisé ;
                            « petite friche (< 0,1 ha) » ; sinon, parmi les friches éligibles :
                            « gain rapide » (potentiel >= 75e centile et faisabilité EPF >= médiane),
                            « fort potentiel, contraintes » (potentiel >= 75e centile, faisabilité < médiane),
                            « potentiel modéré »
  raisons                   les trois critères qui contribuent le plus au score par défaut, en clair
  vigilance                 points à vérifier avant toute décision : pollution avérée, potentielle ou non
                            renseignée (« non renseignée » ne veut pas dire « saine ») ; terrain constructible ;
                            zone inondable (PPRI). Une zone inondable est un atout écologique, mais une contrainte d'usage.
Aucune donnée personnelle : les friches sont des sites publiés par l'EPF ; aucune parcelle agricole n'est
affichée (les prairies ne servent qu'à un taux autour de la friche). Le nom de la friche n'est pas repris dans
friches.csv : certains contiennent un nom de personne ou une mention de succession. L'identifiant `gid` permet
de retrouver le site dans l'observatoire de l'EPF.
"""
import sys
from pathlib import Path

import duckdb
import numpy as np
import rasterio

from geo_utils import part_mph, rattacher_plus_proche

OUT, OUT_EPCI = sys.argv[1], sys.argv[2]
RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
DEPS = ["14", "27", "50", "61", "76"]
PRESETS = {  # poids : réservoir, humide, prairies, surface, ville
    "biodiversite": (0.35, 0.20, 0.30, 0.15, 0.00),
    "eau": (0.15, 0.60, 0.10, 0.15, 0.00),
    "ville": (0.15, 0.15, 0.05, 0.15, 0.50),
}
SURFACE_MIN_HA = 0.1        # en dessous, « petite friche » : renaturer quelques centaines de m² ne pèse pas à l'échelle d'un EPCI
CENTILE_POTENTIEL = 0.75    # seuil de « fort potentiel », calculé sur les friches éligibles (>= 0,1 ha, sans projet engagé)
PROJET_ENGAGE = ("Démarches foncières", "Démarches techniques", "Démarches foncières et techniques",
                 "Démarches financières", "Finalisé")

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute("CREATE TABLE communes (insee VARCHAR, epci_code VARCHAR, epci_nom VARCHAR, geom GEOMETRY)")
for d in DEPS:
    con.execute(f"""INSERT INTO communes SELECT code, codeEpci, json_extract_string(epci, '$.nom'),
                    ST_Transform(geom, 'EPSG:4326', 'EPSG:2154', always_xy := true)
                    FROM ST_Read('{RAW / 'geo' / f'communes_{d}.geojson'}')""")

con.execute(f"""
    CREATE TABLE f AS
    SELECT gid, nom_friche, insee_txt, nom_com, surface / 1e4 AS surface_ha, act_fri_lt, etat_bati, pollution,
           zonage, projet, typavanc, renaturati AS potentiel_epfn_renaturation, position, caracteris, ppri, zone_humid,
           ST_MakeValid(geom) AS geom, ST_PointOnSurface(geom) AS pt
    FROM ST_Read('{RAW / 'friches' / 'friches_epfn.geojson'}')
""")
emprise = "ST_MakeEnvelope(330000, 6780000, 640000, 7020000)"

# Réservoirs : ZNIEFF 1 et Natura 2000
con.execute(f"""CREATE TABLE res AS
    SELECT ST_MakeValid(geom) AS geom FROM ST_Read('{RAW / 'zonages' / 'znieff1.geojson'}')
    UNION ALL SELECT ST_MakeValid(geom) FROM ST_Read('{RAW / 'zonages' / 'natura2000.geojson'}')""")
con.execute("""CREATE TABLE d_res AS
    SELECT f.gid, min(ST_Distance(f.geom, r.geom)) AS d FROM f JOIN res r ON ST_DWithin(f.geom, r.geom, 5000) GROUP BY f.gid""")

# Zones humides inventoriées (DREAL) : part de la friche
con.execute(f"""CREATE TABLE zh AS SELECT ST_MakeValid(geom) AS geom
    FROM ST_Read('{RAW / 'zones_humides' / 'dataset' / 'drealnorm_zh_s_r28.shp'}')""")
con.execute("""CREATE TABLE p_zh AS
    WITH u AS (SELECT f.gid, ST_Union_Agg(z.geom) AS g FROM f JOIN zh z ON ST_Intersects(f.geom, z.geom) GROUP BY f.gid)
    SELECT u.gid, ST_Area(ST_Intersection(f.geom, u.g)) / nullif(ST_Area(f.geom), 0) AS part FROM u JOIN f USING (gid)""")

# Milieux potentiellement humides : part des pixels de 50 m de la friche en classes 1 à 3
mph = []
with rasterio.open(RAW / "mph" / "mph_normandie.tif") as r:
    for gid, gj, x, y in con.execute("SELECT gid, ST_AsGeoJSON(geom), ST_X(pt), ST_Y(pt) FROM f").fetchall():
        mph.append((gid, part_mph(r, gj, x, y)))
con.execute("CREATE TABLE p_mph (gid INTEGER, part DOUBLE)")
con.executemany("INSERT INTO p_mph VALUES (?, ?)", mph)

# Prairies permanentes déclarées en 2024 dans la couronne de 500 m (points des LCP)
con.execute("CREATE TABLE pp (pt GEOMETRY, ha DOUBLE)")
for d in DEPS:
    con.execute(f"""INSERT INTO pp SELECT ST_PointOnSurface(l.wkb_geometry), l.area_lcp
        FROM ST_Read('{RAW / 'rpg_explorer' / f'seq1524_d{d}.gpkg'}') l
        JOIN read_csv_auto('{RAW / 'rpg_explorer' / 'ref_fr_en.csv'}', header=true) r ON r.crop = l.crop24
        WHERE CAST(r.grp AS INTEGER) = 18""")
con.execute("""CREATE TABLE p_pp AS
    SELECT f.gid, sum(pp.ha) AS ha FROM f JOIN pp ON ST_DWithin(pp.pt, f.geom, 500) GROUP BY f.gid""")

# Rattachement aux EPCI
con.execute("""CREATE TABLE fe AS
    SELECT f.gid, c.insee, c.epci_code, c.epci_nom, f.pt FROM f LEFT JOIN communes c ON ST_Within(f.pt, c.geom)""")
rattacher_plus_proche(con, "fe", "gid", "t.pt")

con.execute(f"""
    CREATE TABLE crit AS
    SELECT f.gid, f.nom_com AS commune, fe.insee, fe.epci_code, fe.epci_nom,
           ST_X(ST_Transform(f.pt, 'EPSG:2154', 'EPSG:4326', always_xy := true)) AS lon,
           ST_Y(ST_Transform(f.pt, 'EPSG:2154', 'EPSG:4326', always_xy := true)) AS lat,
           f.surface_ha, f.act_fri_lt AS activite_ancienne, f.etat_bati, coalesce(f.pollution, 'non renseignée') AS pollution,
           CASE WHEN upper(f.zonage) LIKE 'AU%' THEN 'à urbaniser (AU)'
                WHEN upper(f.zonage) LIKE 'U%' OR upper(f.zonage) LIKE 'ZC%' THEN 'urbaine (U)'
                WHEN upper(f.zonage) LIKE 'A%' OR upper(f.zonage) LIKE 'N%' OR upper(f.zonage) LIKE 'ZNC%' THEN 'agricole ou naturelle (A/N)'
                ELSE 'non renseignée' END AS zonage_classe,
           f.typavanc IN {PROJET_ENGAGE} AS projet_engage, f.typavanc AS avancement_projet,
           f.potentiel_epfn_renaturation,
           coalesce(round(d.d), 5000) AS dist_reservoir_m,
           round(100 * greatest(coalesce(z.part, 0), coalesce(m.part, 0),
                                CASE WHEN f.zone_humid LIKE 'Av%' THEN 1 ELSE 0 END), 1) AS part_humide_pct,
           round(100 * least(coalesce(p.ha, 0) / nullif(ST_Area(ST_Buffer(f.geom, 500)) / 1e4 - f.surface_ha, 0), 1), 1)
               AS part_prairies_500m_pct,
           (f.position = 'centre' OR f.caracteris = 'Quartier d''habitation') AS contexte_urbain,
           f.ppri
    FROM f JOIN fe USING (gid) LEFT JOIN d_res d USING (gid) LEFT JOIN p_zh z USING (gid)
    LEFT JOIN p_mph m USING (gid) LEFT JOIN p_pp p USING (gid)
""")

# Rangs centiles et scores
rows = con.execute("""SELECT gid, dist_reservoir_m, part_humide_pct, part_prairies_500m_pct, surface_ha, contexte_urbain,
                             potentiel_epfn_renaturation, projet_engage FROM crit ORDER BY gid""").fetchall()
gid = np.array([r[0] for r in rows])


def centile(v):
    """Rang centile 0-100 (moyenne des rangs pour les ex aequo)."""
    v = np.asarray(v, dtype=float)
    ordre = v.argsort(kind="mergesort")
    rangs = np.empty(len(v))
    rangs[ordre] = np.arange(len(v))
    for val in np.unique(v):  # ex aequo
        idx = v == val
        rangs[idx] = rangs[idx].mean()
    return 100 * rangs / (len(v) - 1)


C = np.column_stack([
    centile([-r[1] for r in rows]),                 # proche d'un réservoir = mieux
    centile([r[2] for r in rows]),
    centile([r[3] for r in rows]),
    centile([np.log1p(r[4] * 1e4) for r in rows]),
    np.array([100.0 if r[5] else 0.0 for r in rows]),
])
scores = {nom: C @ np.array(w) for nom, w in PRESETS.items()}
pot = scores["biodiversite"]
faisa = np.array([r[6] for r in rows], dtype=float)
engage = np.array([bool(r[7]) for r in rows])

rng = np.random.default_rng(2026)
W = rng.dirichlet(np.ones(4), size=1000)            # 1 000 jeux de poids sur les 4 critères écologiques
S = C[:, :4] @ W.T                                   # friches x tirages
seuils = np.quantile(S, 0.9, axis=0)
robustesse = 100 * (S >= seuils).mean(axis=1)

petite = np.array([r[4] < SURFACE_MIN_HA for r in rows])
eligible = ~engage & ~petite
pseuil, fmed = np.quantile(pot[eligible], CENTILE_POTENTIEL), np.median(faisa[eligible])
classe = np.where(engage, "projet engagé", np.where(petite, "petite friche (< 0,1 ha)",
         np.where(pot >= pseuil, np.where(faisa >= fmed, "gain rapide", "fort potentiel, contraintes"), "potentiel modéré")))

# Raisons : les trois plus fortes contributions au score par défaut
crit = {r[0]: r for r in con.execute(
    "SELECT gid, dist_reservoir_m, part_humide_pct, part_prairies_500m_pct, surface_ha FROM crit").fetchall()}


def raison(k, r):
    if k == 0:
        return "dans une ZNIEFF ou un site Natura 2000" if r[1] == 0 else f"à {int(r[1])} m d'une ZNIEFF ou d'un site Natura 2000"
    if k == 1:
        return f"{r[2]:.0f} % en zone humide inventoriée ou potentielle"
    if k == 2:
        return f"{r[3]:.0f} % de prairies permanentes à moins de 500 m"
    return f"surface de {r[4]:.1f} ha".replace(".", ",")


w = np.array(PRESETS["biodiversite"][:4])
raisons = ["; ".join(raison(k, crit[g]) for k in np.argsort(-(C[i, :4] * w))[:3]) for i, g in enumerate(gid)]

con.execute("CREATE TABLE sc (gid INTEGER, score_biodiversite DOUBLE, score_eau DOUBLE, score_ville DOUBLE, "
            "robustesse_pct DOUBLE, classe VARCHAR, raisons VARCHAR)")
con.executemany("INSERT INTO sc VALUES (?, ?, ?, ?, ?, ?, ?)",
                [(int(g), round(float(scores['biodiversite'][i]), 1), round(float(scores['eau'][i]), 1),
                  round(float(scores['ville'][i]), 1), round(float(robustesse[i]), 1), str(classe[i]), raisons[i])
                 for i, g in enumerate(gid)])
con.execute(f"""COPY (SELECT c.* EXCLUDE (ppri, lon, lat), round(c.lon, 6) AS lon, round(c.lat, 6) AS lat,
                       sc.* EXCLUDE (gid), c.surface_ha < {SURFACE_MIN_HA} AS petite_friche,
                       concat_ws('; ',
                           CASE c.pollution WHEN 'Avérée' THEN 'pollution avérée' WHEN 'Potentielle' THEN 'pollution potentielle'
                                            WHEN 'Non connue' THEN 'pollution non connue'
                                            WHEN 'non renseignée' THEN 'pollution non renseignée' END,
                           CASE WHEN c.zonage_classe IN ('urbaine (U)', 'à urbaniser (AU)') THEN 'terrain constructible (pression foncière)' END,
                           CASE WHEN c.ppri IS NOT NULL AND c.ppri NOT IN ('Non', 'Ne sait pas') THEN 'zone inondable (PPRI)' END) AS vigilance
                FROM crit c JOIN sc USING (gid) ORDER BY sc.score_biodiversite DESC) TO '{OUT}' (HEADER, DELIMITER ';')""")

con.execute(f"""COPY (
    SELECT c.epci_code, any_value(c.epci_nom) AS epci_nom, count(*) AS n_friches, round(sum(c.surface_ha), 1) AS friches_ha,
           round(sum(c.surface_ha) FILTER (WHERE sc.classe = 'gain rapide'), 1) AS friches_gain_rapide_ha,
           count(*) FILTER (WHERE sc.classe = 'gain rapide') AS n_gain_rapide,
           round(sum(c.surface_ha) FILTER (WHERE sc.classe = 'fort potentiel, contraintes'), 1) AS friches_fort_potentiel_contraintes_ha,
           round(sum(c.surface_ha) FILTER (WHERE sc.classe = 'projet engagé'), 1) AS friches_projet_engage_ha
    FROM crit c JOIN sc USING (gid) GROUP BY c.epci_code ORDER BY friches_ha DESC) TO '{OUT_EPCI}' (HEADER, DELIMITER ';')""")

print("Friches :", con.execute("SELECT count(*), round(sum(surface_ha)) FROM crit").fetchone(),
      "| sans EPCI :", con.execute("SELECT count(*) FROM crit WHERE epci_code IS NULL").fetchone()[0])
print("Classes (n, ha) :", con.execute("SELECT classe, count(*), round(sum(c.surface_ha)) FROM crit c JOIN sc USING (gid) GROUP BY 1 ORDER BY 3 DESC").fetchall())
print(f"Seuils (friches éligibles : {eligible.sum()}) : potentiel {int(CENTILE_POTENTIEL * 100)}e centile = {pseuil:.1f} ; "
      f"faisabilité EPF médiane = {fmed:.0f}")
