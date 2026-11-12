# Test T1 : l'ANBDD fait-elle déjà « ce que le béton et la charrue ont pris » ?

Date : 18/10/2026. Résultat : **GO**. Le produit reste original, à présenter comme un complément de l'ANBDD.

## Ce qui a été fait

- Outil testé : l'application « Indicateurs territoriaux de la biodiversité » de l'ANBDD, une application Shiny intégrée à anbdd.fr : https://ithomas.shinyapps.io/Indicateurs_EPCI/
- EPCI testé : CC Coutances Mer et Bocage (Manche, territoire bocager).
- Rapports générés :
  - « Superficie Toujours en Herbe dans la Surface Agricole Utile » ;
  - « Occupation des sols ».
- L'Excel « Données » n'a pas été téléchargé : les rapports indiquent eux-mêmes leurs sources et leurs années.

## Ce que publie l'ANBDD

| Indicateur | Source | Années | Maille | Nature |
|---|---|---|---|---|
| Superficie toujours en herbe (STH) dans la SAU | Recensements agricoles, traités par la DRAAF | 1970, 1979, 1988, 2000, 2010, 2020 | EPCI, département, région. Cartes communales issues du RPG 2020, à cause du secret statistique | **Stock net, tous les 10 ans** |
| Occupation des sols | OSCOM (DRAAF), 2008-2020 | 2008 et 2020 | EPCI, avec cartes communales | **Stocks par grande classe et solde net par classe** |

Exemple pour la CC Coutances Mer et Bocage :
- **STH :** 25 342 ha en 2020, soit 55 % de la SAU ; −353 ha entre 2010 et 2020.
- **Occupation des sols, 2008-2020 :** territoires agricoles −436 ha, territoires artificialisés +496 ha.
- **Artefact à noter :** les recensements font apparaître une hausse de la STH dans la Manche (+7 %) entre 2010 et 2020. Le rapport l'explique par un reclassement des prairies permanentes en prairies temporaires lors de la PAC 2010. Un stock net peut donc masquer les retournements.

## Ce que l'ANBDD ne fait pas, et que notre produit apporte

1. **Des flux bruts annuels** (RPG, de 2015 à 2025) au lieu d'un stock net tous les dix ans, ou sur 2008-2020.
2. **La cause de la perte**, en séparant béton et charrue, par EPCI et par année. L'ANBDD donne des soldes par classe, sans matrice de transitions.
3. **La qualité de ce qui a été consommé** : haies, zones humides potentielles, ZNIEFF.
4. **Des données récentes** : 2021-2025, quand l'ANBDD s'arrête en 2020.
5. **Une mise à jour annuelle** possible à chaque nouveau RPG.

## Conséquences pour le projet

- Positionnement pour le pitch : *« La suite annuelle et détaillée des indicateurs de l'ANBDD et de l'étude Agreste 2021 : non plus combien de prairies il reste, mais ce qui les a fait disparaître, chaque année. »* Citer l'ANBDD comme référence, pas comme concurrent.
- Argument méthodologique : l'exemple de la Manche montre qu'un stock net peut masquer les retournements, d'où l'intérêt de flux bruts accompagnés d'une borne haute.
- Piste à creuser : l'ANBDD exploite les données communales OSCOM 2008-2020. Demander à la DRAAF ou à l'ANBDD si ces tables sont diffusables, pour remonter avant 2015.
- Contact ANBDD, chargée de mission scientifique : Iuna Thomas, iuna.thomas@anbdd.fr. Possible relecture ou futur hébergeur du produit (« changer d'échelle »).

## Prochain test

T2 : RPG Explorer (INRAE), successions de cultures 2015-2024 pour la Manche.
