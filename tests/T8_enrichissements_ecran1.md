# T8 : enrichissements de l'écran 1 (blocs D, E et F)

> Note du 10/11/2026 : le béton en milieux potentiellement humides de ce compte rendu est surestimé (343 ha/an, 25 % du béton). Après correction du calcul, il vaut 291 ha/an, soit 21 % du béton, pour une enveloppe qui couvre 22 % de la région. Rouen passe de 53 à 48 %, Seine-Eure de 49 à 38 %, Mont-Saint-Michel-Normandie de 40 à 31 % ; Le Havre reste à 48 %. Voir le registre, section 5.

Date : 01/11/2026. Résultat : **les trois blocs sont calculés pour les 71 EPCI** et intégrés au tableau régional (`data/processed/tableau_regional_epci.csv`, 59 colonnes). La chaîne complète (`src/telecharger_donnees.py` puis `src/pipeline.py`) tourne en environ 4 minutes.

## Nouvelles sources (toutes ouvertes, téléchargées par `src/telecharger_donnees.py`)

| Source | Producteur | Contenu utilisé | Licence | Volume |
|---|---|---|---|---|
| ZNIEFF de types 1 et 2, Natura 2000 (SIC + ZPS) | MNHN, via le WFS de l'IGN | Périmètres : 2 557 ZNIEFF 1, 306 ZNIEFF 2, 151 sites Natura 2000 sur l'emprise | Licence ouverte | 55 Mo (GeoJSON) |
| Inventaire des zones humides de Normandie | DREAL Normandie | 326 000 polygones, 263 500 ha (dont 102 000 ha de prairies humides), terrain et photo-interprétation | Licence ouverte 2.0 | 113 Mo (zip) |
| Milieux potentiellement humides (MPH) | INRAE / Institut Agro (GéoSAS, service WCS) | Raster 50 m, classes de confiance 1 à 3 au sein de l'enveloppe ; 51 et 522 = plans d'eau et estrans, exclus | Licence ouverte | 65 Mo (GeoTIFF) |
| Consommation d'ENAF 2011-2025 | Cerema (fichiers fonciers) | Par commune : flux annuels par destination (habitat, activité…), population, ménages et emplois INSEE 2011, 2016, 2022 | Licence ouverte | 31 Mo (CSV) |
| Séries historiques du recensement (édition 2022) | INSEE | Logements par commune en 2016 et 2022 | Licence ouverte | 6 Mo (zip) |

**Deux sources écartées :**
- **Carte nationale des haies (IGN) :** son édition de mars 2026 montre les haies d'aujourd'hui, pas celles détruites par le béton entre 2019 et 2023. Elle ne permet donc pas de mesurer des « km de haies bétonnées ». Elle est remplacée par la couverture boisée d'avant le béton, lue dans l'OCS GE (CS2.1.x : bois, bosquets, haies larges).
- **Emplois Urssaf :** inutiles, puisque le fichier du Cerema contient déjà les emplois de l'INSEE au lieu de travail, tous secteurs confondus, alors que l'Urssaf ne couvre que le privé.

## Nouveaux scripts

- **`src/qualite_epci.py <dep> <sortie>`, bloc D, par département.**
  - **Béton :** intersection des polygones artificialisés avec chaque zonage. Les zones qui se superposent sont fusionnées pour ne rien compter deux fois. Pour les MPH, on prend la part des pixels du polygone ; pour un polygone plus petit qu'un pixel, son point intérieur.
  - **Charrue :** une parcelle (LCP) est comptée dans une zone si son point intérieur y tombe. La définition est la même que dans `retournements_epci.py` : retournements stricts, toutes PP et prairies anciennes, cumulés sur 2015→2024.
- **`src/sobriete_epci.py <sortie>`, bloc E, régional.**
  - **Communes :** les 2 644 communes normandes du Cerema sont toutes rattachées à un EPCI et ont toutes leurs logements INSEE.
- **`src/tableau_regional.py`, bloc F et assemblage.** Il annualise le bloc D (le béton sur la fenêtre OCS GE, la charrue sur 9 ans), joint le bloc E et calcule le profil et la comparaison.

