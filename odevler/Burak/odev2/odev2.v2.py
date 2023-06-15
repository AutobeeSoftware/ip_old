import cv2 
import numpy as np
import imutils


def empty(img):
    pass


video = cv2.VideoCapture("golet_1.mp4")
video.set(3,640)       # genişlik
video.set(4,480)       # yükseklik


while True:
     _,frame= video.read()
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

     lower_red = np.array([0,100,120])
     upper_red = np.array([10,255,255])
     
     mask1 = cv2.inRange(hsv,lower_red,upper_red)
     cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     cnts1 = imutils.grab_contours(cnts1)
     
     q = []
     
     for c in cnts1:    
         area = cv2.contourArea(c)
         if area > 5000:
             peri=cv2.arcLength(c,True) 
             x,y,w,h=cv2.boundingRect(c)
             # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

             cv2.drawContours(frame,[c],-1,(0,0,255), 3)

             M = cv2.moments(c)

             cx = int(M["m10"]/ M["m00"])
             cy = int(M["m01"]/ M["m00"])
             
             center = [cx,cy]
             q.append(center)
             
             cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
             cv2.putText(frame,"RED",(cx-125,cy-125), cv2.FONT_HERSHEY_SIMPLEX,1.5, (0,0,255),3)

    
    
     lower_yellow = np.array([20,100,100])
     upper_yellow = np.array([30,255,255])

     mask2 = cv2.inRange(hsv,lower_yellow,upper_yellow)
     cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
     cnts2 = imutils.grab_contours(cnts2)
     
     a = []

     for c in cnts2:
         area = cv2.contourArea(c)
         if area > 5000:
             peri=cv2.arcLength(c,True) 
             x,y,w,h=cv2.boundingRect(c)
                 
             if 0.4<=w/h<=1:

                 # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
             
                 cv2.drawContours(frame,[c],-1,(0,255,255), 3)
    
                 M = cv2.moments(c)
    
                 cx = int(M["m10"]/ M["m00"])
                 cy = int(M["m01"]/ M["m00"])
                 
                 center = [cx,cy]
                 a.append(center)
    
                 cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                 cv2.putText(frame,"YELLOW",(cx-125,cy-125), cv2.FONT_HERSHEY_SIMPLEX,1.5, (0,255,255),3)

     if len(a) == 1 and len(q) == 1:
        if a[0][0] > q[0][0]:
            cv2.line(frame, (a[0][0], a[0][1]), (q[0][0], q[0][1]), (0,255,0), 2) 
        else:
            cv2.line(frame, (a[0][0], a[0][1]), (q[0][0], q[0][1]), (0,0,255), 2) 
                 
     # print(len(a))
     # print(len(q))

     cv2.imshow("result",frame)



     k = cv2.waitKey(10)
     if k == ord('q'):
         break

video.release()

cv2.destroyAllWindows()