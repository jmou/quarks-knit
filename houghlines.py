import cv2
import numpy as np


def houghlines(regions_img, rooms_img):
    # Useless
    only_walls = regions_img - rooms_img

    canny_img = np.zeros(
        (only_walls.shape[0], only_walls.shape[1], 3), np.uint8)

    edges = cv2.Canny(only_walls, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 0,
                            minLineLength=20, maxLineGap=10)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(canny_img, (x1, y1), (x2, y2), (0, 255, 0), 10)

    cv2.imwrite("only_walls.png", only_walls)
    cv2.imwrite("canny.png", canny_img)
