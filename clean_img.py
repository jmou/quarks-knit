import cv2
import numpy as np


def clean_img(img, kernel_size=5, iterations=5):
    '''
    clean_img : 
        uses morphological operations to clean the image, in this case uses erosion to remove 
        extremly small items, and dilation to go back to original shape and closess some holes,
        different combination provide diifferent results

    docs: https://docs.opencv.org/master/d9/d61/tutorial_py_morphological_ops.html

    img:  threshhold image
    kernel_size: the size of the morph kernel in pixels 5 by default, by default uses rectangle as a shape
    iterations: nb of times operations are applied

    returns 
        img: cleaned image
    '''

    kernel_s = np.ones((2, 2), np.uint8)
    img = cv2.erode(img, kernel_s, iterations=iterations)

    kernel_1 = np.ones((kernel_size, kernel_size), np.uint8)
    img = cv2.erode(img, kernel_1, iterations=iterations)
    img = cv2.dilate(img, kernel_1, iterations=iterations)

    return img
