import shapely
import geodatasets
import geopandas

from libpysal.weights.experimental._triangulation import(
    delaunay,
    gabriel,
    relative_neighborhood,
    voronoi,
    _edges_from_simplices,)

from libpysal.weights.experimental._utils import _validate_geometry_input


stores = geopandas.read_file(
    geodatasets.get_path('geoda liquor_stores')
)

stores = stores.explode() # convert from multipoint to point
stores.reset_index(inplace=True)

dt = delaunay(stores)


print('Are we missing points in the resulting weights?')
print('dt.n: ', dt.n, 'stores.shape: ', stores.shape)



from scipy.spatial import Delaunay as _Delaunay

coordinates, ids, geoms = _validate_geometry_input(stores,
                                                   ids=None,
                                                   valid_geometry_types=("Point",))

dt_ = _Delaunay(coordinates)

edges = _edges_from_simplices(dt_.simplices)
