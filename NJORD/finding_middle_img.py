import cv2
import numpy as np
import sys
import os

# Add the parent folder path to the system's import path
sys.path.append(os.path.abspath('../IP_general'))

from utils2 import masking,bounding_box, between_buoys
import math



image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/NJORD/stage.jpeg")
#image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)

font = cv2.FONT_HERSHEY_SIMPLEX

lower_red =  np.array([0,59,21])
upper_red = np.array([26,255,255])

lower_green = np.array([53,87,59])
upper_green = np.array([130,255,255])


lower_yellow = np.array([14, 0, 0])
upper_yellow = np.array([36,255,119])


lower_black = np.array([0, 0, 0])
upper_black = np.array([0,0,7])

width = image.shape[1]
heigth = image.shape[0]

print(width, heigth)



mask_red = masking(image, lower_red, upper_red, opening_kernel = 0, medianF_tresh = 0)
reds = bounding_box(mask_red,1,"red")
print(reds)
print("#####################")

mask_green = masking(image, lower_green, upper_green, opening_kernel = 0, medianF_tresh = 0)
greens= bounding_box(mask_green,1,"green")
print(greens)

print("*****************")


mask_yellow = masking(image, lower_yellow, upper_yellow, opening_kernel = 0, medianF_tresh = 0)
yellows= bounding_box(mask_yellow,1,"yellow")
print(yellows)

print("^^^^^^^^^^^^^^^")

mask_black = masking(image, lower_black, upper_black, opening_kernel = 0, medianF_tresh = 0)
blacks= bounding_box(mask_black,1,"black")
print(blacks)

print("^^^^^^^^^^^^^^^")



middle = between_buoys(greens,reds) #closest middle point
print(middle)

##for visualising##
try:
    if middle[1] == True: 
        cv2.circle(image, middle[0], int(middle[2]*0.051), (255,255,255), 2)
    else:
        cv2.circle(image, middle[0],  int(middle[2]*0.05), (0,0,0), 2)


    for i in greens:
        radius = int( math.sqrt(i[1] / math.pi))
        cv2.circle(image, i[0], radius, (0,255,0), 2)
        cv2.putText(image, "green", (i[0][0], i[0][1] - 15), font, 0.7, (0,255,0), 2)
    
    for j in reds:
        
        radius = int( math.sqrt(j[1] / math.pi))
        cv2.circle(image, j[0], radius, (0,0,255), 2)
        cv2.putText(image, "red", (j[0][0], j[0][1] - 15), font, 0.7, (0,0,255), 2)
    
    for k in yellows:
        
        radius = int( math.sqrt(k[1] / math.pi))
        cv2.circle(image, k[0], radius, (0,255,255), 2)
        cv2.putText(image, "yellow", (k[0][0], k[0][1] - 15), font, 0.7, (0,255,255), 2)
    
    for z in blacks:
        
        radius = int( math.sqrt(z[1] / math.pi))
        cv2.circle(image, z[0], radius, (0,255,255), 2)
        cv2.putText(image, "black", (z[0][0], z[0][1] - 15), font, 0.7, (0,255,255), 2)
    
    
except:
    pass


cv2.imshow("Image", image)
cv2.imshow("red", mask_red)
cv2.imshow("green", mask_green)

cv2.waitKey(0)
########
cv2.destroyAllWindows()

