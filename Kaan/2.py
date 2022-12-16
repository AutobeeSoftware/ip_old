import cv2
import numpy as np



img = cv2.imread('shape4.jpg.tiff')
cv2.imshow('original', img)
cv2.waitKey(0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 170, 255)
ret,thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)
(contours,_) = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
def detectShape(c):
       shape = 'unknown'
       peri=cv2.arcLength(cnt,True)
       vertices = cv2.approxPolyDP(cnt, 0.02 * peri, True)
       sides = len(vertices)
       if (sides == 3):
            shape='triangle'
       elif(sides==4):
             x,y,w,h=cv2.boundingRect(cnt)
             aspectratio=float(w)/h
             if (aspectratio==1):
                   shape='square'
             else:
                   shape="rectangle"
       elif(sides==5):
            shape='pentagon'
       elif(sides==6):
            shape='hexagon'
       elif(sides==8):
            shape='octagon'
       elif(sides==10):
            shape='star'
       else:
           shape='circle'
       return shape
for cnt in contours:
    moment=cv2.moments(cnt)
    cx = int(moment['m10'] / moment['m00'])
    cy = int(moment['m01'] / moment['m00'])
    shape=detectShape(cnt)
    cv2.drawContours(img,[cnt],-1,(0,255,0),2)
    cv2.putText(img,shape,(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    cv2.imshow('polygons_detected',img)
cv2.waitKey(0)
cv2.destroyAllWindows()