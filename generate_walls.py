import numpy as np
from shapely.geometry import Polygon


def generate_linear_analysis(room_original, room_cleaned):
    # Experiment Simple fnuction for extraction sifferetn wall segments .....
    walls = []
    original_rooms_arr = np.array(room_original.exterior.coords)
    room_cleaned_arrr = np.array(room_cleaned.exterior.coords)

    for i in range(len(original_rooms_arr)):
        next_i = i+1 if len(original_rooms_arr) > i+1 else 0

        p0 = original_rooms_arr[i]
        p1 = room_cleaned_arrr[i]
        p2 = room_cleaned_arrr[next_i]
        p3 = original_rooms_arr[next_i]
        walls.append(Polygon([p0, p1, p2, p3]))

    return walls
