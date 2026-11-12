# Registre des choix méthodologiques

Date : 01/11/2026, mis à jour le 10/11/2026 (chiffre principal en prairies anciennes, section 2 ; corrections des sections 4, 5, 8 et 9) et le 11/11/2026 (repère foncier national sans verdict, section 6). Ce registre liste chaque choix qui influe sur les chiffres de l'outil. Pour chacun, il donne l'alternative écartée, la justification et la preuve (mesure, test, source). Il sert à la page « méthode » et aux réponses au jury.

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
| **Chiffre principal = prairies anciennes** (constat, carte, rang par profil, herbier, trajectoires) ; toutes les prairies en borne haute | Toutes les prairies permanentes en tête | Depuis la règle des 5 ans, « toutes » contient des prairies semées dans une rotation et reclassées permanentes, surtout en 2018 : leur retournement n'est pas la perte d'une prairie ancienne. Le décompte le plus prudent va en tête, le plus large en borne haute. Le béton est compté de la même façon, sur les prairies anciennes | Décision du 10/11/2026. Sur la fenêtre OCS GE : charrue 5 166 ha/an (anciennes) contre 9 695 (toutes) ; béton 155 ha/an contre 210 ; part du béton 2,9 à 10,6 % contre 2,1 à 6,4 % ; perte de 0,99 % du stock d'anciennes par an contre 1,49 %. 24 EPCI sur 69 changent de trois places ou plus dans leur profil (Mont-Saint-Michel-Normandie : 3e -> 10e des ruraux herbagers) |
| **Trois niveaux :** prairies anciennes, toutes prairies, borne haute | Un seul chiffre | Le reclassement PAC de 2018 a fait passer d'un coup +42 000 ha de prairies temporaires en permanentes dans la Manche. La refonte du RPG de 2023 a fait disparaître le code PRL | Classement des EPCI « prairies anciennes » contre « toutes prairies », chacun rapporté à son stock : Spearman 0,83. Borne basse contre borne haute (avec les prairies hors PAC) : 0,85 |
| **Prairie ancienne** = prairie permanente chaque année de 2015 à N, même définition partout | Prairie permanente au début de la période | Elle écarte les prairies reclassées en 2018 | La définition était différente dans `beton_charrue_epci.py` ; c'est harmonisé, avec un effet inférieur à 1 % |
| **Mise en gel (groupe 11) hors des cultures**, comptée dans la borne haute | Gel compté comme culture | Une mise en gel n'implique pas forcément un labour | 774 ha sur 71 508 ha (1,1 %). Correction appliquée : la charrue baisse de 1,2 % |
| **Sortie de la PAC = devenir inconnu**, jamais comptée comme retournement | La compter comme perte | On ne sait pas ce que devient la parcelle (vente, exploitant non déclarant, artefact de 2023) | 10 000 ha de prairies permanentes non déclarées en 2023 dans la seule Manche (T2) |
| **Retournements répétés comptés à chaque fois** (on compte des événements de labour) | Surface distincte | Chaque labour est une perte de couvert. L'indicateur « prairies anciennes » n'est pas concerné | 937 ha (1,3 %), sur 573 parcelles |
| **Béton prioritaire sur la charrue** | Compter les deux | Ne rien compter deux fois | Recouvrement mesuré : environ 1 ha dans la Manche (T5) |

## 3. Béton

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Ce qu'il y avait avant le béton = **culture déclarée l'année de début** | Couverture OCS GE seule | L'OCS GE confond prairie et culture (même couverture « herbacé », même usage « agriculture ») | Rapport « Prairies retournées » |
| **Prairies probables hors PAC :** herbe agricole bétonnée hors parcelle déclarée, comptée en borne haute | L'ignorer | Prés de petits éleveurs, chevaux de loisir | 456 ha/an, plus du double du béton sur prairies déclarées (210 ha/an). Part du béton : 2,9 à 10,6 % en prairies anciennes, 2,1 à 6,4 % avec toutes les prairies |
| **Ventilation du béton selon l'EPCI du polygone de béton** | Selon l'EPCI de la parcelle | Le total et sa ventilation s'additionnent toujours, même en limite d'EPCI | Correction appliquée. Aucune valeur négative avant comme après ; effet inférieur à 0,1 % |
| **Désartificialisation affichée = « sols rendus » seulement** | Toute désartificialisation de l'IGN | Une surface restée en herbe dont seul l'usage change n'est pas une renaturation | Orne : 212 ha venaient de deux polygones de fin de chantier (T7) |
| **Pas de kilomètres de haies bétonnées.** On compte à la place les zones boisées d'avant le béton (OCS GE) | Couche nationale des haies | Son édition 2026 ne montre plus les haies détruites entre 2019 et 2023 | Métadonnées de l'IGN (T8) |

