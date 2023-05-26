from collections import defaultdict

import numpy
import pandas
import shapely

from .base import W


def vertex_set_intersection(geoms, by_edge=False, ids=None):
    """
    Use a hash map inversion to construct a graph

    Arguments
    ---------
    ...

    """
    if ids is None:
        ids = getattr(geoms, "index", pandas.RangeIndex(len(geoms)))
    ids = numpy.asarray(ids)

    # initialise the target map
    graph = defaultdict(set)

    # get all of the vertices for the input
    assert (
        ~geoms.geom_type.str.endswith("Point")
    ).any(), "this graph type is only well-defined for line and polygon geometries."

    ## TODO: this induces a "fake" edge between the closing and opening point
    ##       of two multipolygon parts. This should never enter into calculations,
    ##       *unless* two multipolygons share opening and closing points in the
    ##       same order and part order. Still, this should be fixed by ensuring that
    ##       only adjacent points of the same part of the same polygon are used.
    ##       this bug also exists in the existing contiguity builder.

    # geoms = geoms.explode()
    # multipolygon_ixs = geoms.get_level_values(0)
    # ids = ids[multipolygon_ixs]
    # geoms = geoms.geometry
    vertices, offsets = shapely.get_coordinates(geoms, return_index=True)
    # initialise the hashmap we want to invert
    vert_to_geom = defaultdict(set)

    # populate the hashmap we intend to invert
    if by_edge:
        for i, vertex in enumerate(vertices[:-1]):
            if offsets[i] != offsets[i + 1]:
                continue
            edge = tuple(sorted([tuple(vertex), tuple(vertices[i + 1])]))
            # edge to {polygons, with, this, edge}
            vert_to_geom[edge].add(offsets[i])
    else:
        for i, vertex in enumerate(vertices):
            # vertex to {polygons, with, this, vertex}
            vert_to_geom[tuple(vertex)].add(offsets[i])

    # invert vert_to_geom
    for nexus in vert_to_geom.values():
        if len(nexus) < 2:
            continue
        nexus_names = {ids[ix] for ix in nexus}
        for geom_ix in nexus:
            gid = ids[geom_ix]
            graph[gid] |= nexus_names
            graph[gid].remove(gid)
    return W.from_dicts(graph)


def queen(geoms, ids=None):
    if ids is None:
        try:
            ids = geoms.index
        except:
            ids = numpy.arange(len(geoms))
    head, tail = shapely.STRtree(geoms).query(geoms, predicate="touches")
    return W.from_arrays(ids[head], ids[tail], numpy.ones_like(head))


def rook(geoms, ids=None):
    if ids is None:
        try:
            ids = geoms.index
        except:
            ids = numpy.arange(len(geoms))
    head, tail = shapely.STRtree(geoms).query(geoms)
    geoms = numpy.asarray(geoms)
    mask = shapely.relate_pattern(geoms[head], geoms[tail], "F***1****")
    return W.from_arrays(ids[head[mask]], ids[tail[mask]], numpy.ones_like(head[mask]))