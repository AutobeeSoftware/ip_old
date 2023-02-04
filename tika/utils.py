import cv2
import numpy as np
from scipy import ndimage
import time

def masking(img, lower_hsv, upper_hsv):
    """
    sınır hsv değerleri ile maske çıkarıp 
    bu maskey opening ve median filter ile sadeleştirme fonskiyonu
    input olarak -> görüntü , alt sınır , üst sınır

    *kernel değişkeni ve median filterdaki size değişkeni
    duruma göre değiştirilebilir boyut ne kadar artarsa o kadar yoğun 
    bir filtreleme yapılır
    """
    
    width = img.shape[1]
    height = img.shape[0]

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    cv2.rectangle(mask, (0,0), (width,int(height/4)), (0, 0, 0), -1)

    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((2, 2), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=2)

    return mask_f


def bounding_box(mask,tresh):
    """
    input olarak maskeyi alır ve maskedeki alanların en büyük 4ünden 
    alanı tresholdun üstünde olanların sol üst köşesinin koordinatları ve 
    bounding box ın uzunluk ve genişliğini verir aksi halde None verir
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    params = []
    if len(contours) > 0:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for c in sorted_contours[:4]:
            obj_area = cv2.contourArea(c)
            
            if obj_area > tresh:
                x, y, w, h = cv2.boundingRect(c)
                params.append([(x, y), (w, h)])

            else:
                print("no object found bigger than treshold")
                
       
        print("next frame")
        return params

    else:
        print("no contour found")
        return None


def intersect(mask1,mask2,mask3):
    """
    parazit azaltmak icin son uc makenin kesisimini alir ve 
    bu kesişim maskesini verir
    """
    intersect0 = cv2.bitwise_and(mask1,mask2)
    interset_3 = cv2.bitwise_and(intersect0,mask3)
    return interset_3

def is_middle(params,width,tresh):
    """
    bounding_box fonksiyonundan alınan parametrelerden yola çıkarak
    cismin konumunu ekrana göre nerde olduğunu verir bunu belirli bir
    treshhold değerine göre yapar

    görüntünün genişliği de parametre olarak verilmeli

    prinlerin bir manası yok ros için farklı outpular ayarlanabilir
    """
    x,y,w,h= params
    cx = x+ int(w/2)

    if cx<width/2-tresh:
        print("on the left")
    elif cx>width/2+tresh:
        print("on the right")
    else:
        print("on the middle")


def last_turn(lastTurnDir,mask):

    """
    araç otları ilaçlamak için ortalarken büyük bir dönüş yapmışsa başka
    sıraya atlayabilir bunun için dönüş bilgisinden yola çıkarak aracın 
    değerlendirdiği alan kısıtlanarak sıradan şaşmasını engellenir

    output olarak yine maske verir

    rosdan dönüş bilgisi alınmalı bkz. lastTurnDir
    """
  
    height,width = mask.shape
    
    if lastTurnDir == "sol":
        cv2.rectangle(mask, (0,0), (int(width/2),height), (0, 0, 0), -1)
        #sol yarıya maske atıldı

    elif lastTurnDir == "sag":
        cv2.rectangle(mask, (int(width/2),0), (width,height), (0, 0, 0), -1)
        #sağ yarıya maske atıldı

    elif lastTurnDir == None:
        cv2.rectangle(mask, (0,0), (int(width/4),height), (0, 0, 0), -1)
        cv2.rectangle(mask, (int(width*3/4),0), (width,height), (0, 0, 0), -1)
        #sol ve sağ 1/4 lük alana maske atıldı

    return mask