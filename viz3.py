import cv2
import numpy as np
import matplotlib.pyplot as plt


def viz3(img, regions, rooms):
    all_regions_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    regions_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    for region in regions:
        cv2.fillPoly(regions_img, [region], (255, 255, 255))
        cv2.fillPoly(all_regions_img, [region], (0, 0, 255))

    rooms_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    for region in rooms:
        cv2.fillPoly(rooms_img, [region], (255, 255, 255))
        cv2.fillPoly(all_regions_img, [region], (255, 0, 255))

    f, ax = plt.subplots(1, 4, figsize=(40, 25))

    ax[0].imshow(regions_img)
    ax[0].axis('off')
    ax[0].set_title('Classified regions')

    ax[1].imshow(rooms_img)
    ax[1].axis('off')
    ax[1].set_title('Classified rooms')

    ax[2].imshow(regions_img - rooms_img)
    ax[2].axis('off')
    ax[2].set_title('Regions - Rooms for contours')

    ax[3].imshow(all_regions_img)
    ax[3].axis('off')
    ax[3].set_title('Regions + Rooms')

    f.savefig('fig3.jpg')
    return all_regions_img, regions_img, rooms_img
