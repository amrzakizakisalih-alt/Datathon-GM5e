# Registre des choix méthodologiques

Date : 01/11/2026. Ce registre liste chaque choix qui influe sur les chiffres de l'outil. Pour chacun, il donne l'alternative écartée, la justification et la preuve (mesure, test, source). Il sert à la page « méthode » et aux réponses au jury.

## Comment chaque choix est justifié

1. **Définition officielle d'abord.** On reprend une définition réglementaire quand elle existe : artificialisation, prairie permanente, ZAN.
2. **Méthode déjà publiée.** On reprend une méthode publiée par un service de l'État quand elle existe.
3. **Mesure de l'effet.** On chiffre ce que change le choix : écart, double compte, part de la surface.
4. **Fourchette plutôt que chiffre unique,** quand une source a un angle mort.
5. **Test de sensibilité** pour chaque seuil arbitraire, avec `src/sensibilite.py` (résultats dans `data/processed/sensibilite.csv`).
6. **Validation externe :** photo aérienne (`data/validation/`) et experts au point d'étape.

## 1. Sources et définitions

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Artificialisation = **couche officielle IGN « OCS GE Artificialisation »** | Règle maison couverture × usage | Couche conforme au décret 2023-1096, donc opposable. Notre règle ne peut pas reproduire les critères supplémentaires de l'IGN | Notre règle retrouvait 97,5 % de l'officiel, avec une précision de 92,8 %. 14 couples couverture/usage sont classés des deux façons par l'IGN (T5b) |
| Prairie permanente = **codes PAC du groupe 18 (PPH, PRL)** | Données satellitaires (Copernicus, OSO) | Définition réglementaire de la PAC (5 ans). Les cartes satellitaires distinguent mal prairies permanentes et temporaires | OSO : F1 de 0,37 pour l'herbe. Copernicus : la couche « perte de prairie » n'est juste qu'environ une fois sur deux (rapport « Prairies retournées ») |
| Suivi des parcelles avec **RPG Explorer** (INRAE), 2015-2024 | Superposer nous-mêmes les RPG annuels | Jeu ouvert (Etalab 2.0) qui suit déjà chaque morceau de parcelle d'une année à l'autre. Les identifiants de parcelle du RPG changent selon les années | Perte d'environ 1 % de surface au nettoyage, documentée par l'INRAE (T2) |
| Retournement = **prairie permanente l'année N et culture l'année N+1** | Comparer deux années éloignées | Méthode de la DRAAF Grand Est (Agreste, 2022) | Ordres de grandeur concordants : environ 1 à 1,5 % du stock par an, contre 1 à 1,2 % en Grand Est |
| Consommation d'espaces = **CONSOENAF (Cerema)** | Artificialisation OCS GE | Base légale du ZAN jusqu'en 2031 (fichiers fonciers) | Les deux bases sont gardées, chacune pour son usage : CONSOENAF pour le ZAN, OCS GE pour le béton |
| Logements = **INSEE, séries historiques 2016 et 2022** ; emplois = INSEE au lieu de travail (dans CONSOENAF) | Emplois Urssaf | L'Urssaf ne couvre que le secteur privé | Toutes les 2 644 communes ont des données |

## 2. Charrue

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **Charrue et béton comparés sur les mêmes années** (fenêtre OCS GE), y compris par milieu | Comparer la moyenne 2015-2024 de la charrue au béton sur 3 ans | Une comparaison n'a de sens que sur une même période. La moyenne 2015-2024 reste affichée seule, en fourchette | Charrue par milieu sur la fenêtre, nette du béton : total identique à `beton_charrue_epci` à moins de 1 ha par département. Correction d'un défaut : une année non déclarée annulait tout le décompte d'une LCP dans `qualite_epci.py` (zones humides 376 -> 396 ha/an, MPH 1 451 -> 1 515, Natura 2000 156 -> 171, ZNIEFF 1 40 -> 44) |
| **PRL (prairie en rotation longue) maintenu dans les prairies permanentes** | Retirer PRL, au moins pour 2022 -> 2023, année où le code disparaît | Classement du RPG Explorer. PRL pèse environ 9 % du stock mais 15 % de la charrue : le retirer change le niveau régional, pas la lecture territoriale. À présenter comme une fourchette | `data/processed/sensibilite_prl.csv` : charrue 8 150 -> 6 913 ha/an sans PRL (-15 %), anciennes 4 920 -> 4 355 (-11,5 %) ; sans PRL en 2023 seulement : -3 % ; classement des EPCI : Spearman 0,98. PRL -> culture : 3,2 % en 2022, 3,7 % en 2023, pas d'anomalie liée à la suppression du code |
| **Trois niveaux :** prairies anciennes, toutes prairies, borne haute | Un seul chiffre | Le reclassement PAC de 2018 a fait passer d'un coup +42 000 ha de prairies temporaires en permanentes dans la Manche. La refonte du RPG de 2023 a fait disparaître le code PRL | Classement des EPCI « toutes prairies » contre « prairies anciennes » : Spearman 0,80 |
| **Prairie ancienne** = prairie permanente chaque année de 2015 à N, même définition partout | Prairie permanente au début de la période | Elle écarte les prairies reclassées en 2018 | La définition était différente dans `beton_charrue_epci.py` ; c'est harmonisé, avec un effet inférieur à 1 % |
| **Mise en gel (groupe 11) hors des cultures**, comptée dans la borne haute | Gel compté comme culture | Une mise en gel n'implique pas forcément un labour | 774 ha sur 71 508 ha (1,1 %). Correction appliquée : la charrue baisse de 1,2 % |
| **Sortie de la PAC = devenir inconnu**, jamais comptée comme retournement | La compter comme perte | On ne sait pas ce que devient la parcelle (vente, exploitant non déclarant, artefact de 2023) | 10 000 ha de prairies permanentes non déclarées en 2023 dans la seule Manche (T2) |
| **Retournements répétés comptés à chaque fois** (on compte des événements de labour) | Surface distincte | Chaque labour est une perte de couvert. L'indicateur « prairies anciennes » n'est pas concerné | 937 ha (1,3 %), sur 573 parcelles |
| **Béton prioritaire sur la charrue** | Compter les deux | Ne rien compter deux fois | Recouvrement mesuré : environ 1 ha dans la Manche (T5) |

