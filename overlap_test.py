import cv2
import numpy as np
from utils2 import gstreamer_pipeline, camCombine





frameL = cv2.VideoCapture(gstreamer_pipeline(0))
frameR = cv2.VideoCapture(gstreamer_pipeline(1))

width = frameR.shape[1]
heigth = frameR.shape[0]
print(f"{width}x{heigth}")



# görüntüde hsv değerleri bulunup not edilir

def empty(img):
    pass

cv2.namedWindow("TrackBar")  # istenilen rengin filtrelenmei için trackbar oluşturma
cv2.resizeWindow("TrackBar", heigth+30, width*2, )
cv2.createTrackbar("overlap", "TrackBar", 0, width*2, empty)

# click s to save click q to quit


while True:  # sürekli kamerayı okutur
    

    overlap = cv2.getTrackbarPos("overlap", "TrackBar")


    combined = camCombine(frameL, frameR,overlap)

    cv2.putText(combined, "left cam", (int(0), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(combined, "right cam" , (int(width-10), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    

    cv2.imshow("TrackBar", combined)  # img görüntüsünü gösteriyor
    cv2.getTrackbarPos("TrackBar", "Frame")
    k = cv2.waitKey(1)  
    
    if k == ord('q'):  
        break
    
    if k == ord('s'):  
        print("overlap: " + str(overlap))



cv2.destroyAllWindows()