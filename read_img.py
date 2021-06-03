import cv2


def read_img(path='./test.png'):
    img_original = cv2.imread(path, flags=cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img_original, 50, 255, cv2.THRESH_BINARY_INV)[1]
    return img_original, img
