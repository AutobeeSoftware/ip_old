import cv2
import numpy as np
#from scipy import ndimage
import matplotlib.pyplot as plt

img = cv2.imread("C:/Users/ertug/Documents/GitHub/IP_general/tika/images/herb1.png")

width = img.shape[1]
heigth = img.shape[0]
print(f"{width}x{heigth}")

img = cv2.resize(img, (0, 0), fx = 0.4, fy = 0.4)
"""
# histogram grafiği ile görüntüdeki hsv değerleri analiz edilebilir
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hue = list(np.concatenate(hsv[:,:,0]).flat)
sat = list(np.concatenate(hsv[:,:,1]).flat)
val = list(np.concatenate(hsv[:,:,2]).flat)

plt.hist(val, bins=255)
plt.show()
"""

# görüntüde hsv değerleri bulunup not edilir

def empty(img):
    pass

cv2.namedWindow("TrackBar")  # istenilen rengin filtrelenmei için trackbar oluşturma
cv2.resizeWindow("TrackBar", 600, 300, )
cv2.createTrackbar("hue_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("hue_max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("sat_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("val_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("val_max", "TrackBar", 255, 255, empty)

lower_mask = None
upper_mask = None

while True:  # sürekli kamerayı okutur

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min, sat_min, val_min])  # beyaz olacak pixellerin değer olark alt ve üst sınırları belirler
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("Frame", img)  # img görüntüsünü gösteriyor
    cv2.imshow("Mask", mask)  # mask görüntüsünü gösteriyor
    
    k = cv2.waitKey(1)  
    
    if k == ord('q'):  
        break
    
    if k == ord('s'):  
        lower_mask = lower
        upper_mask = upper
        print(f"lower mask tresholds are{lower_mask}")
        print(f"upper mask tresholds are{upper_mask}")
        





