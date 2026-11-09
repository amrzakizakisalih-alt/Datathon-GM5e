# Historique des modifications

Ce document garde la trace de chaque modification du code : **ce qui a été fait, concrètement, et à quoi ça sert**. Les entrées les plus récentes sont en bas.

`EXPLICATION_CODE.md` décrit l'état du code à un instant donné. Ce document-ci décrit comment on y est arrivé.

---

## 8 novembre 2026 : phase 1, fiabiliser le socle

Objectif de la phase : que chaque chiffre actuel soit juste, et qu'on puisse le prouver. Les étapes retenues sont celles qui ont obtenu la meilleure note lors de l'évaluation des pistes : l'analyse de sensibilité (9/10), le module de définitions commun (8/10), les tests (7/10) et ADMIN EXPRESS (7/10, à condition de mesurer d'abord le gain).

Avant de commencer, les résultats de `data/processed/` ont été sauvegardés à part, pour pouvoir mesurer l'effet de chaque modification.

### Étape 1 : un module de définitions commun (`src/definitions.py`)

**Le problème :** chaque script réécrivait sa propre façon de classer les cultures du RPG, et ces copies avaient divergé.
- La jachère (groupe RPG 11, « gel ») comptait comme une culture dans `retournements_epci.py` et `beton_charrue_epci.py`, mais pas dans `qualite_epci.py`, dont le commentaire affirmait pourtant « même définition ».
- Les « prairies anciennes » n'avaient pas la même définition : PP chaque année jusqu'à l'année du retournement dans `retournements_epci.py` et `qualite_epci.py`, mais seulement jusqu'au début de la fenêtre OCS GE dans `beton_charrue_epci.py`.

**Ce qui a été fait :**
- Création de `src/definitions.py`, qui contient **à un seul endroit** :
  - la liste des années (2015 à 2024) ;
  - les groupes RPG de chaque classe (PP, PT, fourrage, gel, culture) ;
  - l'expression SQL qui classe une parcelle pour une année (`classe_sql`, `classes_sql`) ;
  - la condition « retournement strict » : PP l'année N, culture l'année N+1 (`retournement_sql`) ;
  - la condition « prairie ancienne » : PP chaque année de 2015 jusqu'à l'année N (`pp_ancienne_sql`).
- `retournements_epci.py`, `beton_charrue_epci.py`, `qualite_epci.py`, `friches.py` et `test_rattachement.py` importent maintenant ces définitions au lieu de les réécrire.

**Deux choix de méthode, tranchés une fois pour toutes :**
1. **La jachère n'est plus une culture.** Une prairie mise en jachère reste le plus souvent en herbe, et rien ne prouve un labour. La compter comme « charrue » surestimait la charrue. La jachère devient une classe à part, `gel`.
   - Elle n'entre plus dans la charrue (retournement strict).
   - Elle entre dans la borne haute des pertes, via une nouvelle colonne `vers_gel` dans `retournements_epci_XX.csv`.
   - Le béton posé sur une jachère reste compté avec le béton sur cultures (`beton_sur_cultures`), parce que c'est une parcelle déclarée.
2. **Une seule définition des prairies anciennes :** PP chaque année de 2015 jusqu'à l'année de départ du retournement. C'est la plus stricte, et c'est celle qu'utilisaient déjà deux scripts sur trois.

**L'effet sur les chiffres (Normandie, en ha/an) :**

| Indicateur | Avant | Après | Écart |
|---|---|---|---|
| Charrue 2015-2024, toutes PP | 8 246 | 8 150 | −96 (−1,2 %) |
| Charrue 2015-2024, PP anciennes | 4 970 | 4 920 | −50 (−1,0 %) |
| Charrue sur la fenêtre OCS GE | 9 785 | 9 695 | −90 (−0,9 %) |
| Charrue sur la fenêtre, PP anciennes | 5 216 | 5 166 | −50 (−1,0 %) |
| Prairies perdues (borne basse) | 9 995 | 9 905 | −90 (−0,9 %) |
| Part du béton (borne basse / haute) | 2,10 % / 6,37 % | 2,12 % / 6,43 % | +0,02 / +0,06 point |
| Bloc D (`qualite_epci.py`) | — | — | aucun : ce script excluait déjà la jachère |

Les prairies mises en jachère représentent 864 ha sur les 9 passages, soit environ 96 ha/an : c'est exactement ce que la charrue a perdu. Le message du projet ne change pas : le béton reste à 2 à 6 % des prairies perdues.

