import cv2


cap = cv2.VideoCapture(1)
extract_path = "/Users/emirysaglam/Documents/GitHub/IP_general/tika/"
count = 0
skip = 0

while True:
    ret, image = cap.read()
    print(0)
    if not ret:
        break
    
    
    """
    if skip % 9 == 0:
        cv2.imshow("Image", image[:, 180:900])
        cv2.imwrite(extract_path + f"tika_{count+1}.jpg",image[:, 180:900])
        count+=1

        print(extract_path + f"{count+1}.png" + " saved")
        print(count)

    k = cv2.waitKey(8)
        
    skip+=1
    """
    
    cv2.imshow("Image", image)

    k = cv2.waitKey(1)

    if k == ord('s'):  
        cv2.imwrite(extract_path + f"{count+1}.png",image)
        count+=1
    
    if k == ord('p'):  
            break
        
            
cv2.destroyAllWindows()