## 4. Rattachement géographique et périodes

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Rattachement par **point intérieur** (`ST_PointOnSurface`), à défaut à la **commune la plus proche** | Découper chaque parcelle entre les communes | Simple et rapide. Les parcelles débordent rarement d'une commune | Surface tombant dans un autre EPCI : 0,37 %, borne haute à cause des contours simplifiés. Parcelles sans commune : 1 % de la surface, à moins de 500 m en médiane |
| **Annualisation par département** sur sa propre fenêtre OCS GE (2019-2022 ou 2020-2023) | Comparer des totaux sur 3 ans | Les fenêtres diffèrent selon les départements | L'EPCI à cheval sur deux fenêtres (Honfleur-Beuzeville) est marqué « mixte » |
| Perte en % du stock : **stock du début de la fenêtre OCS GE**, celui des prairies anciennes pour le chiffre principal | Stock de 2015 | Les pertes et le stock doivent porter sur les mêmes années et les mêmes prairies. Le stock de 2015 ne contient pas les prairies reclassées permanentes en 2018, alors que leurs retournements étaient au numérateur | Correction du 10/11/2026. Toutes prairies, région : 1,64 -> 1,49 % par an ; Mont-Saint-Michel-Normandie : 3,53 -> 2,58 % (son stock passe de 31 477 à 43 127 ha). Stock de prairies anciennes au début de la fenêtre : 536 192 ha, égal à celui de `cohorte_epci.csv` à moins de 1 ha par EPCI |
| Herbier, part du stock de 2015 retournée ou bétonnée : **prairies anciennes seulement** | Toutes les prairies permanentes | Seules les prairies restées permanentes depuis 2015 viennent toutes de ce stock | Correction du 10/11/2026. Charrue, région : 12,1 % affiché avant, 7,3 % après. Mont-Saint-Michel-Normandie : 24 % avant, 7 % après |
| EPCI à cheval sur une autre région : **partie normande seulement**, avec le périmètre affiché. **Exclusion des comparaisons au-delà de 50 % de surface hors Normandie** | Ajouter les départements voisins ; supprimer ces EPCI | Choix de l'équipe : version légère. Les supprimer ferait perdre des hectares normands dans les totaux | Dreux et Maine Saosnois (95 % hors Normandie) sont exclus des comparaisons ; Alençon, Villes Sœurs et Aumale-Blangy sont comparés avec la mention de leur périmètre (T8) |

## 5. Milieux remarquables (bloc D)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Zones humides : **deux sources affichées séparément**, l'inventaire DREAL (avéré) et le modèle MPH de l'INRAE (potentiel) | Une seule source | L'inventaire est hétérogène selon les territoires ; le modèle surestime | Béton : 57 ha/an en zones inventoriées, 291 ha/an en zones potentielles, soit 21 % du béton. L'enveloppe potentielle couvre 22 % de la région : le béton n'y est donc pas surreprésenté. Correction du 10/11/2026 : le calcul précédent (343 ha/an) retirait du dénominateur les pixels hors enveloppe, et un polygone touchant un seul pixel humide valait 100 % (`part_mph` dans `src/geo_utils.py`) |
| Modèle MPH : **classes de confiance 1 à 3** | Classe 3 seulement | Les trois classes sont de taille égale au sein de l'enveloppe (notice INRAE) | Le béton en zone potentiellement humide se répartit à 37 % en classe 1, 39 % en classe 2 et 23 % en classe 3 |
| **Natura 2000 présenté comme « dans un site », jamais comme une infraction** | Prairies sensibles retournées par EPCI | La PAC n'interdit que le retournement des prairies sensibles. Le rattachement est approximatif, et un tel chiffre serait lu comme une accusation | 1 590 ha retournés en Natura 2000 en 9 ans, dont 168 ha (11 %) sur une prairie sensible actuelle (T9) |

