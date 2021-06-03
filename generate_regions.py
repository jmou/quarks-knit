import cv2


def contours_extraction(img):
    '''
    Basic contour extraction from threshold image

    img: img

    returns
        ctr: list of all extracted contours,
        h: containes hierarchical information about every contour, 
            for every contour [nextCtr_id, prevCtr_id, FirstChildCtr_id, parentCtr_id ]
    '''

    ctr, h = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return ctr, h[0]


def contour_data(cnt, epsilon=0.001):
    '''
    Extracts some useful informations from a contour like mass center, area and perimeter, more features can be extracted 
    using cv2.moments
    Also simplifies the contours

    cnt: single contour,
    epsilon: simplification strength 

    returns
        area: area of contour will be used for filtering
        approx: simplified polygon 
    '''

    M = cv2.moments(cnt)

    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)

    epsilon = epsilon * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    return area, approx


def classify_contour(h, idx, cls_dict):
    '''
    classifies the contour, on either region of room
    for the given contour if there is no parent then the contour is a region, else is room

    h: contourss hierarchical features
    idx: index of the contour to classify
    cls_dict: dictionnary containing classification of the different contours

    returns
        updated classification dict

    '''

    p_idx = h[idx][3]
    p_p_idx = h[p_idx][3]

    if p_idx not in cls_dict:
        if p_p_idx == -1:
            p_cls = 0
        else:
            cls_dict = classify_contour(h, idx, cls_dict)
            p_cls = cls_dict[p_idx]
    else:
        p_cls = cls_dict[p_idx]

    cls = p_cls + 1
    cls_dict[idx] = cls

    return cls_dict


# Main function to extract the road mask
def generate_regions(img, epsilon=0.001):
    '''
    Generate the regions and rooms from an image

    img: thresholded image
    epsilon :: should be replaced b **kwags

    returns
        img: cleaned img
        ctr: all extracted contours
        regions: classified regions
        rooms: classified rooms
    '''

    img_area = img.shape[0] * img.shape[1]
    max_area = 0.8*img_area
    min_area = 400

    ctr, h = contours_extraction(img)  # extract contours and hierarchical data

    classes_dict = dict()
    approxs = [None] * len(ctr)

    for i in range(len(ctr)):  # classify contours
        cnt = ctr[i]
        #cnt_area, approx = ctr_data(cnt, epsilon)
        cnt_area, approxs[i] = contour_data(cnt, epsilon)
        # If area is very small or very big then, thea features are useless...
        if cnt_area < max_area and cnt_area > min_area:
            classes_dict = classify_contour(h, i, classes_dict)
        else:
            classes_dict[i] = -1

    base_region_idx = 0 if len(list(classes_dict.values())) < 2 else min(
        [i for i in list(classes_dict.values()) if i >= 0])
    regions = [approxs[i] for i in range(
        len(ctr)) if classes_dict[i] == base_region_idx and h[i][2] != -1]
    rooms = [approxs[i]
             for i in range(len(ctr)) if classes_dict[i] > base_region_idx]

    return img, ctr, classes_dict, regions, rooms
