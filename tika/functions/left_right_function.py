import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
    
def left_right(frame,mask1,mask2):

    cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)
    for c in cnts1:    
        area = cv2.contourArea(c)
        # print(area)
        if area > 100:
            peri=cv2.arcLength(c,True) 
            x,y,w,h=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    
            M = cv2.moments(c)
    
            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])
            
            cv2.circle(frame,(cx,cy),3,(255,255,255),-1)
            # print(cx,cy)
            
            if cx<width/2-20:
                print("kırmızı obje solda")
            elif cx>width/2+20:
                print("kırmızı obje sağda")
            else:
                print("kırmızı obje ortadadır.")
                
                
    cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)
    
    for c in cnts2:
        area = cv2.contourArea(c)
        # print(area)
        if area > 75:
            peri=cv2.arcLength(c,True) 
            x,y,w,h=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
             
            M = cv2.moments(c)
       
            cx = int(M["m10"]/ M["m00"])
            cy = int(M["m01"]/ M["m00"])
            cv2.circle(frame,(cx,cy),3,(255,255,255),-1)
            
            if cx<width/2-20:
                print("yeşil obje solda")
            elif cx>width/2+20:
                print("yeşil obje sağda")
            else:
                print("yeşil obje ortadadır.")



image = cv2.imread("result1.png")    
# plt.imshow(image)      
# plt.show()  

lower_red = np.array([0,100,120])
upper_red = np.array([10,255,255])
    
lower_green = np.array([40,85,50])
upper_green = np.array([70,255,255])

height = image.shape[0]
width = image.shape[1]   
  
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

mask_red = cv2.inRange(hsv,lower_red,upper_red)
# cv2.imshow("result.red",mask_red)

mask_green = cv2.inRange(hsv,lower_green,upper_green)
# cv2.imshow("result.green",mask_red)
    
left_right(image, mask_red, mask_green)
cv2.imshow("result",image)
cv2.waitKey(0)

cv2.destroyAllWindows()
    
