import cv2
import numpy as np
from scipy import ndimage
from utils import masking,bounding_box


# hue values must be discrete

lower_green = np.array([48,80,50])
upper_green = np.array([67,180,180])

lower_red = np.array([0,88,80])
upper_red = np.array([20,255,255])


font = cv2.FONT_HERSHEY_SIMPLEX


image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/tika/cant_find_bbs/errors7.png")


mask_red = masking(image, lower_red, upper_red)
wild_herbs = bounding_box(mask_red)


mask_green = masking(image, lower_green, upper_green)
herbs= bounding_box(mask_green)



try:

    for i in herbs:
        cv2.rectangle(image, i[0], i[1], (0,255,0), 2)
        cv2.putText(image, "herb", (i[1][0]+ 10, i[1][1] + 15), font, 0.7, (0,255,0), 2)

    for j in wild_herbs:
        cv2.rectangle(image, j[0], j[1], (0,0,255), 2)
        cv2.putText(image, "wild herb",(j[1][0]+ 10, j[1][1] + 15),font, 0.7, (0,0,255), 2)


except:
    pass

cv2.imshow("Image", image)
cv2.imshow("red", mask_red)
cv2.imshow("green", mask_green)

cv2.waitKey(0)

cv2.destroyAllWindows()