**À quoi ça sert :** deux scripts ne peuvent plus diverger. Une définition à modifier se modifie à un seul endroit, et la modification s'applique partout.

### Étape 2 : des tests automatiques (`tests/`)

**Le problème :** le code citait des tests (`tests/T5b`, `T8`, `T9`) absents du dépôt. Rien ne permettait de vérifier qu'une modification ne casse pas un calcul.

**Ce qui a été fait :** création d'un dossier `tests/` avec 18 tests, lancés par `pytest`.
- `tests/conftest.py` fabrique un **territoire fictif** : deux communes de 1 km² (A dans l'EPCI E1, B dans l'EPCI E2), des parcelles de 1 ha et des polygones de béton, aux formats exacts des vraies données (RPG Explorer, OCS GE, geo.api).
- `tests/test_definitions.py` (6 tests) vérifie le classement des cultures, le retournement strict, la jachère qui n'est pas un retournement et les prairies anciennes (une PT reclassée en PP en 2018 n'est jamais ancienne, un trou de déclaration casse l'ancienneté).
- `tests/test_geo_utils.py` (4 tests) vérifie que `charger_communes` lit tous les départements et passe bien en Lambert 93 (1 km² = 1 000 000 m²), et que `rattacher_plus_proche` attribue un objet orphelin à la bonne commune.
- `tests/test_pipeline_scripts.py` (8 tests) fait tourner **les vrais scripts** `retournements_epci.py` et `beton_charrue_epci.py` sur le territoire fictif, et compare leurs résultats à des valeurs calculées à la main. Chaque parcelle fictive illustre un cas :
  - une prairie ancienne retournée ;
  - une PT reclassée en PP en 2018 puis retournée (comptée, mais pas comme ancienne) ;
  - une prairie mise en jachère (hors charrue, mais dans la borne haute) ;
  - un trou de déclaration en 2023 ;
  - une parcelle hors des contours, rattachée à la commune la plus proche ;
  - une prairie retournée dont la moitié est bétonnée : **le béton l'emporte**, la charrue ne compte que l'autre moitié ;
  - du béton sur de l'herbe hors PAC (borne haute) ;
  - une désartificialisation, séparée entre « sols rendus » et « changement d'usage ».

**Comment les lancer :** `.venv/bin/python -m pytest tests` (environ 4 secondes). Résultat : **18 tests réussis**.

**À quoi ça sert :** chaque future modification peut être vérifiée en quelques secondes. Les tests documentent aussi la méthode : chacun montre, sur un exemple concret, comment un cas est compté.

**Ce que les tests ne font pas :** ils vérifient la logique du code, pas la qualité des données. Ils ne règlent aucune des limites des données (artefacts de la PAC, hors PAC…).

### Étape 3 : l'analyse de sensibilité (`src/sensibilite.py`)

**Le problème :** deux anomalies connues du RPG pouvaient fausser la charrue et le classement des EPCI : le reclassement de 2018 (84 000 ha de PT passés en PP) et le trou de 2023 (30 000 ha qui disparaissent du RPG). On ne savait pas si nos conclusions en dépendaient.

**Ce qui a été fait :** un nouveau script, `src/sensibilite.py`, ajouté à la fin de `pipeline.py`. Il recalcule la charrue moyenne de chaque EPCI selon quatre scénarios, puis compare le classement des EPCI (taux de charrue en % du stock de PP de 2015) à celui de référence :
- `reference` : les 9 passages 2015→2024, toutes PP (le chiffre du tableau régional) ;
- `sans_2018` : sans le passage 2017→2018 ;
- `sans_2023_2024` : sans les passages 2022→2023 et 2023→2024 ;
- `anciennes` : les 9 passages, prairies anciennes seulement.

La comparaison utilise la corrélation de rang de Spearman (1 = même classement), le plus grand déplacement d'un EPCI, le nombre d'EPCI déplacés de plus de 5 rangs et le nombre d'EPCI communs aux deux top 10. Les 2 EPCI exclus des comparaisons sont écartés (69 EPCI classés).

**Sortie :** `data/processed/sensibilite_epci.csv`, une ligne par EPCI avec la charrue et le rang de chaque scénario.

**Les résultats :**

