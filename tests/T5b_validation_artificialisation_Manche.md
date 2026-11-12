# Test T5b : validation de la règle d'artificialisation contre la couche officielle de l'IGN (Manche)

Date : 18/10/2026. Résultat : **notre approximation est bonne, mais elle est remplacée par la couche officielle**, qui est plus fiable et plus légère. Les conclusions du test T5 ne changent pas.

## La couche officielle

- **Ressource IGN :** `OCSGE-ARTIFICIALISATION`, fichier `OCS-GE-ARTIFICIALISATION_2-0_DIFF-2019-2022_GPKG_LAMB93_D050_2025-09-16`. L'archive 7z fait **1,4 Mo** (MD5 vérifié) et contient `zan_evol_2019_2022_50.gpkg` (4,7 Mo).
- **Deux autres fichiers existent**, inutiles pour nous : l'artificialisation complète de 2019 et celle de 2022.
- **Attributs :** `cs_`, `us_` et `artif_` (« artif » ou « non artif ») pour chaque année, plus `artificialisation` et `surface`. Le champ `artificialisation` vaut +1 pour une surface artificialisée, −1 pour une surface désartificialisée.
- **Manche, 2019 → 2022 :** **782 ha artificialisés** (5 943 polygones) et **114 ha désartificialisés**, soit un solde net de 668 ha.

## Comparaison avec notre règle couverture × usage

| | Surface (ha) |
|---|---|
| Notre approximation | 822 |
| Couche officielle | 782 |
| Surface commune | 763 |

- **Rappel : 97,5 %.** C'est la part de l'artificialisation officielle que notre règle retrouve.
- **Précision : 92,8 %.** C'est la part de notre artificialisation que l'IGN confirme.

**Pourquoi une règle maison ne suffit pas :** 14 couples couverture/usage sont classés tantôt « artif », tantôt « non artif » par l'IGN. C'est le cas par exemple de CS2.2.1/US1.1, CS2.2.1/US6.3, CS1.1.2.1/US1.1 et CS2.1.1.1/US5. L'IGN applique donc des critères en plus du couple CS/US, sans doute des seuils de surface ou d'enclavement et des exemptions.

Principaux écarts, en ha sur les deux années :
- herbacé agricole classé « artif » par l'IGN : 6 ha ;
- herbacé sans usage classé « artif » : 5,9 ha ;
- arbres en zone résidentielle classés « artif » : 4 ha ;
- surfaces minérales agricoles (chemins, cours) classées « non artif » : 3,3 ha.

## Décision

- **`src/beton_charrue_epci.py` lit maintenant directement la couche officielle** (`artificialisation = 1`). Notre règle approximative est supprimée.
- **Résultat après correction :**
  - béton : 782 ha, dont **197 ha sur des prairies permanentes** déclarées (198 ha avant), 26 ha sur des prairies temporaires, 87 ha sur des cultures et 472 ha hors RPG ;
  - charrue : inchangée, avec 11 069 ha toutes prairies permanentes et 4 442 ha de prairies anciennes ;
  - **part du béton dans les pertes de prairies permanentes : 1,7 %**, contre 1,8 % avant.
- **Bonus pour le produit :** la couche officielle donne aussi la **désartificialisation** (114 ha dans la Manche). C'est exactement le « rendre à la nature » du titre, à afficher face au béton.
- **Argument de pitch :** le chiffre d'artificialisation de l'outil est celui de l'IGN, conforme au décret 2023-1096. Il est donc opposable dans le suivi du ZAN.

## Pour les autres départements

La même ressource existe par département (`zone=D014`, `D027`, `D061`, `D076`). Les fenêtres attendues sont 2019-2022 pour l'Eure et la Seine-Maritime, et 2020-2023 pour le Calvados et l'Orne. Elles sont à confirmer lors du téléchargement.
