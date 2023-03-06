import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt

# Kameranýn gordugu objeler tespit edilir.
# Objeler bir dortgen icerisine alinir ve merkezleri belirlenir.
# Dortgenlerin alaný ve merkezler bir dictionary'e kaydedilir.
# Daha sonra bu cisimlerin merkezlerinin ekranin ne tarafinda olduðu belirlenir.
# Once sol, daha sonra orta ve en son sag taraftaki cisimler kontrol edilir. Herhangi birinde birden fazla cisim varsa en buyuk cismin merkezine kirmizi bir daire koyulur.

def finding_mid_objects(image):
    area_merkez = {}
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,100,120])
    upper_red = np.array([10,255,255])

    lower_green = np.array([40,85,50])
    upper_green = np.array([70,255,255])

    mask1 = cv2.inRange(hsv,lower_red,upper_red)
    mask2 = cv2.inRange(hsv, lower_green, upper_green)

    cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts1 = imutils.grab_contours(cnts1)

    cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts2 = imutils.grab_contours(cnts2)

    for c in cnts1:
        area = cv2.contourArea(c)
        if area > 125:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            area_merkez.update({area:center})
        else:
            continue
    
    for c in cnts2:
        area = cv2.contourArea(c)
        if area > 125:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            area_merkez.update({area:center})
        else:
            continue
    
    size = image.shape
    x_value = size[1]

    sol = []
    sag = []
    orta = []

    for i in area_merkez: # Bulunan cisimlerin area degerleri farklý listelere kaydediliyor.
        if (x_value/2) - 20 < area_merkez[i][0] < (x_value/2) + 20:
            orta.append(i)
        elif area_merkez[i][0] < (x_value/2) - 20:
            sol.append(i)
        else:
            sag.append(i)

    if len(sol) == 0: # Aracin ne tarafa dogru dönecegi belirleniyor. Once sol, daha sonra orta ve en son sag taraf kontrol ediliyor.
        if len(orta) == 0:
            if len(sag) == 0:
                pass
            else:
                en_buyuk_deger = max(sag)
                cv2.circle(image, area_merkez[en_buyuk_deger], 3, (0,0,255), -1)
                # print("Saga don")
        else:
            en_buyuk_deger = max(orta)
            cv2.circle(image, area_merkez[en_buyuk_deger], 3, (0,0,255), -1)
            # print("Cisim ortadadir, duz devam et.")
    else:
        en_buyuk_deger = max(sol)
        cv2.circle(image ,area_merkez[en_buyuk_deger], 3, (0,0,255), -1)
        # print("Sola don")
        

# image = cv2.imread("result5.png")
# finding_mid_objects(image)
# cv2.imshow("result", image)
# cv2.waitKey(0)


cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    finding_mid_objects(frame)

    cv2.imshow("result", frame)
    k = cv2.waitKey(5)
    if k == ord("q"):
        break
    
cv2.destroyAllWindows()   