## 3. Béton

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Ce qu'il y avait avant le béton = **culture déclarée l'année de début** | Couverture OCS GE seule | L'OCS GE confond prairie et culture (même couverture « herbacé », même usage « agriculture ») | Rapport « Prairies retournées » |
| **Prairies probables hors PAC :** herbe agricole bétonnée hors parcelle déclarée, comptée en borne haute | L'ignorer | Prés de petits éleveurs, chevaux de loisir | 456 ha/an, plus du double du béton sur prairies déclarées (210 ha/an). Part du béton : 2,1 à 6,4 % |
| **Ventilation du béton selon l'EPCI du polygone de béton** | Selon l'EPCI de la parcelle | Le total et sa ventilation s'additionnent toujours, même en limite d'EPCI | Correction appliquée. Aucune valeur négative avant comme après ; effet inférieur à 0,1 % |
| **Désartificialisation affichée = « sols rendus » seulement** | Toute désartificialisation de l'IGN | Une surface restée en herbe dont seul l'usage change n'est pas une renaturation | Orne : 212 ha venaient de deux polygones de fin de chantier (T7) |
| **Pas de kilomètres de haies bétonnées.** On compte à la place les zones boisées d'avant le béton (OCS GE) | Couche nationale des haies | Son édition 2026 ne montre plus les haies détruites entre 2019 et 2023 | Métadonnées de l'IGN (T8) |

## 4. Rattachement géographique et périodes

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Rattachement par **point intérieur** (`ST_PointOnSurface`), à défaut à la **commune la plus proche** | Découper chaque parcelle entre les communes | Simple et rapide. Les parcelles débordent rarement d'une commune | Surface tombant dans un autre EPCI : 0,37 %, borne haute à cause des contours simplifiés. Parcelles sans commune : 1 % de la surface, à moins de 500 m en médiane |
| **Annualisation par département** sur sa propre fenêtre OCS GE (2019-2022 ou 2020-2023) | Comparer des totaux sur 3 ans | Les fenêtres diffèrent selon les départements | L'EPCI à cheval sur deux fenêtres (Honfleur-Beuzeville) est marqué « mixte » |
| EPCI à cheval sur une autre région : **partie normande seulement**, avec le périmètre affiché. **Exclusion des comparaisons au-delà de 50 % de surface hors Normandie** | Ajouter les départements voisins ; supprimer ces EPCI | Choix de l'équipe : version légère. Les supprimer ferait perdre des hectares normands dans les totaux | Dreux et Maine Saosnois (95 % hors Normandie) sont exclus des comparaisons ; Alençon, Villes Sœurs et Aumale-Blangy sont comparés avec la mention de leur périmètre (T8) |

## 5. Milieux remarquables (bloc D)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Zones humides : **deux sources affichées séparément**, l'inventaire DREAL (avéré) et le modèle MPH de l'INRAE (potentiel) | Une seule source | L'inventaire est hétérogène selon les territoires ; le modèle surestime | Béton : 57 ha/an en zones inventoriées, 343 ha/an en zones potentielles |
| Modèle MPH : **classes de confiance 1 à 3** | Classe 3 seulement | Les trois classes sont de taille égale au sein de l'enveloppe (notice INRAE) | Le béton en zone potentiellement humide se répartit à 37 % en classe 1, 39 % en classe 2 et 23 % en classe 3 |
| **Natura 2000 présenté comme « dans un site », jamais comme une infraction** | Prairies sensibles retournées par EPCI | La PAC n'interdit que le retournement des prairies sensibles. Le rattachement est approximatif, et un tel chiffre serait lu comme une accusation | 1 590 ha retournés en Natura 2000 en 9 ans, dont 168 ha (11 %) sur une prairie sensible actuelle (T9) |