## Bloc D : ce que le béton et la charrue ont pris (Normandie, ha par an)

| Milieu | Béton | Charrue, toutes PP | Charrue, prairies anciennes |
|---|---|---|---|
| Total (rappel) | 1 374 | 8 246 | 4 970 |
| Milieux potentiellement humides (MPH) | **343** (25 % du béton) | **1 475** (18 % de la charrue) | 861 |
| Zones humides inventoriées (DREAL) | 57 (4 %) | **389** (5 %) | 262 |
| Natura 2000 | 30 | 161 | 121 |
| ZNIEFF de type 1 | 13 | 45 | — |
| ZNIEFF de type 2 | 91 | — | — |
| Couverture boisée avant béton (OCS GE) | 133 | — | — |

**Lectures (à confirmer) :**
- **Un quart du béton se pose sur des milieux potentiellement humides**, surtout autour des grandes agglomérations de vallée :
  - Rouen : 53 % de son béton, soit 39 ha/an ;
  - Le Havre : 48 % ;
  - Seine-Eure : 49 % ;
  - Mont-Saint-Michel-Normandie : 40 %.
- **Les prairies humides inventoriées retournées** sont d'abord dans le bocage de l'ouest. En prairies anciennes :
  - CA Mont-Saint-Michel-Normandie : 20,1 ha/an ;
  - Flers Agglo : 17,8 ha/an ;
  - Andaine-Passais : 15,7 ha/an ;
  - Baie du Cotentin : 13,9 ha/an.
- **Des retournements en Natura 2000**, surtout dans l'Orne :
  - Vallées d'Auge et du Merlerault : 37 ha/an ;
  - Terres d'Argentan : 25 ha/an ;
  - Vire au Noireau : 25 ha/an.

  Une prairie en site Natura 2000 n'est pas forcément une « prairie sensible » au sens de la PAC, qui interdit seulement de retourner ces dernières. C'est donc **à vérifier avant tout affichage**.

## Bloc E : trajectoire ZAN et efficacité (Normandie)

- **Consommation d'ENAF :** 16 857 ha du 1/1/2011 au 1/1/2021, soit 1 685 ha/an. Puis 5 787 ha du 1/1/2021 au 1/1/2025, soit 1 447 ha/an.
- **Enveloppe de référence 2021-2031** (moitié de 2011-2021) : 8 428 ha. **69 % déjà consommés en 4 ans.** Au rythme actuel, la consommation 2021-2031 atteindrait 172 % de l'enveloppe.
- **Ce n'est pas l'objectif officiel de chaque EPCI.** La territorialisation du SRADDET fixe des taux différents selon les territoires, et la loi TRACE pourrait modifier l'étape de 2031. À afficher comme une « trajectoire de référence ».
- **Seul 1 EPCI sur 71 est sous 100 % de l'enveloppe en projection** : Fécamp Caux Littoral, à 91 %.
- **Valeurs extrêmes, liées à un petit dénominateur :** la CC de la Vallée de la Haute Sarthe a consommé 85 ha en 2021-2025, contre 41 ha en 2011-2021. Cela fait 1 046 % de projection, probablement un grand projet unique. Cœur de Nacre est à 479 %. **À examiner avant tout affichage.**
- **Efficacité 2016-2022 :**
  - +70 953 logements, soit **11,5 logements par ha** consommé pour l'habitat ;
  - +38 605 emplois, soit **21,6 emplois par ha** consommé pour l'activité.
  - Les écarts sont forts : Rouen est à 92,5 logements par ha, la médiane des EPCI à 6,1.
  - **Dans 31 EPCI, l'emploi a baissé** malgré la consommation d'espace pour l'activité, d'où un ratio négatif.
  - Le ratio est laissé vide quand moins de 1 ha a été consommé.

## Bloc F : profils de comparaison

