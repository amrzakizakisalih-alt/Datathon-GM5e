# T6 : tableau régional « béton + charrue » par EPCI (Normandie, ha/an)

> Note du 10/11/2026 : dans ce compte rendu, la perte « en % du stock par an » divise par le stock de 2015. Elle est désormais rapportée au stock du début de la fenêtre OCS GE (voir le registre, section 4) : les valeurs ci-dessous sont plus hautes que celles de l'outil. Le chiffre principal et le classement portent désormais sur les prairies anciennes (registre, section 2) : l'ordre des EPCI ci-dessous n'est plus celui de l'outil.

Date : 18/10/2026. Résultat : **tableau des 71 EPCI produit.** Fichier : `data/processed/tableau_regional_epci.csv` (séparateur `;`).

## Chaîne de calcul (reproductible)

```
# pour chaque département XX ∈ {14, 27, 50, 61, 76}, fenêtre OCS GE A0-A1 :
.venv\Scripts\python.exe src\retournements_epci.py  data\raw\rpg_explorer\seq1524_dXX.gpkg data\raw\rpg_explorer\ref_fr_en.csv data\raw\geo\communes_XX.geojson data\processed\retournements_epci_XX.csv
.venv\Scripts\python.exe src\beton_charrue_epci.py <zan_evol_A0_A1_XX.gpkg> A0 A1 data\raw\rpg_explorer\seq1524_dXX.gpkg data\raw\rpg_explorer\ref_fr_en.csv data\raw\geo\communes_XX.geojson data\processed\beton_charrue_epci_XX.csv
# puis :
.venv\Scripts\python.exe src\tableau_regional.py data/processed data/raw/geo/epci_departements.csv data/processed/tableau_regional_epci.csv
```

