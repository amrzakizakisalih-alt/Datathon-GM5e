"""Tableau régional « béton + charrue » par EPCI, en ha par an.

Usage :
    python src/tableau_regional.py <dossier data/processed> <epci_departements.csv> <sortie.csv>

Entrées par département XX : retournements_epci_XX.csv et beton_charrue_epci_XX.csv.
Un EPCI à cheval sur deux départements normands est la somme de ses parties. Chaque partie
est d'abord annualisée sur la fenêtre OCS GE de son département (2019-2022 ou 2020-2023).
Ses colonnes « fenetre_ocsge » indiquent alors « mixte ».

Colonnes principales :
  stock_pp_2015                 prairies permanentes déclarées en 2015 (ha)
  charrue_toutes_ha_an          retournements stricts, toutes PP, moyenne 2015->2024 (ha/an)
  charrue_anciennes_ha_an       retournements stricts de PP anciennes, moyenne 2015->2024 (ha/an)
  beton_total_ha_an             artificialisation officielle IGN sur la fenêtre OCS GE (ha/an)
  beton_sur_pp_ha_an            dont sur des PP déclarées l'année de début (ha/an)
  beton_hors_rpg_ha_an          dont hors des parcelles déclarées (ha/an)
  beton_herbe_hors_pac_ha_an    dont sur de l'herbe agricole hors parcelle déclarée : prairies probables hors PAC (ha/an)
  desartif_sols_ha_an           désartificialisation IGN de sols bâtis, revêtus ou stabilisés (ha/an)
  desartif_usage_ha_an          désartificialisation IGN par simple changement d'usage d'une surface végétalisée (ha/an)
  charrue_fenetre_ha_an         retournements stricts sur la même fenêtre, nets du béton (ha/an)
  prairies_perdues_ha_an        beton_sur_pp + charrue_fenetre (ha/an), borne basse
  part_beton_pct                part du béton dans les prairies permanentes perdues (fenêtre), borne basse
  prairies_perdues_haute_ha_an  idem en ajoutant les prairies probables hors PAC bétonnées
  part_beton_haute_pct          part du béton, borne haute
  perte_pct_stock_an            prairies_perdues_ha_an / stock_pp_2015
  hors_normandie                EPCI dont une partie des communes est hors des 5 départements
  part_hors_normandie_surface_pct, part_hors_normandie_population_pct
  perimetre                     « EPCI entier » ou « partie normande (X % de la surface) » : tous les chiffres
                                d'un EPCI à cheval ne portent que sur sa partie normande
  exclu_comparaisons            vrai si au moins la moitié de la surface est hors Normandie (Pays de Dreux,
                                Maine Saosnois) : rang et médianes du profil sont alors vides
  profil, n_profil, rang_perte_profil, perte_pct_stock_an_mediane_profil, part_beton_pct_mediane_profil
  n_friches, friches_ha, friches_gain_rapide_ha, n_gain_rapide, friches_fort_potentiel_contraintes_ha,
  friches_projet_engage_ha      écran 2, depuis friches_epci.csv (voir src/friches.py)
  annees_beton_friches          surface totale des friches / béton annuel : combien d'années de béton elles représentent
  annees_beton_gain_rapide      idem pour les seules friches « gain rapide »
"""
import sys

import duckdb

DIR, EPCI_DEP, OUT = sys.argv[1:4]
# Seuils des profils d'EPCI (voir tests/T8) : densité en hab/km², part des prairies permanentes dans le territoire en %
SEUIL_URBAIN, SEUIL_PERIURBAIN, SEUIL_HERBAGER = 300, 100, 20
# EPCI à cheval sur une autre région : seule la partie normande est calculée. Au-delà de ce seuil de surface
# hors Normandie (en %), l'EPCI est exclu des comparaisons (rang et médianes de profil laissés vides).
SEUIL_EXCLUSION = 50
con = duckdb.connect()
con.execute(f"CREATE TABLE ret AS SELECT * FROM read_csv_auto('{DIR}/retournements_epci_*.csv', delim=';', header=true, filename=true)")
con.execute(f"CREATE TABLE bc AS SELECT * FROM read_csv_auto('{DIR}/beton_charrue_epci_*.csv', delim=';', header=true)")
con.execute(f"CREATE TABLE ed AS SELECT * FROM read_csv_auto('{EPCI_DEP}', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")

