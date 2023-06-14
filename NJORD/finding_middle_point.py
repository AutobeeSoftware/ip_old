import cv2
import numpy as np
import imutils

def determine_buoys(frame, mask1, mask2): # iki dubanın ortasını bulan fonksiyon

    cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    yesil_merkezler = []
    kirmizi_merkezler = []

    for c in cnts1:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if area > 3000:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "RED", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            cv2.circle(frame, center, 7, (255,255,255), -1)
            kirmizi_merkezler.append(center)

    for c in cnts2:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if area > 3000:          
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, "GREEN", (x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,247,255), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            cv2.circle(frame, center, 7, (255,255,255), -1)
            yesil_merkezler.append(center)
                
    if len(yesil_merkezler) == 1 and len(kirmizi_merkezler) == 1:
        middle_x = int((yesil_merkezler[0][0]+kirmizi_merkezler[0][0])/2) # iki dubanın orta noktası x koordinatı
        middle_y = int((yesil_merkezler[0][1]+kirmizi_merkezler[0][1])/2) # iki dubanın orta noktası y koordinatı
        cv2.line(frame, (middle_x, middle_y+50), (middle_x, middle_y-50), (0,0,255), 2) # iki dubanın orta noktasından bir çizgi çizildi 
        

cap = cv2.imread("dubalar.png")

lower_red = np.array([0,100,120])
upper_red = np.array([10,255,255])

lower_green = np.array([36, 25, 25])
upper_green = np.array([70,255,255])

hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv,lower_red,upper_red)
mask2 = cv2.inRange(hsv, lower_green, upper_green)
determine_buoys(cap, mask1, mask2)
cv2.imshow("frame", cap)
cv2.waitKey(0)
cv2.destroyAllWindows()

# while True:
#     _,frame = cap.read()
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     mask1 = cv2.inRange(hsv,lower_red,upper_red)
#     mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)
#     determine_buoys(frame, mask1, mask2)
#     cv2.imshow("Frame", frame)
#     k = cv2.waitKey(10)
#     if k == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()