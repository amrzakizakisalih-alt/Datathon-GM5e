"""Outils communs aux scripts : rattachement des objets aux communes et EPCI."""


def rattacher_plus_proche(con, table, cle, point):
    """Rattache à la commune la plus proche les lignes de `table` sans commune.

    Ce sont les objets dont le point intérieur tombe hors des contours communaux simplifiés
    de geo.api.gouv.fr : littoral, estrans, limites départementales. La table doit avoir les
    colonnes insee, epci_code et epci_nom. `point` est l'expression SQL du point de l'objet
    (alias t), et la table `communes` doit exister.
    """
    con.execute(f"""
        CREATE OR REPLACE TEMP TABLE _plus_proche AS
        SELECT t.{cle} AS cle,
               arg_min({{'insee': c.insee, 'epci_code': c.epci_code, 'epci_nom': c.epci_nom}},
                       ST_Distance({point}, c.geom)) AS m,
               min(ST_Distance({point}, c.geom)) AS dist
        FROM {table} t, communes c
        WHERE t.insee IS NULL
        GROUP BY t.{cle}
    """)
    n, dmax, dmed = con.execute(
        "SELECT count(*), coalesce(max(dist), 0), coalesce(median(dist), 0) FROM _plus_proche").fetchone()
    con.execute(f"""
        UPDATE {table} SET insee = p.m.insee, epci_code = p.m.epci_code, epci_nom = p.m.epci_nom
        FROM _plus_proche p WHERE {table}.{cle} = p.cle
    """)
    print(f"  {table} : {n:,} objets rattachés à la commune la plus proche "
          f"(distance médiane {dmed:,.0f} m, max {dmax:,.0f} m)")
