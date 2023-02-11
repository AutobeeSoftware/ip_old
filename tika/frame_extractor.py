import cv2


cap = cv2.VideoCapture('C:/Users/ertug/Desktop/video.mp4')
path = "C:/Users/ertug/Desktop/data"
c=0

while True:
    ret, image = cap.read()

    if not ret:
        break

    cv2.imshow("Image", image)
    #cv2.imwrite(path + f"{c+1}.png",image)
    c+=1

    print(path + f"{c+1}.png" + " saved")
    k = cv2.waitKey(10)
    
    """    
    if k == ord('s'):  
        cv2.imwrite(path + f"{c+1}.png",image)
        c+=1
    """
    if k == ord('p'):  
            break
        

cv2.destroyAllWindows()

