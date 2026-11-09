"""Définitions communes à tous les scripts : années, classes RPG, prairies anciennes.

C'est la seule source de vérité. Un script qui classe les cultures du RPG ou repère les prairies
anciennes passe par ce module, pour que deux scripts ne puissent plus diverger.

Classes de chaque LCP pour une année, d'après le groupe RPG (`grp` de ref_fr_en.csv) :
  PP        groupe 18   prairies permanentes
  PT        groupe 19   prairies temporaires
  fourrage  groupe 16   fourrages annuels
  gel       groupe 11   jachères (surfaces gelées sans production). Une PP mise en jachère n'est PAS un
                        retournement : la jachère reste souvent en herbe et rien ne prouve un labour.
                        Elle compte seulement dans la borne haute des pertes.
  culture   groupes 1 à 9, 14, 15, 24, 25   céréales, oléagineux, protéagineux, maïs, légumes…
  autre     les autres groupes (vergers, vignes, surfaces non agricoles…)
  non déclaré / NULL    la LCP n'est pas déclarée à la PAC cette année-là

Retournement strict : PP l'année N, culture l'année N+1.
Prairie ancienne pour le passage N -> N+1 : PP chaque année de 2015 jusqu'à N inclus.
"""

ANNEES = [f"{y:02d}" for y in range(15, 25)]   # suffixes des colonnes crop15 ... crop24

GRP_PP, GRP_PT, GRP_FOURRAGE, GRP_GEL = 18, 19, 16, 11
GRP_CULTURE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 24, 25)
# Les deux codes du groupe 18 : PPH = prairie permanente au sens strict, PRL = prairie en rotation longue
# (6 ans ou plus). Le code PRL disparaît du RPG en 2023 : 94 % des PRL de 2022 sont déclarées PPH en 2023.
CODE_PPH, CODE_PRL = "PPH", "PRL"


def annees_entre(debut, fin):
    """Suffixes des années de debut à fin incluses, par exemple (2019, 2022) -> ['19', '20', '21', '22']."""
    return [f"{y:02d}" for y in range(debut % 100, fin % 100 + 1)]


def jointures_ref(alias="l", annees=ANNEES):
    """Jointures SQL de la table `ref` (crop -> grp) pour chaque année : alias r15 ... r24."""
    return " ".join(f"LEFT JOIN ref r{y} ON r{y}.crop = {alias}.crop{y}" for y in annees)


def classe_sql(y, alias="l", non_declare="NULL"):
    """Expression SQL de la classe de l'année y, nommée k{y}. Suppose la jointure r{y} de jointures_ref.

    `non_declare` est la valeur SQL d'une année non déclarée : NULL par défaut, ou "'non déclaré'".
    """
    return f"""CASE WHEN {alias}.crop{y} IS NULL THEN {non_declare}
             WHEN r{y}.grp = {GRP_PP} THEN 'PP' WHEN r{y}.grp = {GRP_PT} THEN 'PT'
             WHEN r{y}.grp IN {GRP_CULTURE} THEN 'culture' WHEN r{y}.grp = {GRP_FOURRAGE} THEN 'fourrage'
             WHEN r{y}.grp = {GRP_GEL} THEN 'gel' ELSE 'autre' END AS k{y}"""


def classes_sql(alias="l", non_declare="NULL", annees=ANNEES):
    """Les colonnes k15 ... k24, séparées par des virgules."""
    return ",\n".join(classe_sql(y, alias, non_declare) for y in annees)


def pp_ancienne_sql(n):
    """Condition SQL « PP chaque année de 2015 jusqu'à l'année n incluse » (n : suffixe, ex. '20')."""
    return " AND ".join(f"k{y} = 'PP'" for y in ANNEES[: ANNEES.index(n) + 1])


def retournement_sql(a, b):
    """Condition SQL du retournement strict entre les années a et b (suffixes)."""
    return f"k{a} = 'PP' AND k{b} = 'culture'"
