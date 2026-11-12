"""Outils communs aux scripts : rattachement des objets aux communes et EPCI, part d'un polygone en milieu humide."""
import json


def part_mph(raster, geojson, x, y):
    """Part des pixels d'un polygone en milieu potentiellement humide (classes 1 à 3), entre 0 et 1.

    `raster` est le fichier MPH ouvert avec rasterio, `geojson` la géométrie en texte, (x, y) son point intérieur.
    Dans ce raster, 0 veut dire « hors de l'enveloppe humide » et sert aussi de valeur « sans donnée ». On lit donc les
    valeurs brutes : avec un tableau masqué, les pixels à 0 sortiraient du dénominateur et tout polygone touchant un
    pixel humide vaudrait 100 %. Si aucun centre de pixel ne tombe dans le polygone, le pixel du point intérieur décide.
    """
    import rasterio.mask  # import local : les scripts sans raster n'ont pas besoin de rasterio

    try:
        dehors, _, fenetre = rasterio.mask.raster_geometry_mask(raster, [json.loads(geojson)], crop=True)
        v = raster.read(1, window=fenetre)[~dehors]
    except ValueError:  # polygone hors de l'emprise du raster
        v = []
    if len(v) == 0:
        v = [next(raster.sample([(x, y)]))[0]]
    return sum(1 for p in v if 1 <= p <= 3) / len(v)


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
