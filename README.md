# Ce que le béton et la charrue ont pris

Projet du Datathon Normandie 2026 (thème : biodiversité × activités humaines). Pour chacune des 71 intercommunalités (EPCI) normandes, l'outil mesure les prairies perdues sous le béton (artificialisation officielle de l'IGN) et sous la charrue (prairies permanentes retournées en culture, d'après le RPG). Toutes les données sont ouvertes.

Le chiffre principal porte sur les prairies anciennes, déclarées permanentes sans interruption depuis 2015. Compter toutes les prairies permanentes donne la borne haute, qui inclut des prairies semées dans une rotation.

Le descriptif du projet est dans `livrables/descriptif_projet.md`, les choix de méthode dans `docs/registre_choix_methodologiques.md`, et les comptes rendus détaillés dans `tests/`.

## Installation

Python 3.12 :

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Sous macOS ou Linux, remplacer `.venv\Scripts\python.exe` par `.venv/bin/python`.

## Lancer

```
.venv\Scripts\python.exe src\telecharger_donnees.py
.venv\Scripts\python.exe src\pipeline.py
```

- `telecharger_donnees.py` télécharge environ 950 Mo dans `data/raw/`. Il est idempotent : relancé, il saute ce qui est déjà là et vérifie les empreintes MD5 quand elles sont publiées. Sources :
  - RPG Explorer (INRAE) ;
  - OCS GE Artificialisation (IGN) ;
  - communes et EPCI (geo.api.gouv.fr) ;
  - ZNIEFF et Natura 2000 (MNHN, via l'IGN) ;
  - inventaire des zones humides (DREAL Normandie) ;
  - milieux potentiellement humides (INRAE) ;
  - observatoire des friches (EPF Normandie) ;
  - consommation d'espaces (Cerema) ;
  - séries historiques du recensement (INSEE).
- `pipeline.py` calcule tout en environ 6 minutes. Option `--deps 50` pour un seul département.

Pour justifier les choix :

- `src/sensibilite.py` : tests de sensibilité, résultats dans `data/processed/sensibilite.csv` ;
- `src/sensibilite_prl.py` : poids du code PRL dans la charrue, résultats dans `data/processed/sensibilite_prl.csv` ;
- `src/cohorte_epci.py` puis `src/trajectoires.py` : trajectoires du « Et si… », à lancer après les scripts de sensibilité (arguments dans leur en-tête) ;
- `src/validation_glmm.py` : comparaison avec un modèle hiérarchique bayésien, résultats dans `data/processed/glmm_validation.csv` ;
- `src/echantillon_validation.py`, `src/preparer_lecture.py` et `src/resultat_validation.py` : vérification sur photo aérienne, à usage interne, avec la page `data/validation/lecture.html` (protocole dans `data/validation/LISEZ-MOI.md`) ;
- `docs/registre_choix_methodologiques.md` : registre de tous les choix, avec leurs preuves.

Pour l'interface : `src/export_web.py` produit les fichiers légers de `web/data/`, décrits dans `web/data/LISEZ-MOI.md` (à lancer après les scripts de sensibilité et `src/trajectoires.py`).

## Voir l'interface

Le site est statique, sans dépendance, sans étape de construction et sans service extérieur (les polices sont dans `web/polices/`). Il doit être servi par un serveur, même local :

```
.venv\Scripts\python.exe -m http.server 8770 --directory web
```

Puis ouvrir http://localhost:8770. Pour le publier, déposer le dossier `web/` chez un hébergeur statique qui compresse les fichiers.

L'interface tient en un écran : six modules dans la barre de gauche (synthèse, prairies, béton et foncier, trajectoires, friches, méthode), un panneau de chiffres pour la Normandie, la carte des 71 intercommunalités au centre, et la fiche d'un territoire qui s'ouvre à droite au clic. Le territoire, le module et les filtres choisis sont dans l'adresse de la page : un lien copié rouvre la même vue.

| Fichier de `web/` | Rôle |
| --- | --- |
| `index.html` | La page et la logique propre à l'interface (modules, panneaux, friches) |
| `commun.js` | Chargement des données, état dans l'adresse, carte, graphiques, tableaux, blocs de chiffres |
| `commun.css`, `d.css` | Composants de base, puis identité visuelle |
| `reperes.json` | Centre de 28 villes, pour se situer sur la carte |
| `data/` | Données produites par `src/export_web.py` |

## Résultats (`data/processed/`)

| Fichier | Contenu |
| --- | --- |
| `retournements_epci_XX.csv` | Charrue : une ligne par EPCI et par an (2016 = retournement entre 2015 et 2016) |
| `beton_charrue_epci_XX.csv` | Béton + charrue sur la fenêtre OCS GE du département |
| `qualite_epci_XX.csv` | Bloc D : béton et charrue en zones boisées, ZNIEFF, Natura 2000, zones humides inventoriées et potentielles |
| `sobriete_epci.csv` | Bloc E : trajectoire ZAN, logements et emplois créés par hectare consommé |
| `friches.csv` | Écran 2 : une ligne par friche (critères écologiques, scores, classe, raisons, vigilance), sans le nom de la friche ; colonnes décrites en tête de `src/friches.py` |
| `friches_epci.csv` | Écran 2 : synthèse des friches par EPCI |
| `tableau_regional_epci.csv` | Les 71 EPCI en ha par an, blocs D et E, profil de comparaison (bloc F) et synthèse des friches. Colonnes décrites en tête de `src/tableau_regional.py`, `src/qualite_epci.py` et `src/sobriete_epci.py` |
| `cohorte_epci.csv` | Prairies anciennes par EPCI et par an : stock, labour, labour en zones fragiles. Colonnes décrites en tête de `src/cohorte_epci.py` |
| `trajectoires_epci.csv` | « Et si… » : trois trajectoires pour les prairies (2035) et le foncier (2031), par EPCI et pour la Normandie. Méthode en tête de `src/trajectoires.py` |
| `trajectoires_annuelles.csv` | Labour cumulé année par année, avec sa fourchette, pour tracer les courbes |
| `trajectoires_validation.csv` | Épreuves sur le passé et tests de sensibilité des trajectoires |

## Organisation

```
contexte/        documents des organisateurs
reports/         rapports de recherche (données, méthodes)
research_notes/  notes derrière ces rapports
tests/           comptes rendus datés des tests T1 à T10 (leurs chiffres sont ceux du jour du test)
src/             code (DuckDB + extension spatiale)
data/raw/        données brutes, non versionnées
data/processed/  résultats CSV, séparateur ;
data/validation/ vérification sur photo aérienne, à usage interne : jamais livré ni publié
web/             le site
docs/            registre des choix méthodologiques
livrables/       descriptif du projet et archive à remettre
archives/        versions antérieures de l'interface
```

Code sous licence MIT, données calculées sous Licence Ouverte 2.0 : voir `LICENCE`.

## Règles

- Ne jamais afficher de parcelle ni nommer d'exploitation : on affiche à l'EPCI.
- Ne livrer que des agrégats : jamais la table des parcelles.
- Citer les sources : « RPG Explorer, INRAE / AgroParisTech (Girault & Martin), d'après le RPG IGN-ASP, Licence Etalab 2.0 » et « OCS GE Artificialisation, IGN ».
