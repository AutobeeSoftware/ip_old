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
    
    frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)
    width = frame.shape[1]
    height = frame.shape[0]

    print(width,height)
    red = Mask(name = "red",image=frame,lower_hsv=lower_red, upper_hsv=upper_red)
    green = Mask(name = "green",image=frame,lower_hsv=lower_green, upper_hsv=upper_green)

    red_mask = red.masking()
    green_mask = green.masking()
    

    #intersect filtreleri atiliyor (son 3 framede de ortak olan pikseller aliniyor)
    #bonding box larin parametreleri belirleniyor

    wild_herbs = Bbox.setBbox("red",red_mask,red.getWidth(),30)
    herbs = Bbox.setBbox("green",green_mask,green.getWidth(),30)
    
    print(len(wild_herbs))
    print(len(herbs))
    
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
            print(i.getTag())
            cv2.rectangle(frame, (i.getX(),i.getY()), (i.getX() + i.getW(), i.getY() + i.getH()), (0,255,0), 2)
            cv2.putText(frame, "herb", (i.getX(), i.getY() +-15), font, 0.7, (0,255,0), 2)

        for j in wild_herbs:
            print(j.getTag())
            cv2.rectangle(frame, (i.getX(),i.getY()), (i.getX() + i.getW(), i.getY() + i.getH()), (0,0,255), 2)
            cv2.putText(frame, "wild herb",(i.getX(), i.getY() +-15), font, 0.7, (0,0,255), 2)
        
        if target != None:
            print(target.getTag())
            cv2.rectangle(frame, (target.getX(),target.getY()), (i.getX() + i.getW(), i.getY() + i.getH()), (255,0,0), 2)
            cv2.putText(frame, target.getTag(), (target.getX(), target.getY() +-15), font, 0.7, (255,0,0), 2)
            cv2.putText(frame, target.getLoc(), (target.getX(), target.getY() -40), font, 0.7, (255,0,0), 2)
        

    except:
        pass


    ### fps icin ##
    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(frame, "fps: " + fps, (red.getWidth() - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    ##########

    cv2.line(frame,(int(red.getWidth()/4),0),(int(red.getWidth()/4),red.getHeigth()),(255,0,0),2)
    cv2.line(frame,(int(red.getWidth()*3/4),0),(int(red.getWidth()*3/4),red.getHeigth()),(255,0,0),2)
    
    red_mask = cv2.merge((red_mask,red_mask,red_mask))
    green_mask = cv2.merge((green_mask,green_mask,green_mask))

    cv2.putText(frame, "rgb", (int(red.getWidth()/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(red_mask, "mask_red" , (int(red.getWidth()/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(green_mask, "mask_green" , (int(red.getWidth()/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    im_v = cv2.hconcat([red_mask,frame, green_mask])

    cv2.imshow("Frame", im_v)  # img görüntüsünü gösteriyor



    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
cap.release()
cv2.destroyAllWindows()

