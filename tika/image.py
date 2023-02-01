import cv2
import numpy as np
from scipy import ndimage
from utils import masking,bounding_box


# hue values must be discrete

lower_green = np.array([40,40,50])
upper_green = np.array([110,255,180])

lower_red = np.array([5,100,110])
upper_red = np.array([30,210,200])



font = cv2.FONT_HERSHEY_SIMPLEX


image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/tika/images/result1.png")


mask_red = masking(image, lower_red, upper_red)
wild_herbs = bounding_box(mask_red)


mask_green = masking(image, lower_green, upper_green)
herbs= bounding_box(mask_green)


try:

    for i in herbs:
        cv2.rectangle(image, i[0], i[1], (0,255,0), 2)

    for j in wild_herbs:
        cv2.rectangle(image, j[0], j[1], (0,0,255), 2)



    
except:
    pass


cv2.waitKey(0)

cv2.destroyAllWindows()




