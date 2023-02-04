import cv2
import numpy as np
from scipy import ndimage
import time
from utils import masking,bounding_box,intersect
import matplotlib.pyplot as plt
from operator import add

# hue values must be discrete
# bu degerler ortam ısıgına göre degisebilir test alaninada ayarlanmalı
# hsv_find dosyasini kullanarak bulunabilir
"""
# atolye ici aksam test
lower_green = np.array([48,80,50])
upper_green = np.array([67,180,180])

lower_red = np.array([0,88,80])
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
cap = cv2.VideoCapture('/Users/emirysaglam/Desktop/video2.mp4')

#intersect fonksiyonu icin son 3 maskeyi tutuyo
red_mask_cache=[]
green_mask_cache=[]

while True:
    ret,image = cap.read()
    if not ret:
        break

    width = image.shape[1]
    height = image.shape[0]

    #anlık maskeleme yapılıyor
    mask_red = masking(image, lower_red, upper_red)
    red_mask_cache.append(mask_red)

    mask_green = masking(image, lower_green, upper_green)
    green_mask_cache.append(mask_green)

    #cache arraylari belli bir boyutta tutuyor
    if len(red_mask_cache) > 3:
        red_mask_cache.pop(0)
        green_mask_cache.pop(0)
    else:
        continue
    
    #intersect filtreleri atiliyor (son 3 framede de ortak olan pikseller aliniyor)
    #bonding box larin parametreleri belirleniyor

    red_inter = intersect(red_mask_cache[0],red_mask_cache[1],red_mask_cache[2])
    wild_herbs = bounding_box(red_inter,50)

    green_inter = intersect(green_mask_cache[0],green_mask_cache[1],green_mask_cache[2])
    herbs = bounding_box(green_inter,50)

    # imshow yapilmiyosa gereksiz
    try:
        #bounding boxlari goruntude ciktisi aliniyor
        for i in herbs:
            cv2.rectangle(image, i[0], list(map(add, i[0], i[1])), (0,255,0), 2)
            cv2.putText(image, "herb", (i[0][0]+ 10, i[0][1] + 15), font, 0.7, (0,255,0), 2)

        for j in wild_herbs:
            cv2.rectangle(image, j[0],list(map(add, j[0], j[1])), (0,0,255), 2)
            cv2.putText(image, "wild herb",(j[0][0]+ 10, j[0][1] + 15),font, 0.7, (0,0,255), 2)

    except:
        pass


    ### fps icin ##
    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    ##########

    cv2.imshow("Image", image)
    cv2.imshow("red", mask_red)
    cv2.imshow("green", mask_green)


    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
    

cv2.destroyAllWindows()