| Profil | Règle | EPCI | Perte de PP médiane (% du stock/an) | Part du béton médiane |
|---|---|---|---|---|
| Urbain | densité ≥ 300 hab/km² | 5 | 0,91 | 7,4 % |
| Périurbain | densité de 100 à 300 hab/km² | 21 | 1,49 | 3,8 % |
| Rural herbager | densité < 100 et prairies permanentes ≥ 20 % du territoire | 25 | 1,74 | 1,6 % |
| Rural de grandes cultures | densité < 100 et prairies < 20 % | 20 | 1,41 | 2,0 % |

**Pourquoi 20 % :** c'est proche de la médiane régionale (17,6 %). Un seuil de 30 % classait le Bocage virois, Flers et le Domfrontais en « grandes cultures ».

**Colonnes ajoutées :** `profil`, `n_profil`, `rang_perte_profil` (1 = plus forte perte du profil), et les médianes du profil pour la perte et la part du béton.

**Exemple :** la CC Coutances Mer et Bocage est rurale herbagère. Elle est 12e sur 25 pour la perte (1,82 % par an contre une médiane de 1,74 %), et la part de son béton est égale à la médiane (1,6 %).

### EPCI à cheval sur une autre région (ajout du 01/11/2026)

**Principe :** tous les calculs ne portent que sur les communes des 5 départements normands. Les ratios restent cohérents, parce que le numérateur et le dénominateur couvrent le même périmètre. Les hectares, eux, ne couvrent que la partie normande de l'EPCI. Choix de l'équipe : on n'ajoute pas les départements voisins (version « légère »).

**Nouvelles colonnes :**
- `part_hors_normandie_surface_pct` et `part_hors_normandie_population_pct`, calculées depuis geo.api ;
- `perimetre` : « EPCI entier » ou « partie normande (X % de la surface) » ;
- `exclu_comparaisons` : vrai quand au moins 50 % de la surface est hors Normandie. Le rang et les médianes du profil sont alors vides, et ces EPCI sont retirés du calcul des médianes.

| EPCI | Part normande de la surface | Traitement |
|---|---|---|
| CC Interco Normandie Sud Eure | 99 % | Comparé normalement |
| CC Aumale - Blangy-sur-Bresle | 81 % | Comparé, avec la mention « partie normande » |
| CU d'Alençon | 73 % | Comparé, avec la mention « partie normande » |
| CC des Villes Sœurs | 61 % | Comparé, avec la mention « partie normande » |
| CA du Pays de Dreux | 5 % | **Exclu des comparaisons** |
| CC Maine Saosnois | 5 % | **Exclu des comparaisons** |

**Règle d'affichage :** toujours afficher `perimetre` dans la fiche d'un EPCI à cheval. Pour Dreux et Maine Saosnois, présenter les chiffres comme ceux de « quelques communes normandes », sans rang.

## Contrôles

- **Les anciennes colonnes sont inchangées :** stock 603 767 ha, charrue 8 246 et 4 970 ha/an, béton 1 374 ha/an, part du béton 2,1 à 6,4 %, comme dans le T7.
- **Aucun sous-total ne dépasse son total,** pour aucun EPCI : béton par milieu ≤ béton total, charrue par milieu ≤ charrue totale, prairies anciennes ≤ toutes PP.
- **Tous les EPCI ont un nom, une densité et un profil.**

## Limites à afficher

- **MPH :** c'est un modèle de 2014, au 1/100 000. Il indique une probabilité de milieu humide, pas une zone humide avérée. Il ne tient pas compte du drainage.
- **Inventaire DREAL :** il est hétérogène. Il mêle inventaires de terrain et photo-interprétation, et sa couverture varie selon les territoires.
- **Rattachement de la charrue aux zones :** il se fait par le point intérieur de la parcelle. Une parcelle à cheval sur une limite est comptée entièrement d'un seul côté.
- **Recensements INSEE :** les valeurs « 2016 » et « 2022 » sont des moyennes sur 5 ans d'enquêtes. Le rapprochement avec la consommation du 1/1/2016 au 1/1/2022 est donc approximatif.
- **Enveloppe ZAN :** c'est une enveloppe de référence nationale, pas l'objectif territorialisé du SRADDET.
