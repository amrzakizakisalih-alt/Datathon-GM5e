"""Prépare la lecture à l'aveugle : télécharge les photos IGN de chaque point et écrit les données de la page.

Usage :
    python src/preparer_lecture.py

À lancer après echantillon_validation.py. Écrit dans data/validation/ :
  - images/Pxxx_avant.jpg et Pxxx_apres.jpg : photos de la mosaïque 2016-2020 et de la mosaïque 2021-2023, cadrées sur la parcelle ;
  - points_lecture.js : pour chaque point, un code, les dates des photos et le contour, sans type, strate, code de culture ni département ;
  - cle_codes.csv : la correspondance code / numéro, lue seulement par resultat_validation.py.
Relancé, il saute les images déjà présentes. Usage interne : ces fichiers localisent des parcelles agricoles.
"""
import csv
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import rasterio
from rasterio.errors import NotGeoreferencedWarning
import warnings

RACINE = Path(__file__).resolve().parent.parent
VAL = RACINE / "data" / "validation"
IMG = VAL / "images"
WMS = "https://data.geopf.fr/wms-r/wms"
UA = {"User-Agent": "datathon-normandie-validation/1.0"}
COUCHES = {"avant": "ORTHOIMAGERY.ORTHOPHOTOS2016-2020", "apres": "ORTHOIMAGERY.ORTHOPHOTOS2021-2023"}
PIXELS, COTE_MIN, MARGE = 800, 300, 1.5
N_COMMUNS = {"retournement détecté": 4, "prairie maintenue": 2}  # points lus par tous les lecteurs, par département
GRAINE = "datathon-2026"
sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)
IMG.mkdir(parents=True, exist_ok=True)


def empreinte(texte):
    return hashlib.md5(f"{texte}{GRAINE}".encode()).hexdigest()


def anneaux(wkt):
    return [[tuple(map(float, c.split())) for c in a.split(",")] for a in re.findall(r"\(([^()]+)\)", wkt)]


def telecharger(couche, bbox, chemin):
    if chemin.exists():
        return True
    p = {"SERVICE": "WMS", "VERSION": "1.3.0", "REQUEST": "GetMap", "LAYERS": couche, "STYLES": "", "CRS": "EPSG:2154",
         "BBOX": ",".join(f"{v:.2f}" for v in bbox), "WIDTH": PIXELS, "HEIGHT": PIXELS, "FORMAT": "image/jpeg"}
    for essai in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(WMS + "?" + urllib.parse.urlencode(p), headers=UA), timeout=90) as f:
                b, ct = f.read(), f.headers.get("Content-Type", "")
            if "image" in ct:
                with rasterio.io.MemoryFile(b) as m, m.open() as s:
                    a = s.read()
                if float((a.max(axis=0) > 10).mean()) < 0.5 or float(np.std(a)) < 2:
                    print(f"Image vide : {chemin.name}")
                    return False
                chemin.write_bytes(b)
                return True
        except Exception:
            pass
        time.sleep(2 * (essai + 1))
    print(f"Échec : {chemin.name}")
    return False


lignes = list(csv.DictReader(open(VAL / "echantillon_retournements.csv", encoding="utf-8"), delimiter=";"))
lignes.sort(key=lambda r: empreinte(r["num"]))
for i, r in enumerate(lignes, 1):
    r["code"] = f"P{i:03d}"
vus = {}
points, taches = [], []
for r in lignes:
    cle = (r["dep"], r["type"])
    vus[cle] = vus.get(cle, 0) + 1
    xy = [c for a in anneaux(r["wkt"]) for c in a]
    xs, ys = [c[0] for c in xy], [c[1] for c in xy]
    cote = max(COTE_MIN, MARGE * max(max(xs) - min(xs), max(ys) - min(ys)))
    x0, y0 = (min(xs) + max(xs) - cote) / 2, (min(ys) + max(ys) - cote) / 2
    bbox = (x0, y0, x0 + cote, y0 + cote)
    points.append({"code": r["code"], "commun": vus[cle] <= N_COMMUNS[r["type"]], "date_avant": r["date_photo_avant"], "date_apres": r["date_photo_apres"],
                   "lat": float(r["lat"]), "lon": float(r["lon"]), "cote_m": round(cote),
                   "contour": [[[round((x - x0) / cote, 4), round(1 - (y - y0) / cote, 4)] for x, y in a] for a in anneaux(r["wkt"])]})
    for periode, couche in COUCHES.items():
        taches.append((couche, bbox, IMG / f"{r['code']}_{periode}.jpg"))

with ThreadPoolExecutor(2) as ex:
    ok = list(ex.map(lambda t: telecharger(*t), taches))
print(f"Images : {sum(ok)} / {len(ok)}")

points.sort(key=lambda p: p["code"])
(VAL / "points_lecture.js").write_text("const POINTS = " + json.dumps(points, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
with open(VAL / "cle_codes.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["code", "num"])
    w.writerows((r["code"], r["num"]) for r in lignes)
print(f"Écrit : {VAL / 'points_lecture.js'} ({len(points)} points, {sum(p['commun'] for p in points)} communs)")
