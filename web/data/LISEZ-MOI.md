# Données de l'interface

Fichiers produits par `src/export_web.py`, à ne pas modifier à la main. Pour les refaire :

```
.venv\Scripts\python.exe src\export_web.py
```

Toutes les données sont des agrégats ou des friches publiées par l'EPF Normandie. Aucune parcelle agricole n'y figure.

## Quel fichier charger, et quand

| Fichier | Taille (compressé) | Quand le charger | Contenu |
|---|---|---|---|
| `regional.json` | 8 Ko (3 Ko) | Au démarrage | Totaux normands, série annuelle, trajectoires, profils, sources, avertissements |
| `epci_index.json` | 46 Ko (6 Ko) | Au démarrage | Une ligne par EPCI : recherche, tableau, couleur de la carte |
| `epci_contours.geojson` | 265 Ko (77 Ko) | Au démarrage de la carte | Contours des 71 EPCI, en WGS 84, avec `code` et `nom` |
| `epci/<code>.json` | 6 Ko au plus | Au clic sur un EPCI | Fiche complète, avec les trajectoires |
| `friches.geojson` | 618 Ko (61 Ko) | À l'ouverture de l'écran 2 | 2 864 points avec classe et scores |
| `friches/<code>.json` | 152 Ko au plus | Au clic sur un EPCI, écran 2 | Détail des friches, triées par score biodiversité décroissant |

Pour relier un contour à sa ligne : `properties.code` de `epci_contours.geojson` = `code` de `epci_index.json`. Pour une friche : `properties.epci` = `code`.

## Fiche d'un EPCI (`epci/<code>.json`)

Les noms de champs reprennent ceux de `tableau_regional_epci.csv`, décrits en tête de `src/tableau_regional.py`, `src/qualite_epci.py` et `src/sobriete_epci.py`. Une valeur absente vaut `null`.

| Bloc | Contenu |
|---|---|
| racine | `code`, `nom`, `departements`, `perimetre`, `hors_normandie`, `exclu_comparaisons`, `fenetre_ocsge` |
| `comparaison` | Profil de l'EPCI, rang parmi les EPCI du même profil, médianes du profil |
| `territoire` | Population, surface, densité, stock de prairies permanentes en 2015 (`stock_pp_2015`) et au début de la fenêtre OCS GE (`stock_pp_debut_fenetre`, et `stock_pp_anciennes_debut_fenetre` pour les seules prairies anciennes) |
| `charrue` | Moyenne 2015-2024 (`charrue_toutes_ha_an`, `charrue_anciennes_ha_an`), fourchette `*_sans_prl_ha_an`, part de PRL, valeurs sur la fenêtre OCS GE |
| `beton` | Total, sur prairies déclarées (toutes, et anciennes seulement), sur herbe hors PAC, hors RPG, sur zones boisées |
| `bilan` | Prairies anciennes perdues (`prairies_anciennes_perdues_ha_an`, basse et haute), part du béton, perte rapportée à leur stock du début de la fenêtre (`perte_anciennes_pct_stock_an`). Les mêmes champs sans « anciennes » comptent toutes les prairies permanentes |
| `sols_rendus` | Désartificialisation |
| `milieux_beton`, `milieux_charrue` | Zones humides, Natura 2000, ZNIEFF. Béton sur la fenêtre OCS GE ; charrue en moyenne 2015-2024, ou sur la fenêtre pour les champs `*_fen_ha_an` |
| `sobriete` | Trajectoire ZAN, logements et emplois créés par hectare |
| `friches` | Totaux de l'EPCI, petites friches comprises |
| `serie` | Par année (2016 = passage 2015 -> 2016) : `stock_pp`, `charrue_toutes`, `charrue_anciennes`, `borne_haute` |
| `trajectoires` | « Et si… » : voir ci-dessous |

## Trajectoires (« Et si… »)

Même bloc `trajectoires` dans `epci/<code>.json` et dans `regional.json`. Celui de la région ajoute `hypotheses` (paramètres utilisés) et `avertissements` (à afficher avec les courbes). Méthode en tête de `src/trajectoires.py`.

`fiabilite` vaut `exploitable`, `indicative` ou `fragile` selon la largeur de la fourchette. La région vaut `région`.

**`prairies`** porte sur les prairies déclarées permanentes sans interruption depuis 2015. `annees` va de 2025 à 2035. Trois blocs portent chacun `bas`, `median` et `haut`, trois listes de 11 valeurs en **hectares labourés cumulés depuis 2025** :

| Bloc | Hypothèse | Champs en plus |
|---|---|---|
| `on_laisse_faire` | Les années futures ressemblent à 2017-2024 | `pct_stock_2035`, `sans_prl_2035_ha` (sans les labours de PRL) |
| `proteger_fragile` | Plus de labour en zones reconnues ni en milieux potentiellement humides | `epargne_2035_ha` |
| `objectif` | Aucun territoire ne laboure plus que l'objectif d'ici 2035 | `epargne_2035_ha`, `effort_pct`, `labour_cible_ha_an` |