## 6. Trajectoire ZAN et efficacité (bloc E)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **Repère national, affiché sans verdict** : la moitié de la consommation 2011-2020 pour 2021-2030, d'après les fichiers fonciers du Cerema | Objectifs territorialisés du SRADDET, recalculés par nous | L'objectif réel d'un territoire n'est pas -50 %. Le SRADDET modifié (voté le 25/03/2024) fixe un taux par périmètre de territorialisation (SCoT ou groupe d'EPCI), appliqué à la consommation 2011-2020 mesurée par la CCF de l'EPF Normandie, puis réduit de 15 % pour une enveloppe régionale mutualisée. Les taux sont dans la règle 21 du fascicule (PDF), pas en données ouvertes par EPCI ; la CCF pèse 1 à 3,3 Go par millésime et s'arrête fin 2023. Reproduire ce calcul sans l'aide de la Région risquerait de donner d'autres chiffres que les siens | Décision du 11/11/2026. L'outil ne dit plus « enveloppe dépassée » ni date d'atteinte : il donne la consommation 2021-2024 en % du repère et explique la règle de la Région, avec ses sources. Le bilan annuel 2025 de la Région ne juge pas non plus les trajectoires : elle ne disposait que des millésimes 2021 et 2022 de la CCF |
| **Alerte « flux unique »** : un flux d'au moins 20 ha et d'au moins 50 % de la consommation 2021-2025, avec la projection sans ce flux | Accepter les projections brutes | Un site enregistré tardivement au cadastre peut fausser la projection | Les Ventes-de-Bourse : 52 ha au cadastre en 2022-2023 pour un site déjà artificialisé selon l'OCS GE (T9) |
| **Ratios logements et emplois par hectare vides sous 1 ha consommé** | Ratio toujours calculé | Un dénominateur trop petit donne un ratio sans signification | 3 EPCI concernés |