**Fenêtres OCS GE (artificialisation officielle de l'IGN) :**
- 2019-2022 pour l'Eure, la Manche et la Seine-Maritime ;
- 2020-2023 pour le Calvados et l'Orne ;
- « mixte » pour un seul EPCI, la CC du Pays de Honfleur-Beuzeville (Calvados et Eure).

Chaque partie départementale est annualisée sur sa propre fenêtre avant d'être additionnée.

**Sources :**
- RPG Explorer (INRAE / AgroParisTech, Etalab 2.0) ;
- OCS GE Artificialisation, différentiel (IGN) ;
- contours et EPCI : geo.api.gouv.fr.

**Durée de calcul :** quelques secondes par département.

## Totaux Normandie

| Indicateur | Valeur |
|---|---|
| Prairies permanentes déclarées en 2015 (RPG) | 598 752 ha |
| Charrue, toutes PP, moyenne 2015→2024 | **8 226 ha/an** |
| Charrue, PP anciennes, moyenne 2015→2024 | **4 961 ha/an** |
| Béton total (artificialisation IGN) | **1 374 ha/an** |
| … dont sur des PP déclarées | **210 ha/an** |
| … dont hors des parcelles déclarées à la PAC | 907 ha/an |
| Désartificialisation (IGN) | 271 ha/an |
| Charrue sur la fenêtre OCS GE, nette du béton | 9 752 ha/an |
| Prairies permanentes perdues sur la fenêtre (béton + charrue) | 9 963 ha/an |
| **Part du béton dans les pertes de PP** | **2,1 %** |

## Les 15 EPCI qui perdent le plus de prairies permanentes (fenêtre OCS GE, ha/an)

| EPCI | Dép. | Stock PP 2015 | Charrue PP anciennes (moy. 2015-24) | Béton total | Béton sur PP | Désartif. | Charrue (fenêtre) | Perdues | Part béton | Perte, % du stock par an |
|---|---|---|---|---|---|---|---|---|---|---|
| CA Mont-Saint-Michel-Normandie | 50 | 28 678 | 258 | 67,5 | 11,8 | 17,0 | 1 101 | 1 113 | 1,1 % | 3,9 |
| CA du Cotentin | 50 | 41 469 | 314 | 65,9 | 18,6 | 6,6 | 806 | 825 | 2,3 % | 2,0 |
| CC Intercom de la Vire au Noireau | 14 | 18 914 | 235 | 22,3 | 6,7 | 6,5 | 590 | 597 | 1,1 % | 3,2 |
| CA Saint-Lô Agglo | 50 | 26 321 | 228 | 31,3 | 9,6 | 4,3 | 506 | 515 | 1,9 % | 2,0 |
| CC Coutances Mer et Bocage | 50 | 21 392 | 213 | 27,7 | 6,5 | 3,9 | 390 | 397 | 1,6 % | 1,9 |
| CA Flers Agglo | 61 | 14 506 | 172 | 12,3 | 3,8 | 3,4 | 384 | 388 | 1,0 % | 2,7 |
| CC Isigny-Omaha Intercom | 14 | 20 189 | 165 | 21,0 | 5,8 | 3,4 | 310 | 315 | 1,8 % | 1,6 |
| CC Andaine - Passais | 61 | 8 100 | 117 | 7,4 | 2,5 | 1,2 | 303 | 305 | 0,8 % | 3,8 |
| CC Côte Ouest Centre Manche | 50 | 13 107 | 92 | 17,5 | 2,9 | 2,1 | 295 | 298 | 1,0 % | 2,3 |
| CC Domfront Tinchebray Interco | 61 | 10 030 | 112 | 7,6 | 2,8 | 1,6 | 246 | 249 | 1,1 % | 2,5 |
| CC de la Baie du Cotentin | 50 | 23 031 | 114 | 12,2 | 5,6 | 0,8 | 227 | 233 | 2,4 % | 1,0 |
| CC de Villedieu Intercom | 50 | 9 325 | 77 | 11,4 | 5,1 | 0,9 | 223 | 228 | 2,2 % | 2,5 |
| CA Lisieux Normandie | 14 | 33 840 | 134 | 30,0 | 6,0 | 5,4 | 219 | 225 | 2,7 % | 0,7 |
| CC Lieuvin Pays d'Auge | 27 | 8 936 | 140 | 17,2 | 3,1 | 1,7 | 210 | 213 | 1,5 % | 2,4 |
| CC Terres d'Argentan Interco | 61 | 18 897 | 127 | 21,9 | 3,4 | 2,4 | 188 | 192 | 1,8 % | 1,0 |

**Là où le béton pèse le plus**, parmi les EPCI qui perdent au moins 20 ha/an :

| EPCI | Prairies perdues (ha/an) | Part du béton |
|---|---|---|
| CU Caen la Mer | 28,5 | **19,8 %** |
| CC de Bayeux Intercom | 55,0 | 7,6 % |
| CU Le Havre Seine Métropole | 71,0 | 7,4 % |
| CC Normandie-Cabourg-Pays d'Auge | 30,5 | 7,1 % |
| CA Fécamp Caux Littoral | 28,4 | 6,7 % |
| Métropole Rouen Normandie | 48,3 | 6,6 % |

**Béton total le plus élevé (ha/an) :**
- CU Caen la Mer : 117,6, dont 68,4 hors des parcelles déclarées à la PAC ;
- CU Le Havre Seine Métropole : 74,3 ;
- Métropole Rouen Normandie : 72,9 ;
- CA Mont-Saint-Michel-Normandie : 67,5 ;
- CA du Cotentin : 65,9.

## Premières lectures (à confirmer)

- **Partout, la charrue domine les pertes de prairies permanentes.** Le béton en représente 2,1 % en moyenne régionale, et au plus environ 20 % dans l'agglomération de Caen.
- **L'ordre de grandeur est plausible :**
  - 4 961 à 8 226 ha/an retournés, contre 6 000 à 8 000 ha/an estimés d'après la DRAAF Grand Est ;
  - 1 374 ha/an artificialisés, cohérent avec une consommation d'espaces d'environ 2 000 ha/an (la consommation au sens des fichiers fonciers est plus large que l'artificialisation).
- **Une géographie nette :**
  - **le bocage de l'ouest** (sud Manche, Bocage virois, Domfrontais, Andaine) perd 2,5 à 3,9 % de son stock de prairies permanentes par an ;
  - **le Pays d'Auge** (Côte Fleurie, Cabourg, Terre d'Auge, Lisieux) perd moins de 0,7 % par an ;
  - **les métropoles** ont peu de prairies, mais la part du béton y est la plus forte.

## Réserves à afficher

1. **Les années 2019 et 2023 sont touchées par des artefacts RPG** (voir T2). Les fenêtres OCS GE, de 2019 à 2023, tombent juste après le reclassement de 2018. La « charrue sur la fenêtre » (9 752 ha/an) dépasse donc la moyenne 2015-2024 (8 226 ha/an). Pour le chiffre principal, préférer « PP anciennes » ou la moyenne 2015-2024.
2. **L'Orne a une désartificialisation anormalement élevée** : 284 ha sur 2020-2023, pour 394 ha artificialisés. C'est peut-être une correction de photo-interprétation dans l'OCS GE. À examiner avant de l'afficher.
3. **Six EPCI débordent hors de Normandie** : CA du Pays de Dreux, CC Normandie Sud Eure, CC Aumale-Blangy-sur-Bresle, CC Maine Saosnois, CU d'Alençon, CC des Villes Sœurs. Leurs chiffres ne couvrent que la partie normande (colonne `hors_normandie`).
4. **Environ 1 % des parcelles RPG ne sont rattachées à aucune commune** : 2 224 LCP, soit environ 6 800 ha, situées sur le littoral ou les limites départementales, à cause des contours simplifiés de geo.api. À corriger avec les contours ADMIN EXPRESS ou un rattachement à la commune la plus proche.
5. **Le béton hors des parcelles déclarées** (907 ha/an) contient de l'herbe non déclarée à la PAC, probablement des prairies. La part du béton dans les pertes de prairies est donc une **borne basse**. Il faudra afficher une fourchette, comme pour la Manche (T5).
6. **2025 n'est pas traité**, car RPG Explorer s'arrête en 2024.
