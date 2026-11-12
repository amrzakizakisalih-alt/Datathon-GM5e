# T7 : correction des réserves du tableau régional

Date : 18/10/2026. Les trois réserves sont traitées, et le tableau `data/processed/tableau_regional_epci.csv` est régénéré.

## 1. Désartificialisation de l'Orne : un artefact de changement d'usage

- **Diagnostic.** Sur 284 ha « désartificialisés » dans l'Orne en 2020→2023, **212 ha viennent de deux polygones** :
  - **136 ha à Gacé :** herbe en chantier (CS2.2.1 / US6.1) devenue herbe agricole (CS2.2.1 / US1.1) ;
  - **75,5 ha à Merlerault-le-Pin :** herbe sous un réseau d'utilité publique (CS2.2.1 / US4.3) devenue herbe agricole.

  Les deux se trouvent dans la CC des Vallées d'Auge et du Merlerault. **Le sol est resté en herbe aux deux dates.** C'est probablement la fin d'un grand chantier linéaire ou temporaire, à vérifier sur les orthophotos du Géoportail (L93 ≈ 502 700 / 6 858 400 et 494 800 / 6 847 300). L'IGN le compte comme une désartificialisation au sens du décret, mais ce n'est pas un « sol rendu à la nature ».
- **Comparaison :** dans les autres départements, la désartificialisation vient surtout de sols stabilisés ou bâtis redevenus herbe (CS1.1.x → CS2.2.1). Aucun polygone n'y dépasse 21 ha.
- **Correction** (`src/beton_charrue_epci.py`) : la désartificialisation est séparée en deux colonnes.
  - `desartif_sols` : la couverture de départ est CS1.1.x (bâti, revêtu, stabilisé). C'est la renaturation réelle, **à afficher**.
  - `desartif_usage` : la surface était déjà végétalisée et seul l'usage a changé. **À ne pas présenter comme une renaturation.**

| Département | Sols rendus (ha) | Changement d'usage (ha) |
|---|---|---|
| Calvados (2020-23) | 142 | 15 |
| Eure (2019-22) | 76 | 18 |
| Manche (2019-22) | 101 | 13 |
| Orne (2020-23) | 54 | **230** |
| Seine-Maritime (2019-22) | 142 | 24 |

Normandie : **172 ha/an de sols rendus** et 100 ha/an de changements d'usage.

## 2. Parcelles sans commune : rattachées à la commune la plus proche

- **Méthode.** Nouveau module `src/geo_utils.py`, fonction `rattacher_plus_proche()`. Il est utilisé par les deux scripts pour les parcelles RPG, les polygones béton et les polygones désartificialisés.
- **Parcelles rattachées par département :**

| Département | Parcelles | Distance médiane | Distance max |
|---|---|---|---|
| Calvados | 831 | 470 m | 2,8 km (littoral) |
| Eure | 192 | 29 m | 225 m |
| Manche | 610 | 59 m | 2,1 km |
| Orne | 427 | 31 m | 266 m |
| Seine-Maritime | 164 | 34 m | 194 m |

- **Effet :** le stock régional de prairies permanentes 2015 passe de 598 752 à **603 767 ha**. Aucun polygone béton n'était orphelin.

## 3. Nouvel indicateur : prairies probables hors PAC

- **Définition :** béton posé sur de l'herbe agricole (OCS GE CS2.2.1 / US1.1 l'année de début), sur la part du polygone **non couverte par une parcelle déclarée à la PAC**. Il s'agit probablement de prairies non déclarées : chevaux de loisir, petits éleveurs, pâtures communales.
- **Usage :** il fournit une **borne haute** de la part du béton dans les pertes de prairies. Nouvelles colonnes :
  - `beton_herbe_hors_pac` ;
  - `prairies_perdues_haute` ;
  - `part_beton_haute_pct`.

## Totaux Normandie après correction (ha/an)

| Indicateur | Valeur |
|---|---|
| Charrue, toutes PP (moyenne 2015-2024) | 8 246 |
| Charrue, PP anciennes (moyenne 2015-2024) | 4 970 |
| Béton total (IGN) | 1 374 |
| Béton sur PP déclarées | 210 |
| **Béton sur prairies probables hors PAC** | **456** |
| Désartificialisation, sols rendus | 172 |
| Désartificialisation, changement d'usage | 100 |
| **Part du béton dans les pertes de prairies** | **de 2,1 % à 6,4 %** |

## Effet sur les EPCI urbains : la fourchette s'élargit nettement

| EPCI | Béton total | Sur PP déclarées | Sur herbe hors PAC | Part du béton, basse | Part du béton, haute |
|---|---|---|---|---|---|
| CU Caen la Mer | 117,6 | 5,6 | 25,6 | 19,8 % | **57,7 %** |
| CA Seine-Eure | 54,9 | 2,5 | 9,4 | 22,2 % | **57,9 %** |
| CU Le Havre Seine Métropole | 74,3 | 5,2 | 9,3 | 7,4 % | 18,1 % |
| Métropole Rouen Normandie | 72,9 | 3,2 | 6,6 | 6,6 % | 17,8 % |
| CA Mont-Saint-Michel-Normandie | 67,5 | 11,8 | 24,6 | 1,1 % | 3,2 % |
| CA du Cotentin | 65,9 | 18,6 | 29,2 | 2,3 % | 5,6 % |

**Lecture :** dans le bocage, la conclusion ne change pas, la charrue domine largement. Autour de Caen et d'Évreux-Louviers (Seine-Eure), le béton pourrait représenter **plus de la moitié** des pertes de prairies, dès lors qu'on compte les prairies non déclarées à la PAC. C'est un message nuancé et plus juste pour les élus urbains.

## Réserves restantes

- Il faut vérifier sur orthophoto les deux polygones de l'Orne, ainsi que quelques cas d'« herbe hors PAC » bétonnée, pour confirmer qu'il s'agit bien de prairies et pas de délaissés ou de bas-côtés.
- Le reclassement de 2018 influence toujours la « charrue sur la fenêtre OCS GE ». Il faut privilégier les prairies anciennes dans le chiffre principal.
- 2025 n'est pas encore traité.
