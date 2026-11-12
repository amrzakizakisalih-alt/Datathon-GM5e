"""Bloc E : trajectoire ZAN et efficacité de la consommation d'espaces, par EPCI.

Usage :
    python src/sobriete_epci.py <sortie.csv>

Sources (data/raw/, voir telecharger_donnees.py) : consommation d'espaces naturels, agricoles et
forestiers (ENAF) par commune du Cerema (CONSOENAF, fichiers fonciers, en m²), séries historiques
du recensement de l'INSEE (logements), communes et EPCI de geo.api.gouv.fr. Seules les communes des
5 départements normands sont comptées ; une commune absente du découpage geo.api prend l'EPCI que lui
donne le Cerema.

Trajectoire ZAN (de référence : réduction de moitié 2021-2031 par rapport à 2011-2021 ; la
territorialisation du SRADDET peut fixer d'autres taux par territoire) :
  conso_ref_ha                  consommation du 1/1/2011 au 1/1/2021 (10 ans)
  conso_2021_2025_ha            consommation du 1/1/2021 au 1/1/2025 (4 ans)
  rythme_ref_ha_an, rythme_actuel_ha_an
  enveloppe_2021_2031_ha        moitié de conso_ref_ha
  enveloppe_consommee_pct       part de l'enveloppe déjà consommée au 1/1/2025
  projection_2031_pct           consommation 2021-2031 au rythme actuel, en % de l'enveloppe
  principal_flux_2021_2025      plus gros flux annuel d'une commune de l'EPCI entre 2021 et 2025 (commune, année, ha, destination)
  part_principal_flux_pct       part de ce flux dans la consommation 2021-2025 de l'EPCI
  alerte_flux_unique            vrai si ce flux fait au moins 20 ha et la moitié de la consommation 2021-2025 :
                                la projection repose alors sur un seul projet (ou une anomalie cadastrale), à vérifier
  projection_2031_pct_hors_principal   projection sans ce flux
Efficacité, recensements 2016 et 2022 face à la consommation du 1/1/2016 au 1/1/2022 :
  conso_habitat_2016_2022_ha, conso_activite_2016_2022_ha
  delta_logements, delta_menages, delta_population, delta_emplois (emplois au lieu de travail, INSEE)
  logements_par_ha_habitat, emplois_par_ha_activite   vides si moins de 1 ha consommé ; négatifs quand
                                logements ou emplois ont baissé malgré la consommation d'espace
  population_2022, surface_km2, densite_2022 (hab/km²)
"""
import sys
from pathlib import Path

import duckdb

OUT = sys.argv[1]
RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
DEPS = ["14", "27", "50", "61", "76"]

con = duckdb.connect()
con.execute("INSTALL spatial; LOAD spatial;")
con.execute("CREATE TABLE geo (insee VARCHAR, epci_code VARCHAR, epci_nom VARCHAR)")
for d in DEPS:
    con.execute(f"""INSERT INTO geo SELECT code, codeEpci, json_extract_string(epci, '$.nom')
                    FROM ST_Read('{RAW / 'geo' / f'communes_{d}.geojson'}')""")

act = " + ".join(f"coalesce(art{y}act{y + 1}, 0)" for y in range(16, 22))
con.execute(f"""
    CREATE TABLE conso AS
    SELECT idcom AS insee, epci25, naf11art21, naf21art25, art16hab22, ({act}) AS art16act22,
           pop16, pop22, men16, men22, emp16, emp22, surfcom2025
    FROM read_csv('{RAW / 'consoenaf' / 'conso_com.csv'}', header=true, all_varchar=false,
                  types={{'idcom': 'VARCHAR', 'iddep': 'VARCHAR', 'epci25': 'VARCHAR'}})
    WHERE iddep IN {tuple(DEPS)}
""")
con.execute(f"""
    CREATE TABLE logements AS
    SELECT CODGEO AS insee, TRY_CAST(P16_LOG AS DOUBLE) AS log16, TRY_CAST(P22_LOG AS DOUBLE) AS log22
    FROM read_csv('{RAW / 'insee' / 'base-cc-serie-historique-2022.CSV'}', delim=';', header=true,
                  types={{'CODGEO': 'VARCHAR'}})
""")
# Flux annuels 2021-2025 par commune, pour repérer une consommation tenant à un seul projet
dest = {"hab": "habitat", "act": "activité", "inc": "inconnue", "mix": "mixte", "rou": "route", "fer": "fer"}
flux = " UNION ALL ".join(
    f"""SELECT idcom AS insee, idcomtxt AS commune, '20{y}-20{y + 1}' AS periode, naf{y}art{y + 1} / 1e4 AS ha,
               CASE greatest({', '.join(f'coalesce(art{y}{k}{y + 1}, 0)' for k in dest)})
                    {' '.join(f"WHEN coalesce(art{y}{k}{y + 1}, 0) THEN '{v}'" for k, v in dest.items())} END AS destination
        FROM read_csv('{RAW / 'consoenaf' / 'conso_com.csv'}', header=true, types={{'idcom': 'VARCHAR', 'iddep': 'VARCHAR'}})
        WHERE iddep IN {tuple(DEPS)}""" for y in range(21, 25))
con.execute(f"CREATE TABLE flux AS {flux}")

