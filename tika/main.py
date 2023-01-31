import cv2
import numpy as np
from scipy import ndimage
import time
import matplotlib.pyplot as plt

# hue values must be discrete

lower_green = np.array([40,40,50])
upper_green = np.array([110,255,180])

lower_red = np.array([5,100,110])
upper_red = np.array([30,210,200])


def masking(img, lower_hsv, upper_hsv):

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

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
            print(obj_area)
            if obj_area > 60:
                x,y,w,h = cv2.boundingRect(c)
                params.append([(x,y),(w+x,h+y)])
                
            else:
                print("no object found bigger than treshold")
                return None
        return params
    
    else:
        print("no contour found")
        return None



font = cv2.FONT_HERSHEY_SIMPLEX


image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/tika/images/result1.png")

width = image.shape[1]
height = image.shape[0]

mask_red = masking(image, lower_red, upper_red)
wild_herbs = bounding_box(mask_red)


mask_green = masking(image, lower_green, upper_green)
herbs= bounding_box(mask_green)


try:

    for i in herbs:
        cv2.rectangle(image, i[0], i[1], (0,255,0), 2)

    for j in wild_herbs:
        cv2.rectangle(image, j[0], j[1], (0,0,255), 2)

    cv2.imshow("Image", image)
    
    cv2.imshow("herb", mask_green)
    cv2.imshow("wildherb", mask_red)

    
except:
    pass


cv2.waitKey(0)

cv2.destroyAllWindows()




