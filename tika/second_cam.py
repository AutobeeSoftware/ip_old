import cv2
import numpy as np
import imutils

def masking(image, lower, upper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    return mask

cap = cv2.VideoCapture(0)
if not cap.isOpened:
    print("no image") 

lower_red = np.array([0,100,120])
upper_red = np.array([10,255,255])

ret,image = cap.read()
area_ = image.shape[1]*image.shape[0]*0.2


while True:
    ret,image = cap.read()
    mask = masking(image, lower_red, upper_red)
    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            area = cv2.contourArea(c)
            if area > area_:
                x,y,w,h = cv2.boundingRect(c)
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
                #### cikti ekle

    cv2.imshow("result", image)
    k = cv2.waitKey(1)
    if k == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()   



    


