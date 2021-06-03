
import numpy as np
from shapely.geometry import Polygon, MultiPolygon


def shapeify(rooms, regions):
    # making rooms and regions into Shapely format
    rooms_polygons = [Polygon(np.squeeze(i)).simplify(5) for i in rooms]
    regions_polygons = [Polygon(np.squeeze(i)).simplify(
        5).difference(MultiPolygon(rooms_polygons)) for i in regions]

    return rooms_polygons, regions_polygons
