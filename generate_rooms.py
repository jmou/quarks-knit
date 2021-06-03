import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.affinity import scale


def check_point_in_polys(polys, p):
    found = False
    for poly in polys:
        if poly.contains(Point(p[0], p[1])):
            found = True
            return found
    return found


def check_line_in_polys(polys, p1, p2, ignore):
    found = False
    for i in range(len(polys)):
        poly = polys[i]
        if i != ignore and poly.intersects(LineString([(p1[0], p1[1]), (p2[0], p2[1])])):
            found = True
            return found
    return found


def generate_rooms(rooms, regions, isSegment=False, iterations=20, scale_factor=1.01):
    keep_indices = dict()
    final_rooms = rooms
    final_rooms_arr = [np.array(r.exterior.coords) for r in final_rooms]

    for val in range(len(final_rooms_arr)):
        keep_indices[val] = list(range(len(final_rooms_arr[val])))

    for i in range(iterations):

        #rooms_dilated = [r.buffer(padding, resolution=-100, cap_style=2, join_style=2) for r in final_rooms]
        rooms_scaled = [scale(
            r, xfact=scale_factor, yfact=scale_factor, origin='center') for r in final_rooms]

        for j in range(len(rooms_scaled)):
            #dilated_room = np.array(rooms_dilated[j].exterior.coords)
            scaled_room = np.array(rooms_scaled[j].exterior.coords)

            for p in range(len(scaled_room)):
                if j in keep_indices and p in keep_indices[j]:
                    point = scaled_room[p]

                    next_idx = p+1 if len(scaled_room) > p+2 else 0
                    point_next = point if not isSegment else scaled_room[next_idx]

                    is_in_regions = check_point_in_polys(
                        regions, point) if not isSegment else check_line_in_polys(regions, point, point_next, j)
                    if is_in_regions:

                        final_rooms_arr[j][p] = point
                        if isSegment:
                            final_rooms_arr[j][next_idx] = point_next

                        is_in_other_rooms = check_point_in_polys(
                            rooms_scaled, point) if not isSegment else check_line_in_polys(rooms_scaled, point, point_next, j)
                        if is_in_other_rooms:
                            keep_indices[j].remove(p)
                            if isSegment and next_idx in keep_indices[j]:
                                keep_indices[j].remove(next_idx)

        final_rooms = [Polygon(new_room) for new_room in final_rooms_arr]
        #print('iteration ', i, ' finished')

    return final_rooms
