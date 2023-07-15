import cv2
import numpy as np
import sys
import os
import math
import time

### fps icin ###
prev_image_time = time.time()

################

# Add the parent folder path to the system's import path
sys.path.append(os.path.abspath('../IP_general'))

from utils2 import masking,bounding_box, between_buoys , camera2lidar

image = cv2.imread("/Users/emirysaglam/GitHub/IP_general/NJORD/stage.jpeg")
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

hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


mask_red = masking(hsv_frame, lower_red, upper_red, opening_kernel = 0, medianF_tresh = 0)
reds = bounding_box(mask_red,100,"red")
print(reds)
print("#####################")

mask_green = masking(hsv_frame, lower_green, upper_green, opening_kernel = 0, medianF_tresh = 0)
greens= bounding_box(mask_green,100,"green")
print(greens)

print("*****************")


mask_yellow = masking(hsv_frame, lower_yellow, upper_yellow, opening_kernel = 0, medianF_tresh = 0)
yellows= bounding_box(mask_yellow,100,"yellow")
print(yellows)

print("^^^^^^^^^^^^^^^")

mask_black = masking(hsv_frame, lower_black, upper_black, opening_kernel = 0, medianF_tresh = 0)
blacks= bounding_box(mask_black,100,"black")
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
        cv2.putText(image, "black", (z[0][0], z[0][1] - 15), font, 0.7, (0,0,0), 2)
    
    
except:
    pass




shift = int((270-60)/2)
ratio = 60/width 


colors = [] 

if reds != None:
    colors += reds
if yellows != None:
    colors += yellows
if greens != None:
    colors += greens
if blacks != None:
    colors += blacks



print("*************************")
testr = camera2lidar(width,60,colors)
print(testr)
try:
    testr = camera2lidar(width,60,colors)
    print(testr)
    for i,o in enumerate(testr):
        if o != 0:
            ind = i - shift
            cv2.line(image, (int(ind//ratio),0 ), (int(ind//ratio), heigth), (0, 0, 255), 1)
            cv2.line(image, (int((ind+1)//ratio),0 ),(int((ind+1)//ratio), heigth), (0, 0, 255), 1)
except:
    pass


"""
try:
    testr = camera2lidar(width,60,reds)
    for i,o in enumerate(testr):
        if o != 0:
            ind = i - shift
            cv2.line(image, (int(ind//ratio),0 ), (int(ind//ratio), heigth), (0, 0, 255), 1)
            cv2.line(image, (int((ind+1)//ratio),0 ),(int((ind+1)//ratio), heigth), (0, 0, 255), 1)
except:
    pass

try:
    testg = camera2lidar(width,60,greens)
    for i,o in enumerate(testg):

        if o != 0:
            ind = i - shift
            cv2.line(image, (int(ind//ratio),0 ), (int(ind//ratio), heigth), (0, 255, 0), 1)
            cv2.line(image, (int((ind+1)//ratio),0 ), (int((ind+1)//ratio), heigth), (0, 255, 0), 1)
except:
    pass

try:
    testy = camera2lidar(width,60,yellows)
    for i,o in enumerate(testy):
        if o != 0:        
            ind = i - shift
            cv2.line(image, (int(ind//ratio),0 ), (int(ind//ratio), heigth), (0, 255, 255), 1)
            cv2.line(image, (int((ind+1)//ratio),0 ), (int((ind+1)//ratio), heigth), (0, 255, 255), 1)
except:
    pass

try:
    testb = camera2lidar(width,60,blacks)
    for i,o in enumerate(testb):
        if o != 0:
            ind = i - shift       
            cv2.line(image, (int(ind//ratio),0 ), (int(ind//ratio), heigth), (0, 0, 0), 1)
            cv2.line(image, (int((ind+1)//ratio),0 ), (int((ind+1)//ratio), heigth), (0, 0, 0), 1)
except:
    pass

"""

new_image_time = time.time()
fps = new_image_time - prev_image_time
print(fps)
cv2.imshow("Image", image)
cv2.imshow("red", mask_red)
cv2.imshow("green", mask_green)

cv2.waitKey(0)
########
cv2.destroyAllWindows()

