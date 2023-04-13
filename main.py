import cv2
import numpy as np
from scipy import ndimage
from tika import Bbox, Mask
import time
import matplotlib.pyplot as plt
from operator import add

# hue values must be discrete
# bu degerler ortam ısıgına göre degisebilir test alaninada ayarlanmalı
# hsv_find dosyasini kullanarak bulunabilir


"""
# atolye ici aksam test
lower_green = np.array([48,22,80])
upper_green = np.array([67,180,180])

lower_red = np.array([0,56,116])
upper_red = np.array([20,255,255])

"""


# atolye dısı gunduz test
lower_green = np.array([35,55,50])
upper_green = np.array([67,255,255])

lower_red = np.array([0,100,136])
upper_red = np.array([17,255,255])




font = cv2.FONT_HERSHEY_SIMPLEX

### fps icin ###
prev_image_time = 0
new_image_time = 0
a = 0
################

# fonskiyonun icine 0 atarak kamerayı aktiflestirebilirsin yoksa istedigin videonun yolunu yaz
cap = cv2.VideoCapture(0)


while True:
    ret,frame = cap.read()
    if not ret:
        break

    red = Mask(name = "red",image=frame,lower_hsv=lower_red, upper_hsv=upper_red)
    green = Mask(name = "green",image=frame,lower_hsv=lower_green, upper_hsv=upper_green)


    #intersect filtreleri atiliyor (son 3 framede de ortak olan pikseller aliniyor)
    #bonding box larin parametreleri belirleniyor
    print(red.getWidth)
    cv2.imshow("red", red.masking())

    wild_herbs = Bbox.setBbox("red",red.masking(),red.getWidth,30)
    herbs = Bbox.setBbox("green",green.masking(),green.getWidth,30)

    obj_loc = None

    if herbs == None and wild_herbs != None:
        combined = wild_herbs
        target = Bbox.closest(combined)
        # int(width/4) orta sayılcak genişliği belirler

    elif wild_herbs == None and herbs != None:
        combined = herbs
        target = Bbox.closest(combined)

        # int(width/4) orta sayılcak genişliği belirler

    elif wild_herbs != None and herbs != None:
        combined = herbs + wild_herbs
        target = Bbox.closest(combined)
        # int(width/4) orta sayılcak genişliği belirler
    else:
        print("no object found")

    # imshow yapilmiyosa gereksiz
    try:
        #bounding boxlari goruntude ciktisi aliniyor
        for i in herbs:
            cv2.rectangle(frame, (i.getX,i.getY), (i.getX + i.getW, i.getY + i.getH), (0,255,0), 2)
            cv2.putText(frame, "herb", (i.getX, i.getY +-15), font, 0.7, (0,255,0), 2)

        for j in wild_herbs:
            cv2.rectangle(frame, (i.getX,i.getY), (i.getX + i.getW, i.getY + i.getH), (0,0,255), 2)
            cv2.putText(frame, "wild herb",(i.getX, i.getY +-15), font, 0.7, (0,0,255), 2)
        
        if target != None:
            cv2.rectangle(frame, (target.getX,target.getY), (i.getX + i.getW, i.getY + i.getH), (255,0,0), 2)
            cv2.putText(frame, target.getTag, (target.getX, target.getY +-15), font, 0.7, (255,0,0), 2)
            cv2.putText(frame, target.getLoc, (target.getX, target.getY -40), font, 0.7, (255,0,0), 2)
        

    except:
        pass


    ### fps icin ##
    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(frame, "fps: " + fps, (red.width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    ##########

    cv2.line(frame,(int(red.width/4),0),(int(red.width/4),red.height),(255,0,0),2)
    cv2.line(frame,(int(red.width*3/4),0),(int(red.width*3/4),red.height),(255,0,0),2)
    cv2.imshow("frame", frame)
    cv2.imshow("red", red.masking())
    cv2.imshow("green", green.masking())


    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break

cv2.destroyAllWindows()

