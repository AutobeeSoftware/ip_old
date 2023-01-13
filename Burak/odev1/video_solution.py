import cv2 
import numpy as np
def empty(img):
    pass

fourrc = cv2.VideoWriter_fourcc(*'XVID')

out = cv2.VideoWriter("video.avi",fourrc,30.0, (640,480))  # 30 fps video, genişlik yükseklik

video = cv2.VideoCapture(0)
cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar",600,300)
cv2.createTrackbar("hue_min","TrackBar",0,179,empty)
cv2.createTrackbar("hue_max","TrackBar",179,179,empty)
cv2.createTrackbar("sat_min","TrackBar",0,255,empty)                            # burdaki trackbarlar videodaki renkleri kontrol etmek için tanımlanmıştır. videodaki resneye göre ayarlama yapılarak nesnenin şekli belirlenir.
cv2.createTrackbar("sat_max","TrackBar",255,255,empty)
cv2.createTrackbar("val_min","TrackBar",0,255,empty)
cv2.createTrackbar("val_max","TrackBar",255,255,empty)

while True:
    ret,img=video.read()

    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)                       # RGB formatına çevirir.
    hue_min=cv2.getTrackbarPos("hue_min","TrackBar")
    hue_max=cv2.getTrackbarPos("hue_max","TrackBar")
    sat_min=cv2.getTrackbarPos("sat_min","TrackBar")
    sat_max=cv2.getTrackbarPos("sat_max","TrackBar")
    val_min=cv2.getTrackbarPos("val_min","TrackBar")
    val_max=cv2.getTrackbarPos("val_max","TrackBar")
    
    lower = np.array([hue_min,sat_min,val_min])                      # renklerin alt sınırları
    upper = np.array([hue_max,sat_max,val_max])                      # renklerin üst sınırları
    mask=cv2.inRange(hsv, lower, upper)                                                     # 1.argüman renk tespiti kapılacak görüntü(RGB formatına çevrilen görüntü), 2.argüman algılamak istediğmiz rengin alt sınırı, 3.argüman algılamak istediğmiz rengin üst sınırı. renk tespitinin kolay olması için RGB ye çevrilmiştir.
    cnts,hei=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)                 # konturlar aynı renk ve yoğunluğa sahip olan tüm kesintisiz noktaları sınır boyunca birleştiren kapalı eğrilerdir.     1. argüman kontur aranacak görüntü, ikinci argüman kontur alma, 3. argüman kontur yaklaşım metodu. contours değişkenine atanan bilgiler aslında görüntüdeki konturların pythondaki bir listesidir.Her kontur nesnenin sınır noktaları koordinatlarının(x,y) bir Numpy dizisidir.
    for i in cnts:
        area=cv2.contourArea(i)
        if area>300:
            peri=cv2.arcLength(i,True)                                 # konturun çevresini hesaplamak için kullanılır. True ifadesi konturun kapalı olduğunu ifade eder.
            approx=cv2.approxPolyDP(i, 0.02*peri, True)                # gereksiz yerleri silme gibi düşünülebilir. yani bir kontur şeklini daha az sayıda köşeye sahip başka bir şekle yaklaştırır. ilk argüman kontur, 2.argüman yaklaşık kontur ile normal kontur arasındaki max masafe.  0.02 sayısını küçülttükçe hassaslık artıyor.  döndürdüğü veri ise köşe noktaların koordinatları 
            x,y,w,h=cv2.boundingRect(i)                                # contur alanını dikdörtgen içine almak için
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(img,"Points: "+str(len(approx)),(x+w+20, y+h+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)

        if len(approx)==4:
            cv2.putText(img,"Rectangle:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
        elif len(approx)==3:
            cv2.putText(img,"Traiangle:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
        else:
            cv2.putText(img,"Circle:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)

        
    cv2.imshow("Frame",img)
    # cv2.imshow("hsv",hsv)
    cv2.imshow("Mask",mask)
    
    out.write(img)
    
    k=cv2.waitKey(1)
    if k==ord('q'):
        break

video.release()
out.release()
cv2.destroyAllWindows()