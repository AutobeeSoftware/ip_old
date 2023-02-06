import cv2


cap = cv2.VideoCapture('/Users/emirysaglam/Documents/GitHub/IP_general/video.mp4')
path = "/Users/emirysaglam/Documents/GitHub/IP_general/"
c=0

while True:
    ret, image = cap.read()

    if not ret:
        break

    cv2.imshow("Image", image)
    k = cv2.waitKey(0)  
    if k == ord('s'):  
        cv2.imwrite(path + f"{c+1}.png",image)
        c+=1

    if k == ord('p'):  
            break
        

cv2.destroyAllWindows()

