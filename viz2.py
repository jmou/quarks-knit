import cv2
import numpy as np
import matplotlib.pyplot as plt


def viz2(img, regions, rooms, all_ctrs):
    all_ctrs_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)

    cv2.drawContours(all_ctrs_img, all_ctrs, -1, (0, 255, 0), 3)

    filtered_ctrs_img = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    for region in regions + rooms:
        cv2.drawContours(filtered_ctrs_img, [region], -1, (0, 255, 0), 3)

    f, ax = plt.subplots(1, 2, figsize=(20, 14))

    ax[0].imshow(all_ctrs_img)
    ax[0].axis('off')
    ax[0].set_title('All contours simplified')

    ax[1].imshow(filtered_ctrs_img)
    ax[1].axis('off')
    ax[1].set_title('All contours filtered and simplified')

    f.savefig('fig2.jpg')
    return
