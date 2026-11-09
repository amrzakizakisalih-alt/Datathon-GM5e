# Vérification sur photo aérienne des retournements de prairies

**But :** estimer la fiabilité de la détection des retournements à partir du RPG. C'est le seul indicateur de l'outil qui repose sur des déclarations administratives, sans vérification de terrain. Le résultat servira à donner un **taux de confirmation** dans la page méthode.

**Usage interne seulement :** l'échantillon, les images et les contours localisent des parcelles agricoles. On ne les publie pas, on ne les affiche pas dans l'outil et on ne les livre pas. Git n'en conserve que ce fichier et `lecture.html`. Seul `resultat_validation.csv`, qui ne contient que des agrégats, peut être cité.

## Comment lire (pour chaque lecteur)

1. Ouvrir `lecture.html` dans un navigateur, sur un ordinateur (Chrome, Edge ou Firefox).
2. Indiquer son prénom, son numéro de lecteur et le nombre total de lecteurs. La page répartit les parcelles toute seule.
3. Pour chaque parcelle, dire ce qu'on voit à l'intérieur du contour : **Herbe, Culture, Autre ou Incertain**, sur la photo d'avant puis sur celle d'après. Le bouton « Aide » rappelle les critères et les raccourcis.
4. Cliquer régulièrement sur « Enregistrer mes réponses ». À la fin, déposer le fichier dans `data/validation/reponses/`.

**Ne pas ouvrir `echantillon_retournements.csv` ni `cle_codes.csv` avant d'avoir terminé** : ils donnent la réponse attendue. Pour transmettre le travail à un autre lecteur, ne lui donner que `lecture.html`, `points_lecture.js` et le dossier `images/` (environ 26 Mo), par un canal privé.

## Comment l'échantillon est construit

`src/echantillon_validation.py` tire 150 points de manière reproductible, tous sur des parcelles d'au moins 1 ha :

- **100 retournements détectés**, 20 par département : 10 sur des prairies anciennes (prairie permanente déclarée chaque année depuis 2015), 10 sur des prairies récentes ;
- **50 prairies maintenues** (témoins), 10 par département : prairie permanente déclarée chaque année de 2018 à 2024.

**La règle importante : la photo d'après est de la même année que la première culture déclarée.** La déclaration est donc confrontée directement à une image de la même année, et sans condition sur ce que devient la parcelle ensuite. Les dates viennent du graphe de mosaïquage de l'IGN. La photo d'avant vient de la mosaïque 2016-2020, sur une parcelle déjà déclarée en prairie cette année-là.

**Trente points sont lus par tous les lecteurs** (4 retournements et 2 témoins par département), pour mesurer leur accord. S'il n'y a qu'un lecteur, cette mesure n'existe pas.

La page ne montre ni le type de la parcelle, ni sa strate, ni son code de culture, ni son département.

## Règle de calcul, fixée avant la lecture

`src/resultat_validation.py` calcule :

- **le taux de confirmation (résultat principal) :** part des retournements détectés lus en « Culture » sur la photo d'après, sans les « Incertain » ;
- **une variante prudente :** les « Incertain » comptent comme non confirmés ;
- **un taux strict :** « Herbe » avant et « Culture » après ;
- **le taux séparé des prairies anciennes et récentes**, puisque l'outil publie les deux chiffres ;
- **les fausses alertes :** témoins lus en « Culture ». Si elles sont nombreuses, c'est la lecture qui est en cause, pas le RPG ;
- **l'accord entre lecteurs :** part de réponses identiques et kappa de Cohen.

Le taux est pondéré par la surface, dans chaque strate puis entre strates. L'intervalle à 95 % vient d'un bootstrap. Sur les points communs, la réponse retenue est la majorité, et une égalité donne « Incertain ».

**On publie le résultat quel qu'il soit, avec cette règle.** On ne change ni l'échantillon ni la règle après avoir vu les réponses.

## Ce que le résultat permet de dire, et ce qu'il ne permet pas

- **Il teste la déclaration d'une année :** « Le RPG déclare une culture cette année-là ; la photo le montre-t-elle ? » Les autres années et les parcelles de moins d'1 ha ne sont pas testées. Le script indique la part de la surface couverte.
- **Il porte en pratique sur des premières cultures de 2022 et 2023 :** ce tirage contient 60 points de 2022, 40 de 2023 et aucun de 2021. Les poids des strates couvrent pourtant 2021 à 2023, une approximation assumée. On suppose que la fiabilité est comparable sur 2015-2024, sans pouvoir le prouver. L'année 2023 suit la refonte du RPG, donc ce test porte aussi sur la période la plus délicate.
- **Il écarte les prairies devenues « permanentes » après la photo d'avant :** ce sont environ 13 à 23 % de la surface des prairies récentes retournées, soit 6 à 10 % de la surface de tous les retournements 2021-2023 sur des parcelles d'au moins 1 ha. Ce sont aussi les cas les plus douteux, donc le taux des prairies récentes est peut-être un peu flatté.
- **Il ne mesure pas les retournements manqués :** prairie labourée puis ressemée, ou jamais déclarée à la PAC. Les témoins disent seulement si l'on se trompe sur des prairies stables.
- **La lecture reste un jugement humain :** une céréale verte de mai peut ressembler à une prairie dense. C'est pourquoi la réponse « Incertain » existe et que le taux d'accord est publié.

## Refaire le tirage ou les images

```
.venv\Scripts\python.exe src\echantillon_validation.py
.venv\Scripts\python.exe src\preparer_lecture.py
.venv\Scripts\python.exe src\resultat_validation.py
```

Refaire le tirage après le début de la lecture rendrait les réponses inutilisables. `cache_dates.csv` garantit que la relance donne le même tirage tant que ce fichier est conservé.