| Scénario | Charrue Normandie (ha/an) | Écart | Spearman | Déplacement max | EPCI déplacés de plus de 5 rangs | Top 10 commun |
|---|---|---|---|---|---|---|
| référence | 8 147 | — | 1,000 | 0 | 0 | 10/10 |
| sans 2018 | 8 808 | +8,1 % | 0,998 | 5 rangs | 0 | 9/10 |
| sans 2023-2024 | 8 192 | +0,5 % | 0,982 | 13 rangs | 9 | 9/10 |
| prairies anciennes | 4 917 | −39,6 % | 0,878 | 37 rangs | 35 | 6/10 |

**Ce que ça veut dire :**
1. **Le reclassement de 2018 ne fausse pas le classement.** Sans le passage 2017→2018, le classement est presque identique (0,998). La charrue moyenne monte même de 8 % : le passage 2017→2018 avait peu de retournements, il ne gonflait donc pas la charrue.
2. **Le trou de 2023 compte un peu pour certains EPCI.** Le total régional ne bouge presque pas (+0,5 %), mais 9 EPCI se déplacent de plus de 5 rangs. Il faut le signaler pour ces EPCI, sans remettre en cause les conclusions régionales.
3. **Le vrai choix qui pèse, c'est « toutes les PP » contre « PP anciennes ».** La charrue baisse de 40 % et la moitié des EPCI change nettement de rang (35 déplacés de plus de 5 rangs, seulement 6 EPCI communs aux deux top 10). Explication probable : dans certains territoires, beaucoup de « prairies permanentes » sont en réalité de vieilles prairies temporaires intégrées à une rotation, retournées régulièrement. Elles comptent dans « toutes les PP », pas dans « PP anciennes ».

**Conséquence à trancher :** le cahier des charges prévoit que « le chiffre principal de la charrue porte sur les prairies anciennes ». Or le tableau régional calcule `prairies_perdues_ha_an`, `part_beton_pct`, `perte_pct_stock_an` et les rangs de profil avec **toutes** les PP. Ce n'est pas un détail : le classement des EPCI change beaucoup selon ce choix. Il faut décider lequel afficher en premier, et montrer l'autre à côté.

**À quoi ça sert :** on peut maintenant dire au jury, chiffres à l'appui, que nos conclusions ne dépendent pas des anomalies de 2018, qu'elles dépendent un peu de 2023 pour quelques EPCI, et que le choix de l'indicateur (toutes PP ou PP anciennes) est déterminant et assumé.

### Étape 4 : ADMIN EXPRESS, mesurer le gain avant de changer les contours

**Le problème :** 899 parcelles (LCP), environ 4 700 ha, ne tombent dans aucune commune normande. Elles sont rattachées à la commune la plus proche, jusqu'à 2,1 km. On supposait que les contours de geo.api.gouv.fr étaient trop simplifiés, et que les contours précis d'**ADMIN EXPRESS** (IGN) feraient disparaître la plupart de ces orphelines. La règle fixée lors de l'évaluation des pistes était de **mesurer le gain avant de changer quoi que ce soit**.

**Ce qui a été fait :**
1. Téléchargement des communes d'ADMIN EXPRESS (édition la plus récente) sur l'emprise de la Normandie, par le service WFS de l'IGN : 4 787 communes, Normandie et départements voisins. Fichier : `data/raw/geo/admin_express_communes.geojson` (113 Mo, non versionné).
2. Une mesure ponctuelle, non intégrée à la pipeline : pour les 887 899 LCP et les 26 496 polygones de béton des 5 départements, on cherche la commune de leur point intérieur avec chacun des deux jeux de contours, puis on compare.

**Les résultats :**

| Mesure | geo.api | ADMIN EXPRESS |
|---|---|---|
| LCP orphelines | 899 (4 667 ha) | 900 (4 668 ha) |
| Polygones de béton orphelins | 0 | 0 |
| LCP qui changent d'EPCI entre les deux jeux | 9 LCP, 15 ha | |

**Conclusion : ADMIN EXPRESS n'apporte rien, et la pipeline n'a pas été modifiée.** Les contours de geo.api sont en fait assez précis pour notre usage. L'hypothèse d'une simplification excessive était fausse : la mesure a évité un changement inutile.

**Ce que la mesure a appris sur les orphelines :** elles ne viennent pas d'un défaut de contours. Leur point tombe réellement hors de Normandie.