con.execute("""
    CREATE TABLE base AS
    WITH charrue AS (
        SELECT CAST(epci_code AS VARCHAR) AS epci_code, any_value(epci_nom) AS epci_nom,
               sum(stock_pp) FILTER (WHERE annee = 2016) AS stock_pp_2015,
               sum(strict_toutes) / 9 AS charrue_toutes_ha_an,
               sum(strict_anciennes) / 9 AS charrue_anciennes_ha_an
        FROM ret GROUP BY 1),
    fen AS (
        SELECT CAST(epci_code AS VARCHAR) AS epci_code,
               CASE WHEN count(DISTINCT debut) > 1 THEN 'mixte' ELSE any_value(debut || '-' || fin) END AS fenetre_ocsge,
               sum(beton_total / (fin - debut)) AS beton_total_ha_an,
               sum(beton_sur_pp / (fin - debut)) AS beton_sur_pp_ha_an,
               sum(beton_hors_rpg / (fin - debut)) AS beton_hors_rpg_ha_an,
               sum(beton_herbe_hors_pac / (fin - debut)) AS beton_herbe_hors_pac_ha_an,
               sum(desartif_sols / (fin - debut)) AS desartif_sols_ha_an,
               sum(desartif_usage / (fin - debut)) AS desartif_usage_ha_an,
               sum(charrue_pp / (fin - debut)) AS charrue_fenetre_ha_an,
               sum(charrue_pp_anciennes / (fin - debut)) AS charrue_anciennes_fenetre_ha_an
        FROM bc GROUP BY 1)
    SELECT c.epci_code, c.epci_nom, ed.departements, ed.hors_normandie, f.fenetre_ocsge,
           round(c.stock_pp_2015) AS stock_pp_2015,
           round(c.charrue_toutes_ha_an, 1) AS charrue_toutes_ha_an,
           round(c.charrue_anciennes_ha_an, 1) AS charrue_anciennes_ha_an,
           round(f.beton_total_ha_an, 1) AS beton_total_ha_an,
           round(f.beton_sur_pp_ha_an, 1) AS beton_sur_pp_ha_an,
           round(f.beton_hors_rpg_ha_an, 1) AS beton_hors_rpg_ha_an,
           round(f.beton_herbe_hors_pac_ha_an, 1) AS beton_herbe_hors_pac_ha_an,
           round(f.desartif_sols_ha_an, 1) AS desartif_sols_ha_an,
           round(f.desartif_usage_ha_an, 1) AS desartif_usage_ha_an,
           round(f.charrue_fenetre_ha_an, 1) AS charrue_fenetre_ha_an,
           round(f.charrue_anciennes_fenetre_ha_an, 1) AS charrue_anciennes_fenetre_ha_an,
           round(f.beton_sur_pp_ha_an + f.charrue_fenetre_ha_an, 1) AS prairies_perdues_ha_an,
           round(100 * f.beton_sur_pp_ha_an / nullif(f.beton_sur_pp_ha_an + f.charrue_fenetre_ha_an, 0), 1) AS part_beton_pct,
           round(f.beton_sur_pp_ha_an + f.beton_herbe_hors_pac_ha_an + f.charrue_fenetre_ha_an, 1) AS prairies_perdues_haute_ha_an,
           round(100 * (f.beton_sur_pp_ha_an + f.beton_herbe_hors_pac_ha_an)
                 / nullif(f.beton_sur_pp_ha_an + f.beton_herbe_hors_pac_ha_an + f.charrue_fenetre_ha_an, 0), 1) AS part_beton_haute_pct,
           round(100 * (f.beton_sur_pp_ha_an + f.charrue_fenetre_ha_an) / nullif(c.stock_pp_2015, 0), 2) AS perte_pct_stock_an
    FROM charrue c JOIN fen f USING (epci_code) LEFT JOIN ed USING (epci_code)
""")