Le bloc contient aussi `stock_anciennes_2024_ha`, `taux_labour_pct_an`, `labour_actuel_ha_an`, `part_labour_zones_fragiles_pct` et `part_labour_prl_pct`.

**`foncier`** porte sur le repère foncier national (la moitié de la consommation 2011-2020, d'après le Cerema), jusqu'au 1/1/2031. Ce n'est pas l'objectif du territoire, que le SRADDET fixe avec un taux propre et une autre source (la CCF). Les champs gardent le mot « enveloppe » :

| Champ | Contenu |
|---|---|
| racine | `enveloppe_ha`, `conso_2021_2025_ha`, `reste_ha`, `rythme_actuel_ha_an`, `alerte_flux_unique`, `deja_depassee` |
| `on_laisse_faire` | `conso_2031_ha`, `bas`, `haut`, `pct_enveloppe`, `annee_atteinte`, `annee_atteinte_bas`, `annee_atteinte_haut` (années décimales : 2026,8 correspond à octobre 2026) |
| `densifier` | `conso_2031_ha`, `pct_enveloppe`, `part_habitat_pct`, `densite_actuelle_logements_ha` |
| `tenir_enveloppe` | `rythme_cible_ha_an`, `effort_pct`, `densite_requise_logements_ha` (`null` si densifier seul ne suffit pas) |

Ne pas afficher de verdict à partir de ces champs : ni « enveloppe dépassée », ni date d'atteinte (`deja_depassee`, `annee_atteinte*`). L'interface donne la consommation 2021-2024 en % du repère et rappelle la règle de la Région.

`epci_index.json` reprend pour la carte : `surface_km2`, `trajectoire_fiabilite`, `t1_2035_pct_stock`, `t3_effort_pct` et `f1_annee_atteinte`.

## Friches

`properties` de `friches.geojson` : `id`, `epci`, `ha`, `classe`, `bio`, `eau`, `ville` (scores 0-100 des trois préréglages), `faisabilite` (potentiel EPF), `robustesse` (%).

Valeurs de `classe` : `gain_rapide`, `fort_potentiel_contraintes`, `potentiel_modere`, `projet_engage`.

La classe est calculée avec le préréglage biodiversité. Un changement de préréglage dans l'interface doit changer l'ordre ou la couleur par score, mais pas la classe affichée.

## Règles d'affichage à respecter

- Le chiffre principal porte sur les prairies anciennes, déclarées permanentes sans interruption depuis 2015 : champs `*_anciennes_*`. Les champs « toutes prairies » sont la borne haute et s'affichent comme telle. Le rang et les médianes de profil sont calculés sur les prairies anciennes.
- Ne jamais afficher un rang ni une médiane si `exclu_comparaisons` vaut `true` (Pays de Dreux, Maine Saosnois).
- Pour un EPCI à cheval sur une autre région, afficher `perimetre` à côté des chiffres.
- Présenter la moyenne 2015-2024 de la charrue comme une fourchette : `charrue_anciennes_sans_prl_ha_an` à `charrue_anciennes_ha_an`, puis `charrue_toutes_ha_an` en borne haute.
- Pour comparer charrue et béton, n'utiliser que les mêmes années : `charrue_fenetre_ha_an`, `charrue_anciennes_fenetre_ha_an` et, par milieu, `charrue_*_fen_ha_an`. La fourchette sans PRL n'existe pas sur cette période.
- Pour dire quelle part du stock de 2015 a été retournée ou bétonnée (herbier), n'utiliser que `charrue_anciennes_ha_an` et `beton_sur_pp_anciennes_ha_an` : les champs « toutes prairies » comptent aussi des prairies reclassées permanentes en 2018, absentes de ce stock.
- Ne pas comparer 2019 aux autres années sans explication : le pic vient du reclassement PAC de 2018.
- Ne jamais présenter un retournement en Natura 2000 ou en ZNIEFF comme une infraction.
- « Pollution non connue » ne veut pas dire « site sain » : toujours afficher `vigilance`.
- Citer les sources de `regional.json` et afficher ses `avertissements` dans la page méthode.
- Toujours afficher une trajectoire avec sa fourchette, et ne présenter que `on_laisse_faire` comme une projection. Les autres sont des hypothèses.
- Si `fiabilite` vaut `fragile`, ne pas afficher de chiffre central pour les prairies : indiquer que le territoire a trop peu de données pour une projection.
- Présenter l'objectif et la densité cible comme des exemples tant que la Région ne les a pas fixés.
- Afficher `perimetre` à côté des trajectoires, et signaler `alerte_flux_unique` à côté du repère foncier.

## Choix de confidentialité

- **Les noms de friches ne sont pas repris :** certains contiennent un nom de personne, une adresse ou une mention de succession. `libelle` est reconstruit à partir de l'activité passée et de la commune.
- **Les 2 204 petites friches (moins de 0,1 ha) ne sont pas sur la carte,** car ce sont souvent des maisons. Elles restent comptées dans les totaux.