| Où tombent-elles ? | LCP | Surface | dont PP en 2015 |
|---|---|---|---|
| **En mer ou sur l'estran**, sur la côte ouest de la Manche | environ 276 | environ 3 850 ha | environ 3 770 ha |
| **Dans une commune d'un département voisin** (Ille-et-Vilaine, Mayenne, Sarthe, Eure-et-Loir, Oise, Yvelines, Val-d'Oise, Somme) | 622 | environ 820 ha | environ 350 ha |

1. **Les parcelles en mer sont des prés salés** (prairies littorales pâturées, par exemple dans la baie du Mont-Saint-Michel), déclarées à la PAC en prairie permanente, au-delà du trait de côte des contours communaux. Elles ne sont quasiment jamais retournées : 2 ha de charrue en 9 ans. Les rattacher à la commune littorale la plus proche est **correct** et ne fausse pas la charrue. Elles augmentent seulement le stock de PP des EPCI côtiers.
2. **Les parcelles des départements voisins sont mal comptées.** Les fichiers RPG Explorer « départementaux » débordent un peu sur les départements voisins, hors de Normandie. Ces parcelles sont aujourd'hui attribuées à tort à l'EPCI normand le plus proche. L'effet est faible (environ 350 ha de PP sur 603 765, soit 0,06 % du stock), mais **la bonne règle serait de les exclure**, puisqu'elles appartiennent à des EPCI d'autres régions.

**Ce qui reste à décider :** exclure ces 622 parcelles. Ce n'était pas dans la liste des étapes retenues. La correction est simple : charger aussi les communes voisines d'ADMIN EXPRESS (déjà téléchargées), et écarter tout objet qui tombe dans l'une d'elles.

**À quoi ça sert :** la limite « 899 LCP au rattachement non prouvé » de `EXPLICATION_CODE.md` est maintenant expliquée et chiffrée. Les deux tiers de la surface sont des prés salés, correctement rattachés. Le reste est une petite erreur, identifiée, avec sa correction connue.

---

## 9 novembre 2026 : fusion avec la version du camarade

**Le contexte :** une nouvelle version, réalisée par un camarade, a été copiée dans `src/`. Elle apportait cinq scripts nouveaux (`echantillon_validation.py`, `preparer_lecture.py`, `resultat_validation.py`, `sensibilite_prl.py`, `export_web.py`), un autre `sensibilite.py`, et une correction dans `beton_charrue_epci.py`. Mais elle partait d'une version antérieure à la phase 1 : la copie avait écrasé `charger_communes`, l'usage de `definitions.py`, mon analyse de sensibilité et l'appel à celle-ci dans `pipeline.py`. Les tests ne se lançaient plus.

Une revue complète a d'abord été faite, en exécutant la nouvelle version dans une copie isolée du projet. La fusion a ensuite gardé le meilleur des deux versions. Avant de commencer, `src/` et `data/processed/` ont été sauvegardés.

**Bonne nouvelle constatée pendant la revue :** les deux versions avaient fait **les mêmes choix de méthode** sans se concerter. La jachère est une classe à part (`vers_gel`), et les prairies anciennes sont « PP chaque année de 2015 jusqu'à N » partout.

### Étape 1 : protéger les données sensibles (`.gitignore`)
`echantillon_validation.py` et `preparer_lecture.py` écrivent dans `data/validation/` les coordonnées et les contours de parcelles agricoles. Le cahier des charges interdit de les publier, et ce dossier n'était pas exclu de git. **Ajout de `data/validation/` (et de `.pytest_cache/`) au `.gitignore`**, avant tout commit.

### Étape 2 : fusionner les scripts de calcul
| Fichier | Gardé de la version du camarade | Remis de notre version |
|---|---|---|
| `geo_utils.py` | — | `charger_communes` (les communes des 5 départements) |
| `retournements_epci.py` | la description des colonnes | `charger_communes`, les définitions de `definitions.py` |
| `beton_charrue_epci.py` | **la ventilation du béton selon l'EPCI du polygone** | `charger_communes`, `definitions.py`, la liste des EPCI limitée à ceux où le département a des objets |
| `qualite_epci.py` | — | `charger_communes`, l'emprise des zonages calculée sur le seul département, la liste des EPCI limitée, `definitions.py` |
| `friches.py`, `echantillon_validation.py`, `sensibilite.py`, `sensibilite_prl.py` | tout le code | les groupes RPG importés de `definitions.py`, au lieu d'être écrits en dur |
| `sensibilite_prl.py` | tout le code | `charger_communes`, pour rattacher les parcelles comme la pipeline |

