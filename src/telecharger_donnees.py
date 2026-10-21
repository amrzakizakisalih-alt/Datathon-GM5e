"""Télécharge toutes les données brutes du projet dans data/raw/.

Usage :
    python src/telecharger_donnees.py [--deps 14 27 50 61 76]

Le script est idempotent : un fichier déjà présent, à la bonne taille ou avec la bonne empreinte,
n'est pas retéléchargé. Il produit :
  data/raw/rpg_explorer/seq1524_dXX.gpkg, ref_fr_en.csv   RPG Explorer (INRAE, Etalab 2.0)
  data/raw/ocsge_artif/dXX/.../zan_evol_A0_A1_XX.gpkg     OCS GE Artificialisation, différentiel (IGN)
  data/raw/ocsge_artif/fenetres.csv                        fenêtre OCS GE et chemin de la couche par département
  data/raw/geo/communes_XX.geojson                         communes et EPCI (geo.api.gouv.fr)
  data/raw/geo/epci_departements.csv                       départements de chaque EPCI touchant la Normandie
Volume total : environ 650 Mo, dont 630 Mo pour RPG Explorer.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import urllib.request
from pathlib import Path

import py7zr

RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
NORMANDIE = ["14", "27", "50", "61", "76"]
DATAVERSE = "https://entrepot.recherche.data.gouv.fr"
DOI_RPG_EXPLORER = "doi:10.57745/6G0JTJ"
GEOPF = "https://data.geopf.fr/telechargement"
GEOAPI = "https://geo.api.gouv.fr"


def ouvrir(url, timeout):
    # data.geopf.fr refuse l'en-tête par défaut de urllib (HTTP 403)
    req = urllib.request.Request(url, headers={"User-Agent": "datathon-normandie-2026/1.0"})
    return urllib.request.urlopen(req, timeout=timeout)


def lire(url, timeout=120):
    with ouvrir(url, timeout) as r:
        return r.read()


def md5(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def telecharger(url, dest, taille=None, empreinte=None):
    """Télécharge url vers dest, sauf si dest existe déjà avec la bonne taille ou empreinte."""
    if dest.exists() and (taille is None or dest.stat().st_size == taille) \
            and (empreinte is None or md5(dest) == empreinte):
        print(f"  déjà là : {dest.relative_to(RACINE)}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    partiel = dest.with_name(dest.name + ".part")
    print(f"  télécharge : {dest.relative_to(RACINE)}")
    with ouvrir(url, 1800) as r, open(partiel, "wb") as f:
        shutil.copyfileobj(r, f, 1 << 20)
    if empreinte is not None and md5(partiel) != empreinte:
        partiel.unlink()
        raise RuntimeError(f"empreinte MD5 incorrecte pour {url}")
    partiel.replace(dest)


def rpg_explorer(deps):
    print("RPG Explorer (INRAE)")
    meta = json.loads(lire(f"{DATAVERSE}/api/datasets/:persistentId/?persistentId={DOI_RPG_EXPLORER}"))
    fichiers = {f["dataFile"]["filename"]: f["dataFile"] for f in meta["data"]["latestVersion"]["files"]}
    ref = fichiers["ref_fr_en.tab"]
    telecharger(f"{DATAVERSE}/api/access/datafile/{ref['id']}?format=original", RAW / "rpg_explorer" / "ref_fr_en.csv")
    for d in deps:
        f = fichiers[f"seq1524_d{d}.gpkg"]
        empreinte = (f.get("checksum") or {}).get("value") if (f.get("checksum") or {}).get("type") == "MD5" else None
        telecharger(f"{DATAVERSE}/api/access/datafile/{f['id']}", RAW / "rpg_explorer" / f"seq1524_d{d}.gpkg",
                    taille=f["filesize"], empreinte=empreinte)


def ocsge_artificialisation(deps):
    print("OCS GE Artificialisation, différentiel (IGN)")
    fenetres = []
    for d in deps:
        page = lire(f"{GEOPF}/resource/OCSGE-ARTIFICIALISATION?zone=D0{d}").decode("utf-8")
        noms = sorted(set(re.findall(
            rf"OCS-GE-ARTIFICIALISATION_2-0_DIFF-(\d{{4}})-(\d{{4}})_GPKG_LAMB93_D0{d}_(\d{{4}}-\d{{2}}-\d{{2}})", page)))
        if not noms:
            raise RuntimeError(f"aucune couche différentielle trouvée pour le département {d}")
        a0, a1, publie = max(noms, key=lambda n: (n[1], n[2]))  # fenêtre la plus récente, puis dernière publication
        nom = f"OCS-GE-ARTIFICIALISATION_2-0_DIFF-{a0}-{a1}_GPKG_LAMB93_D0{d}_{publie}"
        dossier = RAW / "ocsge_artif" / f"d{d}"
        couches = list(dossier.rglob(f"zan_evol_{a0}_{a1}_{int(d)}.gpkg"))
        if not couches:
            url = f"{GEOPF}/download/OCSGE-ARTIFICIALISATION/{nom}/{nom}"
            empreinte = lire(f"{url}.md5").decode("ascii").split()[0]
            archive = dossier / f"{nom}.7z"
            telecharger(f"{url}.7z", archive, empreinte=empreinte)
            with py7zr.SevenZipFile(archive) as z:
                z.extractall(dossier)
            couches = list(dossier.rglob(f"zan_evol_{a0}_{a1}_{int(d)}.gpkg"))
        else:
            print(f"  déjà là : {couches[0].relative_to(RACINE)}")
        fenetres.append({"dep": d, "debut": a0, "fin": a1, "couche": couches[0].relative_to(RACINE).as_posix()})
    with open(RAW / "ocsge_artif" / "fenetres.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["dep", "debut", "fin", "couche"], delimiter=";")
        w.writeheader()
        w.writerows(fenetres)
    for x in fenetres:
        print(f"  département {x['dep']} : fenêtre {x['debut']}-{x['fin']}")


def communes_et_epci(deps):
    print("Communes et EPCI (geo.api.gouv.fr)")
    for d in deps:
        url = f"{GEOAPI}/communes?codeDepartement={d}&fields=nom,code,codeEpci,epci,surface&format=geojson&geometry=contour"
        telecharger(url, RAW / "geo" / f"communes_{d}.geojson")
    epcis = json.loads(lire(f"{GEOAPI}/epcis?fields=nom,code,codesDepartements"))
    with open(RAW / "geo" / "epci_departements.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["epci_code", "epci_nom", "departements", "hors_normandie"])
        for e in epcis:
            ds = e.get("codesDepartements") or []
            if any(x in NORMANDIE for x in ds):
                w.writerow([e["code"], e["nom"], ",".join(ds), str(any(x not in NORMANDIE for x in ds))])
    print("  écrit : data/raw/geo/epci_departements.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--deps", nargs="+", default=NORMANDIE, help="codes des départements (défaut : les 5 normands)")
    deps = p.parse_args().deps
    communes_et_epci(deps)
    ocsge_artificialisation(deps)
    rpg_explorer(deps)
    print("Terminé.")
