import cv2
import numpy as np
from scipy import ndimage
import time
from utils import masking,bounding_box,intersect
import matplotlib.pyplot as plt
from operator import add

# hue values must be discrete


lower_green = np.array([48,80,50])
upper_green = np.array([67,180,180])

lower_red = np.array([0,88,80])
upper_red = np.array([20,255,255])

"""
lower_green = np.array([40,85,50])
upper_green = np.array([70,255,255])

lower_red = np.array([0,100,120])
upper_red = np.array([10,255,255])
        """



font = cv2.FONT_HERSHEY_SIMPLEX


prev_image_time = 0
# used to record the time at which we processed current image
new_image_time = 0
a = 0

cap = cv2.VideoCapture('/Users/emirysaglam/Documents/GitHub/IP_general/video.mp4')

red_mask_cache=[]
green_mask_cache=[]

c=0

while True:
    ret,image = cap.read()

    frame = image.copy()

    if not ret:
        break
    width = image.shape[1]
    height = image.shape[0]

    mask_red = masking(image, lower_red, upper_red)
    red_mask_cache.append(mask_red)

    mask_green = masking(image, lower_green, upper_green)
    green_mask_cache.append(mask_green)

    if len(red_mask_cache) > 3:
        red_mask_cache.pop(0)
        green_mask_cache.pop(0)
    else:
        continue

    red_inter = intersect(red_mask_cache[0],red_mask_cache[1],red_mask_cache[2])
    wild_herbs = bounding_box(red_inter)

    green_inter = intersect(green_mask_cache[0],green_mask_cache[1],green_mask_cache[2])
    herbs = bounding_box(green_inter)


    try:
        
        for i in herbs:
            cv2.rectangle(image, i[0], list(map(add, i[0], i[1])), (0,255,0), 2)
            cv2.putText(image, "herb", (i[1][0]+ 10, i[1][1] + 15), font, 0.7, (0,255,0), 2)

        for j in wild_herbs:
            cv2.rectangle(image, j[0],list(map(add, j[0], j[1])), (0,0,255), 2)
            cv2.putText(image, "wild herb",(j[1][0]+ 10, j[1][1] + 15),font, 0.7, (0,0,255), 2)

    except:
        pass

    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow("Image", image)
    cv2.imshow("red", mask_red)
    cv2.imshow("green", mask_green)


    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
    

cv2.destroyAllWindows()

