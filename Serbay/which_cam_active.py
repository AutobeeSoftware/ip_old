import cv2

cam1 = cv2.VideoCapture(0) # primer camera
cam2 = cv2.VideoCapture(1) # seconder camera
id_ = {cam1 : "0001", cam2: "0002"}

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()
    if ret1 is not True and ret2 is not True: # if both cam are not active
        print(f"{id_[cam1]}\n{id_[cam2]}")
        break
    elif ret1 is not True: # if only cam1 is not active
        print(id_[cam1])
        break
    elif ret2 is not True: # if only cam2 is not active
        print(id_[cam2])
        break

    cv2.imshow("cam1", frame1)
    cv2.imshow("cam2", frame2)
    cv2.waitKey(5)

cv2.destroyAllWindows()