n_sans = con.execute("SELECT count(*) FROM conso c LEFT JOIN geo g USING (insee) WHERE g.insee IS NULL").fetchone()[0]
n_log = con.execute("SELECT count(*) FROM conso c LEFT JOIN logements l USING (insee) WHERE l.insee IS NULL").fetchone()[0]
print(f"Communes Cerema : {con.execute('SELECT count(*) FROM conso').fetchone()[0]} ; "
      f"hors découpage geo.api : {n_sans} ; sans logements INSEE : {n_log}")

con.execute("""
    CREATE TABLE r AS
    WITH c AS (
        SELECT coalesce(g.epci_code, c.epci25) AS epci_code, c.*, l.log16, l.log22
        FROM conso c LEFT JOIN geo g USING (insee) LEFT JOIN logements l USING (insee)),
    noms AS (SELECT DISTINCT epci_code, epci_nom FROM geo WHERE epci_code IS NOT NULL)
    SELECT epci_code, any_value(n.epci_nom) AS epci_nom,
           sum(naf11art21) / 1e4 AS conso_ref_ha, sum(naf21art25) / 1e4 AS conso_2021_2025_ha,
           sum(art16hab22) / 1e4 AS conso_habitat_2016_2022_ha, sum(art16act22) / 1e4 AS conso_activite_2016_2022_ha,
           sum(log22) - sum(log16) AS delta_logements, sum(men22) - sum(men16) AS delta_menages,
           sum(pop22) - sum(pop16) AS delta_population, sum(emp22) - sum(emp16) AS delta_emplois,
           sum(pop22) AS population_2022, sum(surfcom2025) / 1e6 AS surface_km2
    FROM c LEFT JOIN noms n USING (epci_code) GROUP BY epci_code
""")
con.execute("""
    CREATE TABLE principal AS
    SELECT coalesce(g.epci_code, c.epci25) AS epci_code,
           arg_max(f.commune || ' ' || f.periode || ' : ' || round(f.ha, 1) || ' ha, ' || f.destination, f.ha) AS principal_flux_2021_2025,
           max(f.ha) AS ha_principal
    FROM flux f JOIN conso c USING (insee) LEFT JOIN geo g USING (insee) GROUP BY 1
""")
con.execute(f"""
    COPY (
    SELECT epci_code, epci_nom,
           round(conso_ref_ha, 1) AS conso_ref_ha, round(conso_2021_2025_ha, 1) AS conso_2021_2025_ha,
           round(conso_ref_ha / 10, 1) AS rythme_ref_ha_an, round(conso_2021_2025_ha / 4, 1) AS rythme_actuel_ha_an,
           round(conso_ref_ha / 2, 1) AS enveloppe_2021_2031_ha,
           round(100 * conso_2021_2025_ha / nullif(conso_ref_ha / 2, 0), 1) AS enveloppe_consommee_pct,
           round(100 * (conso_2021_2025_ha / 4 * 10) / nullif(conso_ref_ha / 2, 0), 1) AS projection_2031_pct,
           p.principal_flux_2021_2025,
           round(100 * p.ha_principal / nullif(conso_2021_2025_ha, 0), 1) AS part_principal_flux_pct,
           (p.ha_principal >= 20 AND p.ha_principal >= 0.5 * conso_2021_2025_ha) AS alerte_flux_unique,
           round(100 * ((conso_2021_2025_ha - p.ha_principal) / 4 * 10) / nullif(conso_ref_ha / 2, 0), 1)
               AS projection_2031_pct_hors_principal,
           round(conso_habitat_2016_2022_ha, 1) AS conso_habitat_2016_2022_ha,
           round(conso_activite_2016_2022_ha, 1) AS conso_activite_2016_2022_ha,
           round(delta_logements) AS delta_logements, round(delta_menages) AS delta_menages,
           round(delta_population) AS delta_population, round(delta_emplois) AS delta_emplois,
           round(CASE WHEN conso_habitat_2016_2022_ha >= 1 THEN delta_logements / conso_habitat_2016_2022_ha END, 1)
               AS logements_par_ha_habitat,
           round(CASE WHEN conso_activite_2016_2022_ha >= 1 THEN delta_emplois / conso_activite_2016_2022_ha END, 1)
               AS emplois_par_ha_activite,
           round(population_2022) AS population_2022, round(surface_km2, 1) AS surface_km2,
           round(population_2022 / nullif(surface_km2, 0), 1) AS densite_2022
    FROM r LEFT JOIN principal p USING (epci_code) ORDER BY epci_nom
    ) TO '{OUT}' (HEADER, DELIMITER ';')
""")
print(f"Écrit : {OUT}")
print("Normandie :", con.execute("""SELECT round(sum(conso_ref_ha)), round(sum(conso_2021_2025_ha)),
    round(100 * sum(conso_2021_2025_ha) / (sum(conso_ref_ha) / 2), 1), round(sum(delta_logements)),
    round(sum(delta_logements) / sum(conso_habitat_2016_2022_ha), 1), round(sum(delta_emplois)),
    round(sum(delta_emplois) / sum(conso_activite_2016_2022_ha), 1) FROM r""").fetchone(),
    "(réf. 2011-21 ha, 2021-25 ha, % enveloppe, Δ logements, logements/ha, Δ emplois, emplois/ha)")