**La correction du camarade, gardée :** auparavant, le béton posé sur une parcelle était attribué à l'EPCI de la **parcelle**, alors que le béton total l'était à l'EPCI du **polygone de béton**. Pour un polygone à cheval sur deux EPCI, la répartition « béton sur PP, sur PT, sur cultures, hors RPG » ne s'additionnait donc plus au total. Tout est maintenant attribué à l'EPCI du polygone.

**Le piège évité :** dans la version du camarade, la liste des EPCI d'un fichier départemental était « tous les EPCI des communes chargées ». Avec les communes des 5 départements, chaque fichier aurait listé les 71 EPCI, presque tous à zéro. La restriction de notre version a été reprise : 13 à 26 EPCI par département.

**`definitions.py`** contient en plus les deux codes du groupe 18, `CODE_PPH` et `CODE_PRL`, utilisés par `sensibilite_prl.py`.

### Étape 3 : deux analyses de sensibilité qui portaient le même nom
Mon `sensibilite.py` (les anomalies de la PAC) et celui du camarade (les seuils, les poids, les rayons) sont complémentaires. Le mien devient **`sensibilite_anomalies.py`**, avec en plus :
- **un scénario « sans 2019 »**, pour le pic de labours qui suit le reclassement de 2018 ;
- **des rangs moyens pour les ex aequo**, comme dans la définition standard de Spearman.

### Étape 4 : de petites corrections
- **La fonction `spearman`** de `sensibilite.py` et de `sensibilite_prl.py` départageait les ex aequo au hasard. Elle leur donne maintenant le rang moyen. L'effet mesuré est d'au plus 0,003 sur les corrélations.
- **`resultat_validation.py`** affiche un avertissement si une strate n'a aucun point lu : son poids était reporté sur les autres sans le dire.
- **`sensibilite.py`** ferme correctement le fichier `fenetres.csv`.

### Étape 5 : une seule commande, jusqu'au site
`pipeline.py` lance maintenant, après le tableau régional, les trois analyses de sensibilité puis `export_web.py`. Auparavant, l'export dépendait de fichiers que la pipeline ne produisait pas : il fallait lancer 4 scripts à la main, dans le bon ordre.

### Étape 6 : les tests (20 au lieu de 18)
- Les 18 tests existants passent de nouveau.
- **Un test `PRL` :** une prairie en rotation longue est bien une PP pour les définitions communes.
- **Un test du béton à cheval sur deux EPCI :** un polygone de 3 ha, dont le point intérieur tombe dans B, recouvre 1 ha d'une prairie de A. Tout son béton, y compris celui posé sur la prairie de A, doit être compté dans B. Ce test échouerait avec l'ancienne ventilation par parcelle.

### Les résultats de la pipeline fusionnée
Toute la chaîne tourne sans erreur, de la charrue jusqu'aux fichiers du site (`web/data/`, 71 fiches EPCI).

| Normandie | Notre version | Version du camarade | **Fusion** |
|---|---|---|---|
| Stock de PP en 2015 (ha) | 603 765 | 603 767 | **603 765** |
| Charrue, toutes PP (ha/an) | 8 150,2 | 8 150,2 | **8 150,2** |
| Béton sur PP (ha/an) | 210,1 | 210,2 | **210,2** |
| Béton hors RPG (ha/an) | 906,7 | 906,8 | **906,8** |
| Prairies perdues (ha/an) | 9 905,0 | 9 905,0 | **9 904,9** |

La fusion reprend bien **notre rattachement** (le stock, la charrue et les milieux sont identiques à notre version, EPCI par EPCI) et **la ventilation du béton du camarade** (les colonnes de béton sont identiques aux siennes). Aucun rang de profil ne change. Les contrôles internes passent : écart de 0,7 ha entre `sensibilite_prl.py` et la pipeline, et Jaccard = 1 pour le recalcul des friches.

**Un résultat nouveau, grâce au scénario « sans 2019 » :**

| Scénario | Charrue (ha/an) | Écart | Spearman | EPCI déplacés de plus de 5 rangs |
|---|---|---|---|---|
| référence | 8 147 | — | 1,000 | 0 |
| sans 2018 | 8 808 | +8,1 % | 0,998 | 0 |
| **sans 2019** | **7 172** | **−12,0 %** | **0,967** | **19** |
| sans 2023-2024 | 8 192 | +0,5 % | 0,982 | 9 |
| prairies anciennes | 4 917 | −39,6 % | 0,878 | 35 |

