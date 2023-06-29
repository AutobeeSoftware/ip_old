import cv2
import numpy as np



def camCombine(frameL,frameR,overlap):
    # İki kameradan alınan kareleri aynı boyuta getiriyoruz
   
    if frameL.shape[0] == frameR.shape[0] and frameL.shape[1] == frameR.shape[1]:
        h = frameL.shape[0]
        w = frame1.shape[1]
        frameL = frameL[:h, : w - overlap] 
        frameR = frame2[:h, overlap :]

        # İki kareyi yatay olarak birleştiriyoruz
        combined_frame = np.hstack((frameL, frameR))


        return combined_frame

    else:
        return None



frame1 = cv2.imread("test2.jpg")
frame2 = cv2.imread("test1.jpg")

width = frame1.shape[1]
heigth = frame1.shape[0]
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


    combined = camCombine(frame1, frame2,overlap)

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