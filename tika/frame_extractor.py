import cv2


cap = cv2.VideoCapture('C:/Users/ertug/Desktop/video.mp4')
path = "C:/Users/ertug/Desktop/"
c=0

while True:
    ret, image = cap.read()

    if not ret:
        break

    cv2.imshow("Image", image)
    k = cv2.waitKey(0)  # ???????
    if k == ord('s'):  # ord function returns an integer representing the Unicode character
        cv2.imwrite(path + f"{c+1}.png",image)
        c+=1

cv2.destroyAllWindows()

