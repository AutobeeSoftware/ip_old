import cv2
import numpy as np
from scipy import ndimage
import time
import matplotlib.pyplot as plt

# hue values must be discrete

lower_green = np.array([76,31,56])
upper_green = np.array([104,62,30])

lower_red = np.array([24,65,78])
upper_red = np.array([9,92,65])


def masking(img, lower_hsv, upper_hsv):

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=5)

    return mask_f

def bounding_box(mask):
    # try:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    params = []
    if len(contours) > 0:
        
        for c in contours:
            obj_area = cv2.contourArea(c)
            
            if obj_area > 10:
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

print(str(width)+"x",str(height))

mask_red = masking(image, lower_red, upper_red)
wild_herbs = bounding_box(mask_red)


mask_green = masking(image, lower_green, upper_green)
herbs= bounding_box(mask_green)


try:

    #for i in herbs:
    #    cv2.rectangle(image, i[0], i[1], (0,255,0), 2)

    #for j in wild_herbs:
    #    cv2.rectangle(image, j[0], j[1], (255,0,0), 2)

    cv2.imshow("Image", image)
    
    cv2.imshow("herb", mask_green)
    cv2.imshow("wildherb", mask_red)

    
except:
    pass


cv2.waitKey(0)

cv2.destroyAllWindows()






#########video
"""
cap = cv2.VideoCapture("/Users/emirysaglam/Documents/GitHub/IP_general/tika/images/result1.png")


prev_frame_time = 0
# used to record the time at which we processed current frame
new_frame_time = 0
a = 0

while True:
    ret,frame = cap.read()
    if not ret:
        break
    width = frame.shape[1]
    height = frame.shape[0]

    mask_blue = masking(frame, lower_blue, upper_blue)

    blue_ball = bounding_box(mask_blue)

 #test ederken bakarız asıl kodda kapat

    try:
        cv2.drawContours(frame, blue_ball[7], -1, (0, 0, 255), 2)
        cv2.circle(frame, (blue_ball[5], blue_ball[6]), int(blue_ball[4] / 2), (0, 0, 0), 2)
        print("the frame is {} pixels on x plane and the object lies between {}-{}. pixels ".format(width,blue_ball[1],blue_ball[3]))

    except:
        pass

    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(frame, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Image", frame)

    cv2.waitKey(0)

cv2.destroyAllWindows()
"""