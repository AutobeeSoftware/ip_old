import cv2
import numpy as np
from scipy import ndimage
import time
from utils import masking,bounding_box,closest,last_turn,is_center,intersect,gstreamer_pipeline
import matplotlib.pyplot as plt
from operator import add

# hue values must be discrete
# bu degerler ortam ısıgına göre degisebilir test alaninada ayarlanmalı
# hsv_find dosyasini kullanarak bulunabilir



# atolye ici aksam test
lower_green = np.array([48,22,80])
upper_green = np.array([67,180,180])

lower_red = np.array([0,56,116])
upper_red = np.array([20,255,255])


lower_white = np.array([0,0,214])
upper_white = np.array([255,21,255])

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
    
    image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)

    width = image.shape[1]
    height = image.shape[0]
    print(width,height)

    #anlık maskeleme yapılıyor
    mask_red = masking(image, lower_red, upper_red)
    mask_green = masking(image, lower_green, upper_green)
    mask_white = masking(image, lower_white, upper_white)


    #intersect filtreleri atiliyor (son 3 framede de ortak olan pikseller aliniyor)
    #bonding box larin parametreleri belirleniyor

    wild_herbs = bounding_box(mask_green,100,"wild herb")
    herbs = bounding_box(mask_red,100,"herb")
    mermer = bounding_box(mask_white,200,"mermer")
    
    if mermer != None :
        print(mermer)
        for ind,obj in enumerate(mermer):
            (x, y), (w, h),tag = obj
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

            if w/h < 2:
                mermer.pop(ind)
                print("no obj")
                
            elif y > height*0.5 :
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,0), 2)
                cv2.putText(image, "STOP!", (int((x/2)+w),int((h/2)+y)), font, 0.7, (0,0,255), 2)
                ###########
                #ros
                print("STOP!")

            else:
                mermer.pop(ind)
                print("no obj")



    obj_loc = None
    nearest = None

    if herbs == None and wild_herbs != None:
        combined = wild_herbs
        nearest = closest(combined)
        obj_loc = is_center(nearest,width,int(width/4))
        # int(width/4) orta sayılcak genişliği belirler

    elif wild_herbs == None and herbs != None:
        combined = herbs
        nearest = closest(combined)
        obj_loc = is_center(nearest,width,int(width/4))
        # int(width/4) orta sayılcak genişliği belirler

    elif wild_herbs != None and herbs != None:
        combined = herbs + wild_herbs
        nearest = closest(combined)
        obj_loc = is_center(nearest,width,int(width/4)) 
        # int(width/4) orta sayılcak genişliği belirler
    else:
        print("no object found")

    if obj_loc != None:
        cx, cx_string = obj_loc
        (x,y), (w,h), tag = nearest


    # imshow yapilmiyosa gereksiz
    try:
            #bounding boxlari goruntude ciktisi aliniyor
        
        for i in herbs:
            cv2.rectangle(image, i[0], tuple(map(add, i[0], i[1])), (0,255,0), 2)
            cv2.putText(image, "herb", (i[0][0], i[0][1] +-15), font, 0.7, (0,255,0), 2)

    except:
        pass
    
    try:
        
        for j in wild_herbs:
            cv2.rectangle(image, j[0],tuple(map(add, j[0], j[1])), (0,0,255), 2)
            cv2.putText(image, "wild herb",(j[0][0], j[0][1] - 15),font, 0.7, (0,0,255), 2)
        
    except:
        pass
    
    if nearest != None:
        print(nearest[0])
        print( list(map(add, nearest[0], nearest[1])))
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
    
    mask_red = cv2.merge((mask_red,mask_red,mask_red))
    mask_green = cv2.merge((mask_green,mask_green,mask_green))

    cv2.putText(image, "rgb", (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(mask_red, "mask_red" , (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(mask_green, "mask_green" , (int(width/2), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    im_v = cv2.hconcat([mask_red,image, mask_green])
    cv2.imshow("Frame", im_v)  # img görüntüsünü gösteriyor
    cv2.imshow("mask",mask_white)

    k = cv2.waitKey(1)  
    if k == ord('q'):  
        break
    
cap.release()
cv2.destroyAllWindows()

