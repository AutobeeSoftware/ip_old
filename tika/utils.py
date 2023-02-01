import cv2
import numpy as np
from scipy import ndimage
import time

def masking(img, lower_hsv, upper_hsv):
    width = img.shape[1]
    height = img.shape[0]

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    cv2.rectangle(mask, (0,0), (width,int(height/4)), (0, 0, 0), -1)

    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=2)

    return mask_f


def bounding_box(mask):
    # try:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    params = []
    if len(contours) > 0:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        for c in sorted_contours[:3]:
            obj_area = cv2.contourArea(c)
            if obj_area > 60:
                x, y, w, h = cv2.boundingRect(c)
                params.append([(x, y), (w + x, h + y)])

            else:
                print("no object found bigger than treshold")
                return None
        return params

    else:
        print("no contour found")
        return None