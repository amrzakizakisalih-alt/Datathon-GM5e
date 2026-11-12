# T10 : calculs de l'écran 2, « Où rendre » (friches)

> Note du 10/11/2026 : la part humide des friches était surestimée par une erreur de calcul, et non par la taille du pixel comme l'indique ce compte rendu. Après correction, 190 friches ont une part intermédiaire (26 avant), et il y a 415 « gains rapides » pour 672 ha (413 pour 635 ha avant). Le nom des friches n'est plus écrit dans `friches.csv`. Voir le registre, sections 5 et 8.

Date : 01/11/2026. Résultat : **les 5 068 friches de l'observatoire de l'EPF Normandie ont un potentiel écologique, une classe, leurs raisons et leurs points de vigilance.** La synthèse par EPCI est intégrée au tableau régional, qui passe à 75 colonnes. Le calcul (`src/friches.py`) prend environ 1 min 30 et fait partie de `src/pipeline.py`.

## Source

- **Observatoire des friches de l'EPF Normandie** (DataNormandie), édition du 10/03/2026, sous Licence ouverte 2.0. Il compte 5 068 polygones en Lambert-93, pour 3 326 ha. Le téléchargement est ajouté à `src/telecharger_donnees.py`.
- **Les friches sont souvent minuscules :** la moitié fait moins de 0,11 ha, et 44 % sont d'anciennes habitations. 284 friches de plus de 2 ha totalisent à elles seules 2 154 ha.
- **Les attributs environnementaux de l'EPF sont lacunaires :** pollution vide à 55 %, zone humide à 90 %, inondation à 77 %. Ils ne sont donc pas utilisés comme critères. On s'en sert seulement pour signaler (colonne `vigilance`) et pour compléter la part humide quand l'EPF indique une zone humide avérée.
- **L'EPF fournit déjà un « potentiel de renaturation »** pour chaque friche (de 42 à 84, médiane 57). Il suit une méthode de l'ADEME fondée sur le propriétaire, la surface, le bâti, la pollution, la centralité et la viabilisation. **C'est un score de faisabilité, pas d'intérêt écologique.** Il est repris tel quel comme faisabilité.

## Ce que nous ajoutons : le potentiel écologique

Quatre critères sont calculés pour toutes les friches à partir de nos couches, puis convertis en rangs centiles :

| Critère | Calcul | Distribution (10e / 50e / 90e centile) |
|---|---|---|
| Proximité d'un réservoir de biodiversité | Distance à la ZNIEFF de type 1 ou au site Natura 2000 le plus proche (0 = dedans, plafonnée à 5 km) | 61 m / 1 122 m / 4 170 m ; 272 friches sont dedans |
| Part humide | Maximum entre la part en zone humide inventoriée (DREAL), la part des pixels en milieu potentiellement humide (MPH) et la mention « avérée » de l'EPF | 0 / 0 / 100 % ; 1 932 friches ont une part humide non nulle |
| Prairies autour | Prairies permanentes déclarées en 2024 à moins de 500 m, rapportées à la couronne de 500 m | 0 / 11 / 38 % |
| Surface | Logarithme de la surface | — |

**Trois préréglages de poids** (réservoir, humide, prairies, surface, contexte urbain) :

| Préréglage | Poids |
|---|---|
| Biodiversité (par défaut) | 0,35 / 0,20 / 0,30 / 0,15 / 0 |
| Eau | 0,15 / 0,60 / 0,10 / 0,15 / 0 |
| Nature en ville | 0,15 / 0,15 / 0,05 / 0,15 / 0,50 |

**Robustesse :** on tire 1 000 jeux de poids au hasard (loi de Dirichlet sur les 4 critères écologiques). L'indice donne la part des tirages où la friche reste dans les 10 % les mieux classées.

**Corrélation entre notre potentiel écologique et la faisabilité de l'EPF : 0,31.** Les deux scores mesurent bien des choses différentes.

## Classes

| Classe | Règle | Friches | ha |
|---|---|---|---|
| Gain rapide | Potentiel ≥ 75e centile et faisabilité EPF ≥ médiane (58), parmi les friches éligibles | 413 | 635 |
| Fort potentiel, contraintes | Potentiel ≥ 75e centile et faisabilité < médiane | 154 | 106 |
| Potentiel modéré | Le reste des friches éligibles | 1 701 | 1 493 |
| Projet engagé | Projet de reconversion en démarches (foncières, techniques, financières) ou finalisé | 596 | 1 007 |
| Petite friche (< 0,1 ha) | Trop petite pour peser à l'échelle d'un EPCI | 2 204 | 85 |

