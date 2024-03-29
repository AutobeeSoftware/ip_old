import cv2
import numpy as np
from scipy import ndimage
import time

def masking(img, lower_hsv, upper_hsv, opening_kernel = 2, medianF_tresh = 2, horizon_tresh = 0):
    """
    sınır hsv değerleri ile maske çıkarıp 
    bu maskey opening ve median filter ile sadeleştirme fonskiyonu
    input olarak -> görüntü , alt sınır , üst sınır

    *kernel değişkeni ve median filterdaki size değişkeni
    duruma göre değiştirilebilir boyut ne kadar artarsa o kadar yoğun 
    bir filtreleme yapılır
    """
    
    width = img.shape[1]

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    
    #kameranın konumuna göre yukarı atılcak maskenin boyutunu değiştirbilirsin 
    if horizon_tresh > 0 :
        cv2.rectangle(mask, (0,0), (width,horizon_tresh), (0, 0, 0), -1)

    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((opening_kernel, opening_kernel), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=medianF_tresh)

    return mask_f


def bounding_box(mask,tresh,tag):
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
            print(obj_area)
            
            if obj_area > tresh:
                x, y, w, h = cv2.boundingRect(c)
                params.append([(x, y), (w, h),tag])

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

def is_center(params,width,tresh):
    """
    bounding_box fonksiyonundan alınan parametrelerden yola çıkarak
    cismin konumunu ekrana göre nerde olduğunu verir bunu belirli bir
    treshhold değerine göre yapar

    cismin merkezinin vulunduğu pikselin x eksenindeki yerini verir

    görüntünün genişliği de parametre olarak verilmeli

    printlerin bir manası yok ros için farklı outpular ayarlanabilir
    """
    if params != None:
        (x,y),(w,h),tag = params
        cx = x+ int(w/2)
        if cx<int(width/2-tresh):
            print("on the left")
            cx_string = "left"
        elif cx>int(width/2+tresh):
            print("on the right")
            cx_string = "right"
        else:
            print("on the middle")
            cx_string = "middle"
        
        print([cx,cx_string])

        return [cx,cx_string]

    else:
        return None

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

    else:
        cv2.rectangle(mask, (0,0), (int(width/4),height), (0, 0, 0), -1)
        cv2.rectangle(mask, (int(width*3/4),0), (width,height), (0, 0, 0), -1)
        #sol ve sağ 1/4 lük alana maske atıldı

    return mask

def closest(params):
    """
    kameraya en yakın bounding boxı verir
    boduning_box fonksiyonun çıktısını ver
    """
    cache = 0
    ind = None
    for index,object in enumerate(params):
        (x,y),(w,h),tag = object
        if cache < w*h:
            cache = w*h
            ind = index
        else:
            continue
    if ind != None:
        return params[ind]
    else:
        return None

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):

    """
    opencv ile çağırınca 960x540dan mı alıyo 1920x180den mi?
    >>cv2.VideoCapture(gstreamer_pipeline()) 
    """
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
#cumulate fonksiyonu ekle