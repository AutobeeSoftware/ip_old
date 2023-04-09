import cv2
import numpy as np
#from scipy import ndimage
import matplotlib.pyplot as plt
from utils import gstreamer_pipeline



"""
# histogram grafiği ile görüntüdeki hsv değerleri analiz edilebilir
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hue = list(np.concatenate(hsv[:,:,0]).flat)
sat = list(np.concatenate(hsv[:,:,1]).flat)
val = list(np.concatenate(hsv[:,:,2]).flat)

plt.hist(val, bins=255)
plt.show()
"""

cap = cv2.VideoCapture(gstreamer_pipeline())

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

type = input("type (red/green)")

if type == "green":
    color = "green mask"
    lower_mask = np.array([48,22,80])
    upper_mask = np.array([67,180,180])

elif type == "red":
    color = "red mask"
    lower_mask = np.array([0,56,116])
    upper_mask = np.array([20,255,255])

else:
    print("unkown input")

# click s to save click q to quit


while True:  # sürekli kamerayı okutur
    
    ret,image = cap.read()
    if not ret:
        break

    image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)

    width = image.shape[1]
    heigth = image.shape[0]
    print(f"{width}x{heigth}")


    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min, sat_min, val_min])  # beyaz olacak pixellerin değer olark alt ve üst sınırları belirler
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.merge((mask,mask,mask))
    
    cv2.putText(image, "rgb", (width/2, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image, color , (width/2, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    
    im_v = cv2.vconcat([image, mask])

    cv2.imshow("Frame", im_v)  # img görüntüsünü gösteriyor
    cv2.imshow(color, mask)  # mask görüntüsünü gösteriyor
    
    k = cv2.waitKey(1)  
    
    if k == ord('q'):  
        break
    
    if k == ord('s'):  
        lower_mask = lower
        upper_mask = upper
        
        print(f"                       hue,saturation,value")
        print(f"{color} lower tresholds are{lower_mask}")
        print(f"{color} upper tresholds are{upper_mask}")
        





