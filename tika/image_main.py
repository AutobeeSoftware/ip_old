import cv2
import numpy as np
from scipy import ndimage
from operator import add
from utils import masking,bounding_box,closest,last_turn,is_center


# hue values must be discrete

lower_green = np.array([35,55,50])
upper_green = np.array([67,255,255])

lower_red = np.array([0,100,136])
upper_red = np.array([17,255,255])

font = cv2.FONT_HERSHEY_SIMPLEX


image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/tika/images/herb1.png")
width = image.shape[1]
heigth = image.shape[0]



mask_red = masking(image, lower_red, upper_red)
wild_herbs = bounding_box(mask_red,50,"wild herb")


mask_green = masking(image, lower_green, upper_green)
herbs= bounding_box(mask_green,50,"herb")

combined = herbs + wild_herbs
nearest = closest(combined)

cx, string = is_center(nearest,width,int(width/4))


#closest fonksiyonuya beraber objeleri birleştir



try:

    for i in herbs:
        cv2.rectangle(image, i[0], list(map(add, i[0], i[1])), (0,255,0), 2)
        cv2.putText(image, "herb", (i[0][0], i[0][1] - 15), font, 0.7, (0,255,0), 2)

    for j in wild_herbs:
        cv2.rectangle(image, j[0],list(map(add, j[0], j[1])), (0,0,255), 2)
        cv2.putText(image, "wild herb",(j[0][0], j[0][1] -15),font, 0.7, (0,0,255), 2)
    
    cv2.rectangle(image, nearest[0], list(map(add, nearest[0], nearest[1])), (255,0,0), 2)
    cv2.putText(image, nearest[2], (nearest[0][0], nearest[0][1] -15), font, 0.7, (255,0,0), 2)
    cv2.putText(image, string, (nearest[0][0], nearest[0][1] -40), font, 0.7, (255,0,0), 2)
    

    

except:
    pass

cv2.line(image,(int(width/4),0),(int(width/4),heigth),(255,0,0),5)
cv2.line(image,(int(width*3/4),0),(int(width*3/4),heigth),(255,0,0),5)

cv2.imshow("Image", image)
cv2.imshow("red", mask_red)
cv2.imshow("green", mask_green)

cv2.waitKey(0)

cv2.destroyAllWindows()




