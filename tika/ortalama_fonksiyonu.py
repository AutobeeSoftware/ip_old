import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt

# Objenin merkezini bul ve merkezin koordinat de�erlerini listeye kaydet.
# Ekran�n orta noktas�n� bul ve koordinat de�erlerini ba�ka bir listeye kaydet.
# E�er objenin x de�eri daha b�y�kse sa�a d�n yazd�r. (Ara� sa�a d�nmeli.)
# E�er ekran�n x de�eri daha b�y�kse sola d�n yazd�r. (Ara� sola d�nmeli.)
# E�er ekran�n ve objenin x de�erleri e�itse ortalanm��t�r. Obje ortaland� yaz.

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
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            area_merkez.update({area:center})
            # cv2.circle(image, center, 3, (0,255,255), -1)
        else:
            continue
    
    for c in cnts2:
        area = cv2.contourArea(c)
        if area > 100:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            center = (int(x+(w/2)), int(y+(h/2)))
            area_merkez.update({area:center})
            # cv2.circle(image, center, 3, (0,255,255), -1)
        else:
            continue
    
    # print(area_merkez)

    size = image.shape
    x_value = size[1]

    sol = []
    sag = []
    orta = []

    for i in area_merkez:
        if (x_value/2) - 20 < area_merkez[i][0] < (x_value/2) + 20:
            #print("Obje ortada, duz devam et.")
            orta.append(i)
        elif area_merkez[i][0] < (x_value/2) - 20:
            # print("Obje soldadir,sola don.")
            sol.append(i)
        else:
            # print("Obje sagdadir, saga don.")
            sag.append(i)

    if len(sol) == 0:
        if len(sag) == 0:
            if len(orta) == 0:
                print("Obje Yok")
            else:
                print("Cisim ortadadir, duz devam et.")
        else:
            print("Saga don")
    else:
        print("Sola don")

        
    cv2.imshow("result", image)
    cv2.waitKey(0)


image = cv2.imread("result1.png")
finding_mid_objects(image)
# finding_mid_screen(image)
cap = cv2.VideoCapture("video.mp4")


# while True:
#     ret, frame = cap.read()
#     finding_mid_screen(frame)

#     cv2.imshow("result", frame)
#     k = cv2.waitKey(15)
#     if k == ord("q"):
#         break

# cv2.destroyAllWindows()   
