"""Analyse de sensibilité : la charrue et le classement des EPCI dépendent-ils des anomalies de la PAC ?

Usage :
    python src/sensibilite_anomalies.py <dossier data/processed> <sortie.csv>

Complète sensibilite.py (seuils, poids, rayons) et sensibilite_prl.py (prairies en rotation longue).
Deux anomalies connues du RPG peuvent fausser la charrue :
  - 2018 : 84 000 ha de prairies temporaires passent en permanentes (reclassement probable). Ces
    « jeunes PP » gonflent le stock, et sont labourées en nombre l'année suivante (pic de 2019) ;
  - 2023 : 30 000 ha de prairies déclarées en 2022 ne le sont plus en 2023 (refonte du RPG). Leurs
    retournements des passages 2022->2023 et 2023->2024 sont invisibles.
On recalcule la charrue moyenne de chaque EPCI (ha/an, et % du stock de PP 2015 par an) selon cinq scénarios :
  reference          les 9 passages 2015->2024, toutes PP (le chiffre du tableau régional)
  sans_2018          sans le passage 2017->2018
  sans_2019          sans le passage 2018->2019, celui du pic dû au reclassement de 2018
  sans_2023_2024     sans les passages 2022->2023 et 2023->2024
  anciennes          les 9 passages, PP anciennes seulement (PP chaque année depuis 2015) : insensible au
                     reclassement de 2018 par construction
Pour chaque scénario, on compare le classement des EPCI (taux de charrue en % du stock) à celui de référence :
  spearman           corrélation de rang (1 = même classement ; ex aequo au rang moyen)
  ecart_rang_max     plus grand déplacement d'un EPCI dans le classement
  n_deplaces_5       EPCI déplacés de plus de 5 rangs
  top10_commun       EPCI communs aux 10 premiers des deux classements
Les EPCI exclus des comparaisons (moins de la moitié de leur surface en Normandie) sont écartés.
Sortie : une ligne par EPCI, avec la charrue et le rang de chaque scénario. Le résumé est affiché.
"""
import sys

import duckdb

DIR, OUT = sys.argv[1:3]
SCENARIOS = {  # nom -> (colonne de retournements_epci, années d'arrivée exclues)
    "reference": ("strict_toutes", ()),
    "sans_2018": ("strict_toutes", (2018,)),
    "sans_2019": ("strict_toutes", (2019,)),
    "sans_2023_2024": ("strict_toutes", (2023, 2024)),
    "anciennes": ("strict_anciennes", ()),
}

con = duckdb.connect()
con.execute(f"""CREATE TABLE ret AS SELECT CAST(epci_code AS VARCHAR) AS epci_code, * EXCLUDE (epci_code)
                FROM read_csv_auto('{DIR}/retournements_epci_*.csv', delim=';', header=true)""")
con.execute(f"""CREATE TABLE t AS SELECT CAST(epci_code AS VARCHAR) AS epci_code, epci_nom, exclu_comparaisons
                FROM read_csv_auto('{DIR}/tableau_regional_epci.csv', delim=';', header=true)""")

cols = []
for nom, (col, exclues) in SCENARIOS.items():
    filtre = f"annee NOT IN {tuple(exclues) + (0,)}"
    n = 9 - len(exclues)
    cols.append(f"sum({col}) FILTER (WHERE {filtre}) / {n} AS charrue_{nom}_ha_an")
con.execute(f"""
    CREATE TABLE s AS
    SELECT epci_code, sum(stock_pp) FILTER (WHERE annee = 2016) AS stock_pp_2015, {', '.join(cols)}
    FROM ret GROUP BY epci_code
""")
taux = ", ".join(f"100 * charrue_{n}_ha_an / nullif(stock_pp_2015, 0) AS taux_{n}" for n in SCENARIOS)
# rang « fractionnel » : les ex aequo reçoivent la moyenne de leurs rangs, comme dans la définition de Spearman
rangs = ", ".join(f"rank() OVER (ORDER BY taux_{n} DESC) + (count(*) OVER (PARTITION BY taux_{n}) - 1) / 2.0 AS rang_{n}"
                  for n in SCENARIOS)
con.execute(f"""
    CREATE TABLE r AS
    WITH x AS (SELECT s.*, t.epci_nom, {taux} FROM s JOIN t USING (epci_code)
               WHERE NOT t.exclu_comparaisons AND stock_pp_2015 > 0)
    SELECT *, {rangs} FROM x
""")

print("Scénario | charrue Normandie (ha/an) | écart à la référence | spearman | écart de rang max | "
      "EPCI déplacés > 5 rangs | top 10 commun")
ref_total = con.execute("SELECT sum(charrue_reference_ha_an) FROM r").fetchone()[0]
for n in SCENARIOS:
    total, rho, emax, n5 = con.execute(f"""
        SELECT sum(charrue_{n}_ha_an), corr(rang_{n}, rang_reference), max(abs(rang_{n} - rang_reference)),
               count(*) FILTER (WHERE abs(rang_{n} - rang_reference) > 5) FROM r""").fetchone()
    top = con.execute(f"""SELECT count(*) FROM r WHERE rang_{n} <= 10 AND rang_reference <= 10""").fetchone()[0]
    print(f"{n} | {total:,.0f} | {100 * (total - ref_total) / ref_total:+.1f} % | {rho:.3f} | {emax:g} | {n5} | {top}/10")

arrondis = ", ".join(f"round(charrue_{n}_ha_an, 1) AS charrue_{n}_ha_an, round(taux_{n}, 3) AS taux_{n}_pct, rang_{n}"
                     for n in SCENARIOS)
con.execute(f"""COPY (SELECT epci_code, epci_nom, round(stock_pp_2015) AS stock_pp_2015, {arrondis}
                      FROM r ORDER BY rang_reference) TO '{OUT}' (HEADER, DELIMITER ';')""")
print(f"Écrit : {OUT}")
