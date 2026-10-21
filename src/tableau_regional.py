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
"""
import sys

import duckdb

DIR, EPCI_DEP, OUT = sys.argv[1:4]
con = duckdb.connect()
con.execute(f"CREATE TABLE ret AS SELECT * FROM read_csv_auto('{DIR}/retournements_epci_*.csv', delim=';', header=true, filename=true)")
con.execute(f"CREATE TABLE bc AS SELECT * FROM read_csv_auto('{DIR}/beton_charrue_epci_*.csv', delim=';', header=true)")
con.execute(f"CREATE TABLE ed AS SELECT * FROM read_csv_auto('{EPCI_DEP}', delim=';', header=true, types={{'epci_code': 'VARCHAR'}})")

con.execute("""
    CREATE TABLE r AS
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
    ORDER BY prairies_perdues_ha_an DESC
""")
con.execute(f"COPY r TO '{OUT}' (HEADER, DELIMITER ';')")
print(f"Écrit : {OUT} ({con.execute('SELECT count(*) FROM r').fetchone()[0]} EPCI)")
