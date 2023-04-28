import cv2
import numpy as np
import time
from utils import masking,bounding_box,closest,is_center,intersect,gstreamer_pipeline
import matplotlib.pyplot as plt
from operator import add

# hue values must be discrete
# bu degerler ortam ısıgına göre degisebilir test alaninada ayarlanmalı
# hsv_find dosyasini kullanarak bulunabilir



# atolye ici aksam test
lower_hsv = np.array([0,0,214])
upper_hsv = np.array([255,21,255])


font = cv2.FONT_HERSHEY_SIMPLEX

### fps icin ###
prev_image_time = 0
new_image_time = 0
a = 0
################

# fonskiyonun icine 0 atarak kamerayı aktiflestirebilirsin yoksa istedigin videonun yolunu yaz
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("camera failed")


while True:
    ret,image = cap.read()
    if not ret:
        break
    
    width = image.shape[1]
    height = image.shape[0]
    print(width,height)

    white = masking(image,lower_hsv,upper_hsv)
    object = bounding_box(white,200,"mermer")

    if object != None :
        print(object)
        
        for ind,obj in enumerate(object):
            (x, y), (w, h),tag = obj
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

            if w/h < 2:
                object.pop(ind)
                print("no obj")
                
            elif y > height*0.5 :
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
                cv2.putText(image, "STOP!", (int((x/2)+w),int((h/2)+y)), font, 0.7, (0,0,255), 2)
                print("STOP!")
            else:
                object.pop(ind)
                print("no obj")




    ### fps icin ##
    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    ##########

    cv2.imshow("frame",image)
    cv2.imshow("mask",white)


    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
    
cap.release()
cv2.destroyAllWindows()

