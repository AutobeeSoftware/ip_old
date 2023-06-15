import cv2
import numpy as np
import imutils

video = cv2.VideoCapture("golet_2.mp4")
video.set(3,640)
video.set(4,480)

while True:
    _,frame= video.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,100,120])
    upper_red = np.array([10,255,255])

    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])

    mask1 = cv2.inRange(hsv,lower_red,upper_red)
    mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)

    cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    sari_merkezler = []
    kirmizi_merkezler = []

    for c in cnts1:
        area = cv2.contourArea(c)
        if area > 5000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02*peri, True)
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "RED", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            cv2.circle(frame, center, 7, (255,255,255), -1)
            kirmizi_merkezler.append(center)

    for c in cnts2:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if 0.4 <= w/h <= 0.9:
            if area > 5000:           
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, "YELLOW", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,247,255), 2)
                center = (int(x+(w/2)), int(y+(h/2)))
                cv2.circle(frame, center, 7, (255,255,255), -1)
                sari_merkezler.append(center)
                
    if len(sari_merkezler) == 1 and len(kirmizi_merkezler) == 1:
        if sari_merkezler[0][0] > kirmizi_merkezler[0][0]: 
            cv2.line(frame, (sari_merkezler[0][0], sari_merkezler[0][1]), (kirmizi_merkezler[0][0], kirmizi_merkezler[0][1]), (0,255,0), 2)
            # Sarı duba referans olarak seçildi. Eğer sarı duba sağdaysa yeşil, soldaysa kırmızı çizgi çekiliyor.
        else:
            cv2.line(frame, (sari_merkezler[0][0], sari_merkezler[0][1]), (kirmizi_merkezler[0][0], kirmizi_merkezler[0][1]), (0,0,255), 2) 
    
    cv2.imshow("Frame", frame)

    k = cv2.waitKey(10)
    if k == ord("q"):
        break

video.release()
cv2.destroyAllWindows()