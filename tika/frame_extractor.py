import cv2


cap = cv2.VideoCapture('/Users/emirysaglam/Documents/GitHub/IP_general/tika/data/data_collect.mov')
extract_path = "/Users/emirysaglam/Documents/GitHub/IP_general/tika/data/data_frames/"
count = 0
skip = 0

while True:
    ret, image = cap.read()

    if not ret:
        break
    
    

    if skip % 9 == 0:
        cv2.imshow("Image", image[:, 180:900])
        cv2.imwrite(extract_path + f"tika_{count+1}.jpg",image[:, 180:900])
        count+=1

        print(extract_path + f"{count+1}.png" + " saved")
        print(count)

    k = cv2.waitKey(8)
        
    skip+=1
    """    
    if k == ord('s'):  
        cv2.imwrite(path + f"{count+1}.png",image)
        c+=1
    """
    if k == ord('p'):  
            break
        

cv2.destroyAllWindows()