Les friches éligibles sont celles d'au moins 0,1 ha et sans projet engagé (2 268 friches). Le seuil de potentiel (75e centile) vaut 64,3.

**Réglage :** une première version, avec un seuil au 70e centile et sans exclure les petites friches, donnait 1 009 « gains rapides », dont 341 de moins de 0,1 ha. Ce n'était pas assez sélectif.

**Parmi les 413 gains rapides :**
- 213 ont une robustesse d'au moins 50 % : ils restent en tête quels que soient les poids ;
- 195 sont en zone agricole ou naturelle, 76 en zone urbaine et 142 sans zonage renseigné ;
- 52 ont une pollution avérée et 33 une pollution potentielle.

## Raisons et vigilance

- **`raisons` :** les trois critères qui contribuent le plus au score par défaut, en clair. Exemple pour l'ancien site Bottu/Sanofi à Saint-Jean-de-Livet (2 ha) : « dans une ZNIEFF ou un site Natura 2000 ; 63 % de prairies permanentes à moins de 500 m ; 100 % en zone humide inventoriée ou potentielle ».
- **`vigilance` :** pollution avérée, potentielle, non connue ou non renseignée ; terrain constructible (pression foncière) ; zone inondable selon le PPRI.
  - Pour le site Bottu/Sanofi : « pollution non connue ».
  - Première version corrigée : elle ignorait la valeur « Non connue » de l'EPF et n'affichait aucune vigilance pour cet ancien site industriel.

## Lien avec l'écran 1 (colonnes du tableau régional)

**Nouvelles colonnes :**
- `n_friches`, `friches_ha`, `friches_gain_rapide_ha`, `n_gain_rapide`, `friches_fort_potentiel_contraintes_ha`, `friches_projet_engage_ha` ;
- `annees_beton_friches` et `annees_beton_gain_rapide` : la surface de friches rapportée au béton annuel de l'EPCI.

**À l'échelle régionale :**
- les friches représentent **2,4 années de béton** (3 326 ha pour 1 374 ha/an), et les seuls « gains rapides » **0,5 année** ;
- l'outil ne doit donc pas suggérer que les friches suffisent à compenser l'artificialisation : elles en compensent une petite partie.

**EPCI les plus dotés en gains rapides :**

| EPCI | Friches « gain rapide » | Surface | Années de béton |
|---|---|---|---|
| Métropole Rouen Normandie | 15 | 90 ha | 1,2 |
| CU Caen la Mer | 2 | 70 ha | 0,6 |
| CC du Pays de Honfleur-Beuzeville | 5 | 48 ha | 2,3 |
| CA Lisieux Normandie | 19 | 42 ha | 1,4 |
| CC des Vallées d'Auge et du Merlerault | 31 | 40 ha | 4,6 |

**Cas particulier :** un EPCI n'a aucune friche recensée. Ses colonnes friches sont vides, ce qui veut dire « aucune friche dans l'observatoire », pas « zéro hectare mesuré ».

## Contrôles

- **Rattachement :** les 5 068 friches sont toutes rattachées à un EPCI (point intérieur, aucun recours à la commune la plus proche).
- **Cohérence :** la somme par EPCI redonne exactement le total, soit 5 068 friches, 3 326 ha et 635 ha de gains rapides.
- **Lecture des premiers résultats :** les meilleurs scores vont à d'anciens sites industriels de fond de vallée, en ZNIEFF ou en Natura 2000, en zone humide et entourés de prairies. C'est le cas à Saint-Jean-de-Livet, Pont-Authou, Picauville et Gouffern en Auge. C'est conforme à l'intention.

## Limites à afficher

- **C'est un pré-repérage, pas une décision.** La faisabilité réelle dépend du coût de dépollution, de la maîtrise foncière et de la valeur du terrain, qui ne sont pas dans les données.
- **« Pollution non connue » ou « non renseignée » ne veut pas dire « site sain ».**
- **La part humide repose en partie sur un modèle de 2014 au 1/100 000.** Pour une petite friche, un seul pixel de 50 m décide, d'où des valeurs souvent à 0 ou 100 %.
- **Les prairies autour sont approchées par le point intérieur des parcelles RPG.** Elles ne comptent que les prairies déclarées à la PAC en 2024.
- **Les haies et les forêts ne sont pas prises en compte,** faute de couche à jour pour les forêts dans nos données. C'est une piste d'amélioration (BD Forêt v2).
- **Seuils réglables** en tête de `src/friches.py` : `SURFACE_MIN_HA`, `CENTILE_POTENTIEL`, `PRESETS`. Ils sont à faire valider par les experts au point d'étape.
