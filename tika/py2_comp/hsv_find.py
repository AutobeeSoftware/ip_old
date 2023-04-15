import cv2
import numpy as np
import matplotlib.pyplot as plt
#from utils import gstreamer_pipeline

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print ('camera failed')

_,img = cap.read()
img = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
width = img.shape[1]
heigth = img.shape[0]
print ('{0} x {1}'.format(width, heigth))

def empty(img):
    pass

type = raw_input("type (red/green)")

if type == "green":
    color = "green mask"
    lower_mask = np.array([48,22,80])
    upper_mask = np.array([67,180,180])

elif type == "red":
    color = "red mask"
    lower_mask = np.array([0,56,116])
    upper_mask = np.array([20,255,255])

else:
    print ("unknown input")
    color = "unknown"
    lower_mask = np.array([0,0,0])
    upper_mask = np.array([0,0,0])

cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar", heigth, width)
cv2.createTrackbar("hue_min", "TrackBar", lower_mask[0], 255, empty)
cv2.createTrackbar("hue_max", "TrackBar", upper_mask[0], 255, empty)
cv2.createTrackbar("sat_min", "TrackBar", lower_mask[1], 255, empty)
cv2.createTrackbar("sat_max", "TrackBar", upper_mask[1], 255, empty)
cv2.createTrackbar("val_min", "TrackBar", lower_mask[2], 255, empty)
cv2.createTrackbar("val_max", "TrackBar", upper_mask[2], 255, empty)

while True:
    
    ret,image = cap.read()
    if not ret:
        break

    image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)

    width = image.shape[1]
    heigth = image.shape[0]

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.merge((mask,mask,mask))

    cv2.putText(image, "rgb", (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(mask, color , (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)

    im_v = cv2.vconcat([image, mask])

    cv2.imshow("TrackBar", im_v)  
    cv2.getTrackbarPos("TrackBar", "Frame")
    k = cv2.waitKey(1)  

    if k == ord('q'):  
        break
        
    if k == ord('s'):  
        lower_mask = lower
        upper_mask = upper
        
        print("                            hue,sat,val")
        print("{} lower tresholds are {}".format(color, lower_mask))
        print("{} upper tresholds are {}".format(color, upper_mask))