Sources pour le SRADDET : [objectif 4 bis du SRADDET modifié](https://normandie-a-la-carte.normandie.fr/sobriete_fonciere/objectif_sraddet/o4bis.pdf) ; [bilan annuel 2025 de la conférence régionale de gouvernance du ZAN](https://www.normandie.fr/sites/default/files/2026-04/bilan_enaf_2025.pdf) ; [CCF sur DataNormandie](https://www.datanormandie.fr/visualisation/information/?id=cartographie_de_la_consommation_fonciere_ccf). La table des taux (règle 21) n'a pas été relevée.

## 7. Profils de comparaison (bloc F)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **4 profils par règles simples :** densité ≥ 300 / 100 hab/km², prairies permanentes ≥ 20 % du territoire | Classification statistique ; classement de toute la région | Lisible par un élu. On compare l'EPCI à des territoires semblables plutôt qu'à toute la région | Effectifs : 5 urbains, 21 périurbains, 25 ruraux herbagers, 20 ruraux de grandes cultures |
| Seuil herbager à **20 %** | 30 % | Le seuil de 30 % classait le Bocage virois, Flers et le Domfrontais en « grandes cultures » | **Sensible :** un seuil à 15, 25 ou 30 % fait changer de profil 8, 10 ou 15 EPCI. Le seuil périurbain à 80 ou 150 en fait changer 6 ou 11. **À faire valider par les experts** |

## 8. Friches (écran 2)

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| **Potentiel écologique calculé par nous**, faisabilité = **score de l'EPF** | Utiliser le seul score de l'EPF ; recalculer la faisabilité | Le score de l'EPF (méthode ADEME) ne regarde pas l'écologie. Ses attributs environnementaux sont lacunaires (zone humide vide à 90 %) | Corrélation de 0,31 entre les deux scores : ils mesurent des choses différentes |
| **4 critères en rangs centiles, préréglage biodiversité** (0,35 / 0,20 / 0,30 / 0,15) | Optimisation (Zonation, prioritizr) | Transparent et réglable dans l'interface (manuel OCDE/JRC des indicateurs composites) | Avec des poids égaux, on retrouve 76 % des mêmes « gains rapides » (Jaccard 0,757). La part humide vient de la même correction que le béton (section 5) : 186 friches avaient une part surestimée de plus de 25 points ; 8 sortent des « gains rapides » et 10 y entrent |
| **Rayon de 500 m** pour les prairies autour | 300 m ou 1 000 m | Échelle de voisinage paysager | Jaccard 0,80 à 300 m et 0,77 à 1 000 m |
| « Gain rapide » = **potentiel ≥ 75e centile et faisabilité ≥ médiane**, sur les friches d'au moins **0,1 ha** sans projet engagé | Seuil au 70e centile, sans seuil de surface (1 009 gains rapides, dont 341 de moins de 0,1 ha) | Une sélection resserrée et significative à l'échelle d'un EPCI | Jaccard 0,85 au 70e centile et 0,81 au 80e. Surface 0,05 ha : 0,79. Surface 0,5 ha : 0,34, car ce seuil retire volontairement les friches moyennes |
| **Noyau stable** à mettre en avant | Liste brute | Les friches qui restent en tête quelle que soit la variante sont les plus défendables | **283 friches sur 415 (457 ha sur 672)** restent en « gain rapide » dans toutes les variantes : seuils, rayon, poids égaux |
| Colonne **vigilance** : pollution avérée, potentielle, non connue ou non renseignée ; terrain constructible ; zone inondable | Ne rien signaler | « Non connue » ne veut pas dire « saine » | Le site Bottu/Sanofi n'avait aucune vigilance avant correction (T10) |

## 9. Trajectoires (« Et si… »)

Ce sont des trajectoires conditionnelles, pas des prévisions. Seules T1 et F1 prolongent des données observées ; T2, T3, F2 et F3 traduisent des hypothèses.

| Choix retenu | Alternative écartée | Justification | Preuve |
|---|---|---|---|
| Suivre la **cohorte des prairies anciennes**, et seulement la part labourée | Tracer le total des prairies permanentes ; tracer toute la baisse de la cohorte | Le total monte avec les reclassements (604 000 ha en 2015, 620 000 en 2024). La cohorte a perdu 140 000 ha, dont 44 000 par la charrue : le reste a surtout quitté les déclarations, au devenir inconnu | RPG Explorer 2018 : 676 152 ha, contre 673 869 ha publiés par le ministère (0,3 % d'écart) |
| **Rythme de labour sans tendance,** années futures tirées parmi 2017-2024 | Tendance linéaire ; modèle statistique | 8 années seulement, avec des ruptures en 2018 et 2023. 2016 est écartée : la cohorte n'y a qu'un an d'ancienneté. Les deux années les plus basses, 2018 (0,44 % de la cohorte labourée) et 2024 (0,41 %, contre 0,8 à 1,4 % les autres années), tombent sur des campagnes où la PAC restreignait les retournements (voir T2) : T1 prolonge donc aussi ces restrictions. Coïncidence **à faire confirmer par la DRAAF** | Pente de -0,003 point par an. Épreuves sur le passé, écart régional : +4,7 %, -1,7 % et -6,8 % à taux moyens (`trajectoires_validation.csv`), environ +2 %, -4 % et -10 % pour la médiane du bootstrap, qui est le chiffre publié (`glmm_validation.csv`) |
| **Rythme de chaque EPCI rapproché de celui de son profil,** total régional conservé | Taux propre de l'EPCI | Un petit EPCI a des années très irrégulières | Erreur médiane par EPCI : 21 à 25 %, contre 28 à 31 % avec le taux propre, sur les trois épreuves |
| **Fourchette à deux niveaux de tirage,** élargie pour les EPCI (K = 1,31) | Fourchette brute | Avant élargissement, seuls 83 à 85 % des EPCI restaient dans une fourchette annoncée à 90 % | Facteur appris sur deux épreuves et vérifié sur la troisième : 87 à 93 % |
| **Bootstrap conservé pour les trajectoires** | Modèle logistique hiérarchique bayésien (profil + EPCI + année + cellule) | Règle fixée avant les résultats : au moins 2 épreuves sur 3 gagnées en score d'intervalle et en CRPS, sans couverture plus éloignée de 90 % que le bootstrap élargi | `glmm_validation.csv` : modèle prévu, 0 épreuve sur 3, couverture de 100 %, intervalles trop larges (score moyen 2,74 contre 1,47). Variante à a priori plus serré sur l'effet année, élargie : 2 épreuves sur 3, mais couverture plus éloignée (2,4 points contre 1,9). Médianes par EPCI très proches : Spearman 0,995 |
| **Autres sorties retirées du stock,** jamais comptées comme des labours ; celles de 2023 remplacées par la moyenne | Les ignorer | Une prairie sortie des déclarations ne peut plus être comptée comme labourée. 2023 reflète en partie la refonte du RPG | Sans ces sorties : +7,3 % de labour en 2035 |
| **T2 = plus de labour dans les zones reconnues et les milieux potentiellement humides** | « Ce qui est déjà décidé » ; zones reconnues seules | Le filet de la PAC porte sur un ratio régional, sans cible par territoire : son effet sur la cohorte d'un EPCI ne se chiffre pas. Il a pourtant joué en Normandie : régime d'autorisation en 2017 (ratio à -3,55 %, référence 2012), puis régime d'interdiction décidé fin 2023 (-6,45 %, référence 2018) et levé rétroactivement fin 2024, après retraitement du ratio (-0,79 %). Les zones reconnues sont déjà peu labourées | Zones reconnues : 7,4 % du labour pour 27 % du stock (0,24 % par an, contre 1,14 % ailleurs), soit -7,3 % en 2035. Avec les MPH : -20,9 %. Un rythme plus bas ne prouve pas qu'une protection agit |
| **T3 = au plus 5 % de la cohorte labourés d'ici 2035, par EPCI** | Objectif régional réparti sans règle | Exemple : l'objectif revient à la Région. L'intérêt est de montrer l'effort requis par territoire | 66 EPCI sur 71 auraient un effort à faire ; -46 % au total |
| **F2 = au moins 20 logements par ha** ; F3 = rythme qui s'en tient au repère national | Dates et densités d'un SRADDET territorialisé | Exemple : le repère est national, pas l'objectif du territoire (voir section 6), et la loi TRACE est en débat. Au-delà de 100 logements par ha, la densité requise n'est pas affichée | À 20 logements par ha : 130 % du repère fin 2030, contre 172 % |
| **Horizon 2035** | 2050 | Neuf années de données ne permettent pas de projeter beaucoup plus loin | 2024, année basse : sans elle, +6,9 % de labour en 2035 ; calibration 2019-2024 : +8,4 % |

Sources pour le ratio régional de la PAC : [Terre-net, 10/11/2017](https://www.terre-net.fr/reglementation/article/132187/la-normandie-et-les-hauts-de-france-epingles-pour-retournement-excessif) (régime d'autorisation) ; [Réussir, 06/11/2023](https://www.reussir.fr/lait/prairies-permanentes-4-regions-en-regime-dautorisation-ou-dinterdiction) (arrêté du 31/10/2023) ; [Réussir, 03/12/2024](https://www.reussir.fr/lait/prairies-permanentes-larrete-sur-lassouplissement-des-regles-est-sorti) (arrêté du 25/11/2024). Ce sont des articles de presse : les arrêtés eux-mêmes restent à relire.

## 10. Ce qui reste à valider

| Point | Moyen | Statut |
|---|---|---|
| Objectif de T3 et densité de F2 | Région, DRAAF, DREAL | Valeurs d'exemple, **à remplacer** |
| Cause du rythme très bas de 2024 | Régime d'interdiction de retournement décidé fin 2023 (arrêté du 31/10/2023), levé rétroactivement par l'arrêté du 25/11/2024. À confirmer avec la DRAAF, avec la part de l'hiver humide et de la refonte du RPG | Explication probable, **à confirmer** |
| Fiabilité de la détection des retournements | Lecture à l'aveugle de 100 retournements (50 prairies anciennes, 50 récentes) et 50 témoins, sur une photo IGN de l'année même de la première culture déclarée, avec `data/validation/lecture.html` ; règle de calcul fixée avant lecture (`data/validation/LISEZ-MOI.md`) ; quelques heures à se répartir | **À faire par l'équipe** |
| Seuils des profils (herbager 20 %, densités 100 et 300) | Point d'étape avec les experts | À valider |
| Poids et seuils des friches | Point d'étape avec les experts ; EPF Normandie | À valider |
| Objectifs ZAN réels par territoire | Obtenir de la Région les taux de la règle 21 par EPCI et la consommation CCF agrégée, pour remplacer le repère national | **Besoin pour changer d'échelle** |

## 11. Reproduire les preuves

```
.venv\Scripts\python.exe src\telecharger_donnees.py
.venv\Scripts\python.exe src\pipeline.py
.venv\Scripts\python.exe src\sensibilite.py
.venv\Scripts\python.exe src\sensibilite_prl.py
.venv\Scripts\python.exe src\cohorte_epci.py data\processed\cohorte_epci.csv
.venv\Scripts\python.exe src\trajectoires.py
.venv\Scripts\python.exe src\validation_glmm.py
.venv\Scripts\python.exe src\echantillon_validation.py
.venv\Scripts\python.exe src\preparer_lecture.py
.venv\Scripts\python.exe src\resultat_validation.py
```

Les comptes rendus T1 à T10 (dossier `tests/`) détaillent chaque test.