## 6. Trajectoire ZAN et efficacité (bloc E)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **Trajectoire de référence nationale** (moitié de 2011-2021 pour 2021-2031) | Objectifs territorialisés du SRADDET | Ces objectifs ne sont pas disponibles en données ouvertes par EPCI, et la loi TRACE est en débat | À afficher comme « trajectoire de référence » |
| **Alerte « flux unique »** : un flux d'au moins 20 ha et d'au moins 50 % de la consommation 2021-2025, avec la projection sans ce flux | Accepter les projections brutes | Un site enregistré tardivement au cadastre peut fausser la projection | Les Ventes-de-Bourse : 52 ha au cadastre en 2022-2023 pour un site déjà artificialisé selon l'OCS GE (T9) |
| **Ratios logements et emplois par hectare vides sous 1 ha consommé** | Ratio toujours calculé | Un dénominateur trop petit donne un ratio sans signification | 3 EPCI concernés |

## 7. Profils de comparaison (bloc F)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **4 profils par règles simples :** densité ≥ 300 / 100 hab/km², prairies permanentes ≥ 20 % du territoire | Classification statistique ; classement de toute la région | Lisible par un élu. On compare l'EPCI à des territoires semblables plutôt qu'à toute la région | Effectifs : 5 urbains, 21 périurbains, 25 ruraux herbagers, 20 ruraux de grandes cultures |
| Seuil herbager à **20 %** | 30 % | Le seuil de 30 % classait le Bocage virois, Flers et le Domfrontais en « grandes cultures » | **Sensible :** un seuil à 15, 25 ou 30 % fait changer de profil 8, 10 ou 15 EPCI. Le seuil périurbain à 80 ou 150 en fait changer 6 ou 11. **À faire valider par les experts** |

## 8. Friches (écran 2)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **Potentiel écologique calculé par nous**, faisabilité = **score de l'EPF** | Utiliser le seul score de l'EPF ; recalculer la faisabilité | Le score de l'EPF (méthode ADEME) ne regarde pas l'écologie. Ses attributs environnementaux sont lacunaires (zone humide vide à 90 %) | Corrélation de 0,31 entre les deux scores : ils mesurent des choses différentes |
| **4 critères en rangs centiles, préréglage biodiversité** (0,35 / 0,20 / 0,30 / 0,15) | Optimisation (Zonation, prioritizr) | Transparent et réglable dans l'interface (manuel OCDE/JRC des indicateurs composites) | Avec des poids égaux, on retrouve 77 % des mêmes « gains rapides » (Jaccard 0,767) |
| **Rayon de 500 m** pour les prairies autour | 300 m ou 1 000 m | Échelle de voisinage paysager | Jaccard 0,79 à 300 m et 0,76 à 1 000 m |
| « Gain rapide » = **potentiel ≥ 75e centile et faisabilité ≥ médiane**, sur les friches d'au moins **0,1 ha** sans projet engagé | Seuil au 70e centile, sans seuil de surface (1 009 gains rapides, dont 341 de moins de 0,1 ha) | Une sélection resserrée et significative à l'échelle d'un EPCI | Jaccard 0,85 au 70e centile et 0,82 au 80e. Surface 0,05 ha : 0,78. Surface 0,5 ha : 0,34, car ce seuil retire volontairement les friches moyennes |
| **Noyau stable** à mettre en avant | Liste brute | Les friches qui restent en tête quelle que soit la variante sont les plus défendables | **281 friches sur 413 (481 ha sur 635)** restent en « gain rapide » dans toutes les variantes : seuils, rayon, poids égaux |
| Colonne **vigilance** : pollution avérée, potentielle, non connue ou non renseignée ; terrain constructible ; zone inondable | Ne rien signaler | « Non connue » ne veut pas dire « saine » | Le site Bottu/Sanofi n'avait aucune vigilance avant correction (T10) |

## 9. Ce qui reste à valider

| Point | Moyen | Statut |
|---|---|---|
| Fiabilité de la détection des retournements | Lecture à l'aveugle de 100 retournements (50 prairies anciennes, 50 récentes) et 50 témoins, sur une photo IGN de l'année même de la première culture déclarée, avec `data/validation/lecture.html` ; règle de calcul fixée avant lecture (`data/validation/LISEZ-MOI.md`) ; quelques heures à se répartir | **À faire par l'équipe** |
| Seuils des profils (herbager 20 %, densités 100 et 300) | Point d'étape avec les experts | À valider |
| Poids et seuils des friches | Point d'étape avec les experts ; EPF Normandie | À valider |
| Lecture de la trajectoire ZAN | Région et DREAL : quelle base afficher ? | À valider |

## 10. Reproduire les preuves

```
.venv\Scripts\python.exe src\telecharger_donnees.py
.venv\Scripts\python.exe src\pipeline.py
.venv\Scripts\python.exe src\sensibilite.py
.venv\Scripts\python.exe src\sensibilite_prl.py
.venv\Scripts\python.exe src\echantillon_validation.py
.venv\Scripts\python.exe src\preparer_lecture.py
.venv\Scripts\python.exe src\resultat_validation.py
```

Les comptes rendus T1 à T10 (dossier `tests/`) détaillent chaque test.
