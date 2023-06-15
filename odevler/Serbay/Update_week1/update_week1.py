import cv2
import numpy as np
import math
from sklearn.cluster import KMeans

def empty(img):
    pass

video = cv2.VideoCapture(0)
cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar", 600, 300)
cv2.createTrackbar("hue_min", "Trackbar", 0, 179, empty)
cv2.createTrackbar("hue_max", "Trackbar", 179, 179, empty)
cv2.createTrackbar("sat_min", "Trackbar", 0, 255, empty)
cv2.createTrackbar("sat_max", "Trackbar", 255, 255, empty)
cv2.createTrackbar("val_min", "Trackbar", 0, 255, empty)
cv2.createTrackbar("val_max", "Trackbar", 255, 255, empty)

while True:
    ret,img = video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))


    hue_min = cv2.getTrackbarPos("hue_min", "Trackbar")
    hue_max = cv2.getTrackbarPos("hue_max", "Trackbar")
    sat_min = cv2.getTrackbarPos("sat_min", "Trackbar")
    sat_max = cv2.getTrackbarPos("sat_max", "Trackbar")
    val_min = cv2.getTrackbarPos("val_min", "Trackbar")
    val_max = cv2.getTrackbarPos("val_max", "Trackbar")
    lower = np.array([hue_min,sat_min,val_min])
    upper = np.array([hue_max,sat_max,val_max])

    mask = cv2.inRange(hsv, lower, upper)

    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 300:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Points: "+ str(len(approx)), (x+w+20, y+h+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2)
        if len(approx) == 4:
            cv2.putText(img, "Rectangle", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,255), 2)
        elif len(approx) == 3:
            corners = cv2.cornerHarris(gray, 2, 3, 0.04)
            coords = np.argwhere(corners > 0.01*corners.max())
            km = KMeans(
                n_clusters=3, init='random',
                n_init=10, max_iter=300, 
                tol=1e-04, random_state=0
            )
            y_km = km.fit_predict(coords)
            merkezler = km.cluster_centers_
            a = int(math.sqrt((merkezler[0][0] - merkezler[1][0])**2 + (merkezler[0][1]-merkezler[1][1])**2))
            b = int(math.sqrt((merkezler[0][0] - merkezler[2][0])**2 + (merkezler[0][1]-merkezler[2][1])**2))
            c = int(math.sqrt((merkezler[1][0] - merkezler[2][0])**2 + (merkezler[1][1]-merkezler[2][1])**2))
            if a == b == c:
                cv2.putText(img, "Equilateral Triangle", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)
            else:
                cv2.putText(img, "Triangle", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)

        elif len(approx) == 6:
            cv2.putText(img, "Hexagon", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,0), 2)
                    
        else:
            cv2.putText(img, "Circle", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Frame", img)
    cv2.imshow("hsv", hsv)
    cv2.imshow("Mask", mask)
    k = cv2.waitKey(10)
    if k == ord("q"):
        break

video.release()
cv2.destroyAllWindows()