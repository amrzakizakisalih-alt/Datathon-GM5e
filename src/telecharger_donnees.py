"""Télécharge toutes les données brutes du projet dans data/raw/.

Usage :
    python src/telecharger_donnees.py [--deps 14 27 50 61 76]

Le script est idempotent : un fichier déjà présent, à la bonne taille ou avec la bonne empreinte,
n'est pas retéléchargé. Il produit :
  data/raw/rpg_explorer/seq1524_dXX.gpkg, ref_fr_en.csv   RPG Explorer (INRAE, Etalab 2.0)
  data/raw/ocsge_artif/dXX/.../zan_evol_A0_A1_XX.gpkg     OCS GE Artificialisation, différentiel (IGN)
  data/raw/ocsge_artif/fenetres.csv                        fenêtre OCS GE et chemin de la couche par département
  data/raw/geo/communes_XX.geojson                         communes et EPCI (geo.api.gouv.fr)
  data/raw/geo/epci_departements.csv                       départements de chaque EPCI touchant la Normandie, et part
                                                           de sa surface et de sa population hors des 5 départements
  data/raw/zonages/{znieff1,znieff2,natura2000}.geojson    ZNIEFF et Natura 2000 (MNHN, via le WFS de l'IGN)
  data/raw/zones_humides/dataset/drealnorm_zh_s_r28.shp    inventaire régional des zones humides (DREAL Normandie)
  data/raw/mph/mph_normandie.tif                           milieux potentiellement humides, 50 m (INRAE, GéoSAS)
  data/raw/friches/friches_epfn.geojson                    observatoire des friches (EPF Normandie, Licence ouverte 2.0)
  data/raw/consoenaf/conso_com.csv                        consommation d'ENAF par commune 2011-2025 (Cerema)
  data/raw/insee/base-cc-serie-historique-2022.CSV         population et logements 2011-2016-2022 (INSEE)
Volume total : environ 950 Mo, dont 630 Mo pour RPG Explorer.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import urllib.request
import zipfile
from pathlib import Path

import py7zr

RACINE = Path(__file__).resolve().parent.parent
RAW = RACINE / "data" / "raw"
NORMANDIE = ["14", "27", "50", "61", "76"]
DATAVERSE = "https://entrepot.recherche.data.gouv.fr"
DOI_RPG_EXPLORER = "doi:10.57745/6G0JTJ"
GEOPF = "https://data.geopf.fr/telechargement"
GEOAPI = "https://geo.api.gouv.fr"
WFS_IGN = "https://data.geopf.fr/wfs/ows"
# Emprise de la Normandie en Lambert-93, avec une marge (xmin, ymin, xmax, ymax)
EMPRISE = (330000, 6780000, 640000, 7020000)
ZH_DREAL = ("https://atom.geo-ide.developpement-durable.gouv.fr/atomArchive/GetResource"
            "?id=be433f7d-cb7a-426a-92c5-491a6a155a62&dataType=dataset")
MPH_WCS = "https://geosas.fr/geoserver/wcs"
CONSOENAF = ("https://static.data.gouv.fr/resources/consommation-despaces-naturels-agricoles-et-forestiers-"
             "du-1er-janvier-2011-au-1er-janvier-2025/20260724-142909/conso-com.csv")
FRICHES_EPFN = ("https://www.datanormandie.fr/sites/default/files/dataset/412/06d61-8975-43cd-b6a0-2ce642c11e3a/"
                "observatoire_des_friches__donnees20260310.geojson")
FRICHES_DICO = ("https://www.datanormandie.fr/sites/default/files/dataset/412/06d61-8975-43cd-b6a0-2ce642c11e3a/"
                "r28_obsfriches_dictionnaire_variables_variables.csv")
INSEE_SERIES ="https://www.insee.fr/fr/statistiques/fichier/8582555/base-cc-serie-historique-2022_csv.zip"


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
        w.writerow(["epci_code", "epci_nom", "departements", "hors_normandie",
                    "part_hors_normandie_surface_pct", "part_hors_normandie_population_pct"])
        for e in epcis:
            ds = e.get("codesDepartements") or []
            if any(x in NORMANDIE for x in ds):
                hors = any(x not in NORMANDIE for x in ds)
                ps = pp = 0.0
                if hors:  # part de la surface et de la population de l'EPCI située hors des 5 départements
                    cs = json.loads(lire(f"{GEOAPI}/epcis/{e['code']}/communes?fields=surface,population,codeDepartement"))
                    dehors = [c for c in cs if c["codeDepartement"] not in NORMANDIE]
                    ps = 100 * sum(c.get("surface") or 0 for c in dehors) / sum(c.get("surface") or 0 for c in cs)
                    pp = 100 * sum(c.get("population") or 0 for c in dehors) / sum(c.get("population") or 0 for c in cs)
                w.writerow([e["code"], e["nom"], ",".join(ds), str(hors), round(ps, 1), round(pp, 1)])
    print("  écrit : data/raw/geo/epci_departements.csv")


def wfs_geojson(typenames, dest, pas=1000):
    """Télécharge une ou plusieurs couches WFS de l'IGN sur l'emprise normande, en Lambert-93, par pages."""
    if dest.exists():
        print(f"  déjà là : {dest.relative_to(RACINE)}")
        return
    bbox = ",".join(map(str, EMPRISE)) + ",urn:ogc:def:crs:EPSG::2154"
    objets = []
    for t in typenames:
        debut = 0
        while True:
            url = (f"{WFS_IGN}?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES={t}"
                   f"&SRSNAME=EPSG:2154&BBOX={bbox}&OUTPUTFORMAT=application/json&COUNT={pas}&STARTINDEX={debut}")
            page = json.loads(lire(url, timeout=300))["features"]
            for o in page:
                o["properties"]["couche"] = t
            objets += page
            if len(page) < pas:
                break
            debut += pas
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection",
                   "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::2154"}},
                   "features": objets}, f)
    print(f"  écrit : {dest.relative_to(RACINE)} ({len(objets)} objets)")


def zonages_et_milieux():
    print("ZNIEFF et Natura 2000 (MNHN, WFS IGN)")
    wfs_geojson(["patrinat_znieff1:znieff1"], RAW / "zonages" / "znieff1.geojson")
    wfs_geojson(["patrinat_znieff2:znieff2"], RAW / "zonages" / "znieff2.geojson")
    wfs_geojson(["patrinat_sic:sic", "patrinat_zps:zps"], RAW / "zonages" / "natura2000.geojson")

    print("Zones humides inventoriées (DREAL Normandie)")
    archive = RAW / "zones_humides" / "zh_normandie.zip"
    telecharger(ZH_DREAL, archive)
    if not (RAW / "zones_humides" / "dataset" / "drealnorm_zh_s_r28.shp").exists():
        with zipfile.ZipFile(archive) as z:
            z.extractall(RAW / "zones_humides")

    print("Milieux potentiellement humides (INRAE, GéoSAS)")
    x0, y0, x1, y1 = EMPRISE
    telecharger(f"{MPH_WCS}?service=WCS&version=2.0.1&request=GetCoverage&coverageId=mntsurf__mph_fr"
                f"&format=image/tiff&subset=X({x0},{x1})&subset=Y({y0},{y1})", RAW / "mph" / "mph_normandie.tif")

    print("Observatoire des friches (EPF Normandie, édition du 10/03/2026)")
    telecharger(FRICHES_EPFN, RAW / "friches" / "friches_epfn.geojson")
    telecharger(FRICHES_DICO, RAW / "friches" / "dictionnaire.csv")

    print("Consommation d'espaces (Cerema) et séries historiques (INSEE)")
    telecharger(CONSOENAF, RAW / "consoenaf" / "conso_com.csv")
    archive = RAW / "insee" / "serie_historique_2022.zip"
    telecharger(INSEE_SERIES, archive)
    if not (RAW / "insee" / "base-cc-serie-historique-2022.CSV").exists():
        with zipfile.ZipFile(archive) as z:
            z.extractall(RAW / "insee")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--deps", nargs="+", default=NORMANDIE, help="codes des départements (défaut : les 5 normands)")
    deps = p.parse_args().deps
    communes_et_epci(deps)
    ocsge_artificialisation(deps)
    zonages_et_milieux()
    rpg_explorer(deps)
    print("Terminé.")
