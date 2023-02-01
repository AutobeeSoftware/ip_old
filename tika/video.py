import cv2
import numpy as np
from scipy import ndimage
import time
from utils import masking,bounding_box
import matplotlib.pyplot as plt

# hue values must be discrete


lower_green = np.array([40,40,50])
upper_green = np.array([110,255,180])

lower_red = np.array([5,100,110])
upper_red = np.array([30,210,200])



font = cv2.FONT_HERSHEY_SIMPLEX


prev_image_time = 0
# used to record the time at which we processed current image
new_image_time = 0
a = 0

cap = cv2.VideoCapture('C:/Users/ertug/Desktop/video.mp4')


while True:
    ret,image = cap.read()
    
    if not ret:
        break
    width = image.shape[1]
    height = image.shape[0]

    mask_red = masking(image, lower_red, upper_red)
    wild_herbs = bounding_box(mask_red)


    mask_green = masking(image, lower_green, upper_green)
    herbs = bounding_box(mask_green)


    try:
        
        for i in herbs:
            cv2.rectangle(image, i[0], i[1], (0,255,0), 2)

        for j in wild_herbs:
            cv2.rectangle(image, j[0], j[1], (0,0,255), 2)

    except:
        pass

    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow("Image", image)
    cv2.waitKey(1)

cv2.destroyAllWindows()