Le passage 2018→2019 pèse beaucoup plus que le passage 2017→2018 : c'est **l'année qui suit le reclassement** qui gonfle la charrue « toutes PP », puisque les PT reclassées en 2018 sont labourées en 2019. L'analyse d'hier, qui ne retirait que 2017→2018, ne pouvait pas le voir. Les prairies anciennes, elles, neutralisent cet effet.

### Étape 7 : les fichiers manquants, rangés à leur place
Trois fichiers cités par les scripts sont arrivés dans `src/` pendant la fusion. Ils ont été déplacés là où les scripts et le protocole les attendent :

| Fichier | Nouvel emplacement | Pourquoi |
|---|---|---|
| `lecture.html` | `data/validation/lecture.html` | la page charge `points_lecture.js` et `images/` dans son propre dossier |
| `LISEZ-MOI.md` (le protocole de validation) | `data/validation/LISEZ-MOI.md` | c'est ce chemin que citent `echantillon_validation.py` et `resultat_validation.py` |
| `registre_choix_methodologiques.md` | `docs/registre_choix_methodologiques.md` | c'est ce chemin que cite `sensibilite.py` |

Le protocole précise que git ne doit conserver, dans `data/validation/`, **que** `LISEZ-MOI.md` et `lecture.html`. Le `.gitignore` a été affiné en ce sens : tout le dossier est ignoré, sauf ces deux fichiers. Vérifié avec `git check-ignore`.

### Étape 8 : un défaut de `qualite_epci.py`, signalé par le registre
**Le problème :** le registre du camarade mentionne une correction : « une année non déclarée annulait tout le décompte d'une LCP dans `qualite_epci.py` ». Le défaut était bien présent dans notre version. Le script additionne, pour chaque parcelle, ses retournements des 9 passages. Une année non déclarée valait `NULL`. Si une parcelle était en PP une année puis non déclarée l'année suivante, ce terme valait `NULL`, **toute la somme devenait `NULL`**, et `coalesce(..., 0)` la remplaçait par 0. Les retournements des **autres** années de cette parcelle disparaissaient.

**La correction :** dans `qualite_epci.py`, une année non déclarée vaut maintenant `'non déclaré'` au lieu de `NULL`. La comparaison donne alors « faux » au lieu de « inconnu ». Un test (`test_annee_non_declaree_n_efface_pas_les_autres_retournements`) reproduit le piège et vérifie la correction. Les autres scripts n'avaient pas ce défaut : ils comptent avec `FILTER (WHERE ...)`, qui traite `NULL` comme faux.

**L'effet sur la charrue en milieux remarquables (Normandie, ha/an, moyenne 2015-2024) :**

| Milieu | Avant | Après | Écart |
|---|---|---|---|
| Zones humides inventoriées | 375,7 | 395,6 | +5,3 % |
| dont prairies anciennes | 253,2 | 261,4 | +3,2 % |
| Milieux potentiellement humides | 1 451,0 | 1 514,7 | +4,4 % |
| dont prairies anciennes | 847,3 | 869,7 | +2,6 % |
| Natura 2000 | 155,8 | 170,8 | +9,6 % |
| ZNIEFF de type 1 | 39,9 | 44,4 | +11,3 % |

Ces chiffres sont **identiques à ceux du registre** (376 → 396, 1 451 → 1 515, 156 → 171, 40 → 44) : la correction concorde avec celle du camarade. La charrue totale, le béton et le bilan ne changent pas, puisqu'ils ne viennent pas de ce script.

### Ce qui reste à faire
- **Demander au camarade sa dernière version de `qualite_epci.py`.** Le registre décrit une charrue par milieu calculée « sur la fenêtre OCS GE, nette du béton », alors que la version reçue la calcule sur 2015-2024. Soit cette évolution n'a pas été transmise, soit le registre anticipe. Il faut vérifier avant de publier ces chiffres.
- **Récupérer les comptes rendus de tests T1 à T10**, cités par le registre comme preuves (« dossier `tests/` »), et `web/data/LISEZ-MOI.md`.
- **Travailler par branches git** pour éviter que la situation se reproduise : chacun sur sa branche, puis une fusion qui signale les conflits au lieu de les écraser.
- `src/communes_epci.html` (8 Mo, une page générée) devrait sortir de `src/`.
