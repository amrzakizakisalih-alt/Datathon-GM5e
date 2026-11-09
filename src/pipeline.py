"""Enchaîne tout le calcul : charrue et béton par département, tableau régional, sensibilités, export web.

Usage :
    python src/pipeline.py [--deps 14 27 50 61 76]

Prérequis : python src/telecharger_donnees.py (il écrit data/raw/ocsge_artif/fenetres.csv).
Sorties dans data/processed/ :
  retournements_epci_XX.csv   charrue, une ligne par EPCI et par an
  beton_charrue_epci_XX.csv   béton + charrue sur la fenêtre OCS GE du département
  qualite_epci_XX.csv         bloc D : béton et charrue en milieux remarquables
  sobriete_epci.csv           bloc E : trajectoire ZAN et efficacité
  friches.csv                 écran 2 : une ligne par friche (critères, scores, classe, raisons)
  friches_epci.csv            écran 2 : synthèse des friches par EPCI
  tableau_regional_epci.csv   les 71 EPCI, en ha par an, avec les blocs D, E et le profil (bloc F)
  sensibilite_anomalies_epci.csv  charrue et classement des EPCI avec et sans les anomalies de la PAC (2018, 2019, 2023)
  sensibilite.csv             effet des seuils, poids et rayons (profils, friches, zones humides)
  sensibilite_prl.csv, sensibilite_prl_epci.csv   poids des prairies en rotation longue (PRL)
Puis export_web.py écrit les fichiers du site dans web/data/.
"""
import argparse
import csv
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
OUT = RACINE / "data" / "processed"
SRC = RACINE / "src"


def lancer(script, *args):
    subprocess.run([sys.executable, str(SRC / script), *map(str, args)], check=True, cwd=RACINE)


if __name__ == "__main__":
    with open(RAW / "ocsge_artif" / "fenetres.csv", encoding="utf-8") as f:
        fenetres = {x["dep"]: x for x in csv.DictReader(f, delimiter=";")}
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--deps", nargs="+", default=sorted(fenetres), help="codes des départements (défaut : tous)")
    deps = p.parse_args().deps

    OUT.mkdir(parents=True, exist_ok=True)
    ref = RAW / "rpg_explorer" / "ref_fr_en.csv"
    for d in deps:
        fw = fenetres[d]
        rpg, communes = RAW / "rpg_explorer" / f"seq1524_d{d}.gpkg", RAW / "geo"  # le dossier : les scripts chargent les 5 départements
        print(f"===== département {d} (fenêtre OCS GE {fw['debut']}-{fw['fin']})", flush=True)
        lancer("retournements_epci.py", rpg, ref, communes, OUT / f"retournements_epci_{d}.csv")
        lancer("beton_charrue_epci.py", RACINE / fw["couche"], fw["debut"], fw["fin"], rpg, ref, communes,
               OUT / f"beton_charrue_epci_{d}.csv")
        lancer("qualite_epci.py", d, OUT / f"qualite_epci_{d}.csv")
    print("===== trajectoire ZAN et efficacité", flush=True)
    lancer("sobriete_epci.py", OUT / "sobriete_epci.csv")
    print("===== friches (écran 2)", flush=True)
    lancer("friches.py", OUT / "friches.csv", OUT / "friches_epci.csv")
    print("===== tableau régional", flush=True)
    lancer("tableau_regional.py", OUT.as_posix(), (RAW / "geo" / "epci_departements.csv").as_posix(),
           (OUT / "tableau_regional_epci.csv").as_posix())
    print("===== analyses de sensibilité", flush=True)
    lancer("sensibilite_anomalies.py", OUT.as_posix(), (OUT / "sensibilite_anomalies_epci.csv").as_posix())
    lancer("sensibilite.py")
    lancer("sensibilite_prl.py")
    print("===== export pour le site", flush=True)
    lancer("export_web.py")
