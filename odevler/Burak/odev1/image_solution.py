import cv2
import numpy as np

img = cv2.imread("shapes6.png")
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                                 # yüklediğimiz resim griye çevrilir. Griye çevrilmesinin sebebi RGB de üç renk kanalı yani 3 boyut varken gri görüntüler tek boyutludur. Bu şekilde model karmaşıklığı azaltılır.

cv2.imshow("Detecting Shapes",img)                                              # detecting shapes adında bir pencere açıyoruz.
cv2.waitKey(0)                                                                  # klavye bağlama fonskiyonudur. 0 yazılırsa sonsuza kadar bekler

ret, thresh = cv2.threshold(img_gray,127,255,1)                                 # verilen görüntüyü siyah ve beyaz olarak ikili görüntüye çevirir. Kullanılma amacı, görüntü üzerinde gürültüleri azaltmak, görüntüyü belirginleştirmek ve nesneleri algılamaktır.

# cv2.imshow("aaa",ret)
# cv2.imshow("bbb",thresh)

contours, ret = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)         # konturlar aynı renk ve yoğunluğa sahip olan tüm kesintisiz noktaları sınır boyunca birleştiren kapalı eğrilerdir.     1. argüman kontur aranacak görüntü, ikinci argüman kontur alma, 3. argüman kontur yaklaşım metodu. contours değişkenine atanan bilgiler aslında görüntüdeki konturların pythondaki bir listesidir.Her kontur nesnenin sınır noktaları koordinatlarının(x,y) bir Numpy dizisidir.

for cnt in contours:
    peri=cv2.arcLength(cnt,True)                                                # konturun çevresini hesaplamak için kullanılır. True ifadesi konturun kapalı olduğunu ifade eder.
    # print(peri)
    approx=cv2.approxPolyDP(cnt, 0.02*peri, True)                               # gereksiz yerleri silme gibi düşünülebilir. yani bir kontur şeklini daha az sayıda köşeye sahip başka bir şekle yaklaştırır. ilk argüman kontur, 2.argüman yaklaşık kontur ile normal kontur arasındaki max masafe.  0.02 sayısını küçülttükçe hassaslık artıyor. döndürdüğü veri ise köşe noktaların koordinatları
    x,y,w,h=cv2.boundingRect(cnt)                                               # contur alanını dikdörtgen içine almak için
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.putText(img,"Points: "+str(len(approx)),(x+w, y+h),cv2.FONT_HERSHEY_COMPLEX, 0.7, (255,0,0),2)
    for i in range(len(approx)):
        print(approx[i])                         # köşe noktalarının koordinatları
    #     print(approx[i][0][0])
    #     print(approx[i][0][1])
    print()

    if len(approx)==4:

        q=[]
        q.append(pow(pow(approx[3][0][0]-approx[0][0][0],2)+pow(approx[3][0][1]-approx[0][0][1],2),0.5))
        
        for i in range(len(approx)-1):
            q.append(pow(pow(approx[i][0][0]-approx[i+1][0][0],2)+pow(approx[i][0][1]-approx[i+1][0][1],2),0.5))           # kenar uzunluklarını q listesine atıyorum. (x2-x1)^2+(y2-y1)^2  nin karekökü şeklinde
        
        for i in range(len(q)-1):
            if q[i]==q[i+1] and q[len(q)-1]==q[0]:                                                                       # tüm kenar uzunlukları eşit ise kare.  yaklaşık değerleri değil, tam olarak birbirlerine eşit ise kare
                cv2.putText(img,"Square:",(x+w-100, y+h),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
            else:
                cv2.putText(img,"Rectangle:",(x+w-200, y+h),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
        for i in range(len(q)):
            print(q[i])
   
    elif len(approx)==3:
        q=[]
        q.append(pow(pow(approx[2][0][0]-approx[0][0][0],2)+pow(approx[2][0][1]-approx[0][0][1],2),0.5))
        
        for i in range(len(approx)-1):
            q.append(pow(pow(approx[i][0][0]-approx[i+1][0][0],2)+pow(approx[i][0][1]-approx[i+1][0][1],2),0.5))
        
        for i in range(len(q)-1):
            if q[i]==q[i+1] and q[len(q)-1]==q[0]:
                cv2.putText(img,"Regular Triangle:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
                
            else:
                cv2.putText(img,"Traiangle:",(x+w-200, y+h+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
        
    elif len(approx)==5:
        q=[]
        q.append(pow(pow(approx[4][0][0]-approx[0][0][0],2)+pow(approx[4][0][1]-approx[0][0][1],2),0.5))
        
        for i in range(len(approx)-1):
            q.append(pow(pow(approx[i][0][0]-approx[i+1][0][0],2)+pow(approx[i][0][1]-approx[i+1][0][1],2),0.5))
        
        for i in range(len(q)-1):
            if q[i]==q[i+1] and q[len(q)-1]==q[0]:
                cv2.putText(img,"Regular Pentagon:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
                
            else:
                cv2.putText(img,"Pentagon:",(x+w-200, y+h+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
                
    
    elif len(approx)==6:
        q=[]
        q.append(pow(pow(approx[5][0][0]-approx[0][0][0],2)+pow(approx[5][0][1]-approx[0][0][1],2),0.5))
        
        for i in range(len(approx)-1):
            q.append(pow(pow(approx[i][0][0]-approx[i+1][0][0],2)+pow(approx[i][0][1]-approx[i+1][0][1],2),0.5))
        
        for i in range(len(q)-1):
            if q[i]==q[i+1] and q[len(q)-1]==q[0]:
                cv2.putText(img,"Regular Hexagon:",(x+w+20, y+h+45),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
                
            else:
                cv2.putText(img,"Hexagon:",(x+w-200, y+h+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)


    else:
        cv2.putText(img,"Circle:",(x+w-200, y+h+20),cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)


    cv2.imshow("Detecting Shapes",img)
    k=cv2.waitKey(0)
    if k==ord('q'):               # q ya bastığımda pencere kapanıyor
        break
    
cv2.destroyAllWindows()
    
# video solution ile siteyi birleştirmeye çalıştım