# Bloc D : béton annualisé sur la fenêtre de chaque partie départementale, charrue moyenne 2015->2024
con.execute(f"CREATE TABLE q AS SELECT * FROM read_csv_auto('{DIR}/qualite_epci_*.csv', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")
qcols = [c[0] for c in con.execute("DESCRIBE q").fetchall()]
qsel = ", ".join(
    [f"round(sum({c} / (fin - debut)), 1) AS {c}_ha_an" for c in qcols if c.startswith("beton_")]
    + [f"round(sum({c}) / 9, 1) AS {c}_ha_an" for c in qcols if c.startswith("charrue_")])
con.execute(f"CREATE TABLE qa AS SELECT epci_code, {qsel} FROM q GROUP BY epci_code")

# Bloc E : trajectoire ZAN et efficacité (déjà par EPCI)
con.execute(f"CREATE TABLE s AS SELECT * EXCLUDE (epci_nom) FROM read_csv_auto('{DIR}/sobriete_epci.csv', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")

# Écran 2 : friches de l'EPCI, et lien avec le béton (« combien d'années de béton les friches représentent »)
con.execute(f"CREATE TABLE fr AS SELECT * EXCLUDE (epci_nom) FROM read_csv_auto('{DIR}/friches_epci.csv', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")

# Bloc F : profil de l'EPCI, pour comparer à des territoires semblables plutôt qu'à toute la région
con.execute(f"""
    CREATE TABLE r AS
    WITH t AS (
        SELECT b.*, coalesce(ed.part_hors_normandie_surface_pct, 0) AS part_hors_normandie_surface_pct,
               coalesce(ed.part_hors_normandie_population_pct, 0) AS part_hors_normandie_population_pct,
               qa.* EXCLUDE (epci_code), s.* EXCLUDE (epci_code), fr.* EXCLUDE (epci_code),
               round(fr.friches_ha / nullif(b.beton_total_ha_an, 0), 1) AS annees_beton_friches,
               round(coalesce(fr.friches_gain_rapide_ha, 0) / nullif(b.beton_total_ha_an, 0), 1) AS annees_beton_gain_rapide,
               round(100 * b.stock_pp_2015 / (s.surface_km2 * 100), 1) AS part_pp_territoire_pct
        FROM base b LEFT JOIN ed USING (epci_code) LEFT JOIN qa USING (epci_code) LEFT JOIN s USING (epci_code)
        LEFT JOIN fr USING (epci_code)),
    p AS (
        SELECT *, CASE
            WHEN densite_2022 >= {SEUIL_URBAIN} THEN 'urbain'
            WHEN densite_2022 >= {SEUIL_PERIURBAIN} THEN 'périurbain'
            WHEN part_pp_territoire_pct >= {SEUIL_HERBAGER} THEN 'rural herbager'
            ELSE 'rural de grandes cultures' END AS profil,
            CASE WHEN part_hors_normandie_surface_pct = 0 THEN 'EPCI entier'
                 ELSE 'partie normande (' || CAST(round(100 - part_hors_normandie_surface_pct) AS INTEGER) || ' % de la surface)' END AS perimetre,
            part_hors_normandie_surface_pct >= {SEUIL_EXCLUSION} AS exclu_comparaisons
        FROM t),
    -- Comparaisons calculées sur les seuls EPCI dont on couvre l'essentiel du territoire
    c AS (
        SELECT epci_code,
               count(*) OVER (PARTITION BY profil) AS n_profil,
               rank() OVER (PARTITION BY profil ORDER BY perte_pct_stock_an DESC) AS rang_perte_profil,
               round(median(perte_pct_stock_an) OVER (PARTITION BY profil), 2) AS perte_pct_stock_an_mediane_profil,
               round(median(part_beton_pct) OVER (PARTITION BY profil), 1) AS part_beton_pct_mediane_profil
        FROM p WHERE NOT exclu_comparaisons)
    SELECT p.*, c.* EXCLUDE (epci_code)
    FROM p LEFT JOIN c USING (epci_code) ORDER BY prairies_perdues_ha_an DESC
""")
con.execute(f"COPY r TO '{OUT}' (HEADER, DELIMITER ';')")
print(f"Écrit : {OUT} ({con.execute('SELECT count(*) FROM r').fetchone()[0]} EPCI)")
