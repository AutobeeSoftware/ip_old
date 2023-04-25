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
lower_green = np.array([48,22,80])
upper_green = np.array([67,180,180])


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

#intersect fonksiyonu icin son 3 maskeyi tutuyo
green_mask_cache=[]

while True:
    ret,image = cap.read()
    if not ret:
        break
    
    width = image.shape[1]
    height = image.shape[0]
    print(width,height)

    #anlık maskeleme yapılıyor
    mask_green = masking(image, lower_green, upper_green)
    green_mask_cache.append(mask_green)

    #cache arraylari belli bir boyutta tutuyor
    if len(green_mask_cache) > 3:
        green_mask_cache.pop(0)
    else:
        continue
    
    #intersect filtreleri atiliyor (son 3 framede de ortak olan pikseller aliniyor)
    #bonding box larin parametreleri belirleniyor

    green_inter = intersect(green_mask_cache[0],green_mask_cache[1],green_mask_cache[2])
    herbs = bounding_box(green_inter,50,"herb")

    obj_loc = None
    if herbs != None :
        nearest = closest(herbs)
        obj_loc = is_center(nearest,width,int(width/4))
        
    # int(width/4) orta sayılcak genişliği belirler

    if obj_loc != None:
        cx, cx_string = obj_loc
    # imshow yapilmiyosa gereksiz

    try:
        #bounding boxlari goruntude ciktisi aliniyor
        for i in herbs:
            cv2.rectangle(image, i[0], tuple(map(add, i[0], i[1])), (0,255,0), 2)
            cv2.putText(image, "herb", (i[0][0], i[0][1] +-15), font, 0.7, (0,255,0), 2)

    except:
        pass

    if nearest != None:
        cv2.rectangle(image, nearest[0], tuple(map(add, nearest[0], nearest[1])), (255,0,0), 2)
        cv2.putText(image, nearest[2], (nearest[0][0], nearest[0][1] -15), font, 0.7, (255,0,0), 2)
        cv2.putText(image, cx_string, (nearest[0][0], nearest[0][1] -40), font, 0.7, (255,0,0), 2)
    
    ### fps icin ##
    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    ##########

    cv2.line(image,(int(width/4),0),(int(width/4),height),(255,0,0),2)
    cv2.line(image,(int(width*3/4),0),(int(width*3/4),height),(255,0,0),2)
    
    mask_green = cv2.merge((mask_green,mask_green,mask_green))

    cv2.putText(image, "rgb", (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(mask_green, "mask_green" , (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    im_v = cv2.hconcat([image, mask_green])
    cv2.imshow("Frame", im_v)  # img görüntüsünü gösteriyor

    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
    
cap.release()
cv2.destroyAllWindows()

