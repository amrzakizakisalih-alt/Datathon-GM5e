# Descriptif du projet — Datathon Normandie 2026

Ce texte suit les rubriques du modèle des organisateurs (`contexte/Descriptif_projet_Datathon.docx`). Les passages entre crochets sont à compléter par l'équipe.

## Nom de la solution et membres qui portent le projet

**Béton & Charrue** — « Ce que le béton et la charrue ont pris »

Équipe : GM5e. Membres : PINEL Robin SECK Cheikh SHERADJ DRISSI Mouad ZAKI SALIH Amr

## Quelques mots-clés pour décrire la solution

Prairies permanentes · artificialisation des sols · intercommunalités · friches · renaturation · données ouvertes · cartographie · sobriété numérique

## Le problème auquel la solution répond

Les prairies anciennes sont l'un des milieux les plus utiles à la biodiversité, à l'eau et au stockage du carbone en Normandie. On les croit surtout menacées par l'urbanisation. Les données disent autre chose.

Entre 2019 et 2023, environ 5 300 hectares de prairies anciennes ont disparu chaque année en Normandie. Les constructions n'en expliquent que 3 à 11 %. Le reste est remis en culture : la surface concernée est 8 à 33 fois celle prise par les constructions.

Aujourd'hui, un élu ne dispose pas de ce constat pour son territoire. Les indicateurs publics donnent une surface de prairies tous les dix ans, sans dire ce qui les fait disparaître ni où. La consommation foncière, elle, est suivie de près. Le débat public regarde donc le béton, et beaucoup moins la charrue.

## Les cibles identifiées

- Les élus et les services des 71 intercommunalités normandes : urbanisme, environnement, agriculture.
- La Région Normandie et les services de l'État (DREAL, DRAAF), pour comparer les territoires entre eux.
- Les acteurs de la biodiversité et du foncier : Agence normande de la biodiversité, Établissement public foncier, conservatoires, chambres d'agriculture.
- Les habitants et les associations qui veulent comprendre ce qui se passe près de chez eux.

## Les bénéfices et impacts attendus

- **Un constat par territoire, lisible en une phrase.** Chaque intercommunalité voit combien de prairies anciennes elle perd, ce qui les fait disparaître, et où elle se situe parmi les territoires comparables.
- **Deux causes mesurées sur les mêmes années.** La mise en culture, d'après les déclarations des agriculteurs, et les constructions, d'après la couche officielle de l'IGN.
- **Un regard sur les milieux sensibles** : zones humides, sites Natura 2000, zones d'intérêt écologique.
- **Trois scénarios jusqu'en 2035**, avec leur marge d'incertitude, pour voir ce que changerait une protection des zones sensibles ou un objectif de réduction.
- **Un repérage des friches à rendre à la nature** : 2 864 friches classées selon leur intérêt écologique et la facilité du projet, dont 415 à restaurer en priorité.
- **Un outil sobre et honnête.** Site statique sans dépendance ni service extérieur, données ouvertes uniquement, aucun affichage à la parcelle, limites écrites en clair, et un registre qui justifie chaque choix de méthode.

Limites assumées : l'outil décrit et compare, il ne prescrit pas. Le repérage des prairies mises en culture n'a pas encore été vérifié sur photographies aériennes. Le repère foncier affiché est national : les objectifs fixés par la Région à chaque territoire restent à intégrer, avec son concours.

## Les données mobilisées

| Jeu de données | Producteur | Lien |
|---|---|---|
| Successions de cultures 2015-2024 (RPG Explorer), d'après le Registre parcellaire graphique | INRAE / AgroParisTech, d'après IGN et ASP | https://doi.org/10.57745/6G0JTJ |
| OCS GE Artificialisation, différentiel par département | IGN | https://geoservices.ign.fr/ocsge |
| Contours des communes et des intercommunalités | geo.api.gouv.fr (DINUM) | https://geo.api.gouv.fr |
| ZNIEFF de types 1 et 2, sites Natura 2000 | MNHN, diffusion IGN | https://data.geopf.fr/wfs/ows |
| Inventaire des zones humides de Normandie | DREAL Normandie | https://www.donnees.normandie.developpement-durable.gouv.fr |
| Milieux potentiellement humides | INRAE / Institut Agro | https://geosas.fr |
| Observatoire des friches | Établissement public foncier de Normandie, via DataNormandie | https://www.datanormandie.fr/visualisation/information/?id=observatoire_des_friches_-_epfn |
| Consommation d'espaces naturels, agricoles et forestiers 2011-2025 | Cerema | https://www.data.gouv.fr/datasets/consommation-despaces-naturels-agricoles-et-forestiers-du-1er-janvier-2011-au-1er-janvier-2025 |
| Séries historiques du recensement (logements, population) | INSEE | https://www.insee.fr/fr/statistiques/8582555 |

Toutes ces données sont ouvertes. Les adresses exactes des fichiers téléchargés sont dans `src/telecharger_donnees.py`.

## Le lien vers la solution / des captures d'écran

- Site : [adresse publique à renseigner après la mise en ligne]
- Code, données calculées et documentation : archive jointe (`beton_charrue_datathon_2026.zip`).
- Captures d'écran : [à joindre : la synthèse régionale, la fiche d'une intercommunalité, le module « Friches à rendre »].
