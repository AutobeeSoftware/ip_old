import cv2
import numpy as np
from scipy import ndimage
import time
import math

def masking(hsv, lower_hsv, upper_hsv, opening_kernel = 2, medianF_tresh = 2, horizon_tresh = 0):
    width = hsv.shape[1]

    # creating mask
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    
    if horizon_tresh > 0 :
        cv2.rectangle(mask, (0,0), (width,horizon_tresh), (0, 0, 0), -1)

    mask = cv2.bitwise_and(mask, mask, mask=mask)

    if opening_kernel > 0:
        # applying opening operation
        kernel = np.ones((opening_kernel, opening_kernel), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    if medianF_tresh > 0:
    # removing parasites
        mask = ndimage.median_filter(mask, size=medianF_tresh)

    return mask

def bounding_box(mask,tresh,tag):

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    params = []
    if len(contours) > 0:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for c in sorted_contours[:4]:
            obj_area = cv2.contourArea(c)
            
            if obj_area > tresh:
                x, y, w, h = cv2.boundingRect(c)
                params.append([(x+int(w/2), y+int(h/2)),obj_area,tag])

            else:
                print("no object found bigger than treshold")
                
       
        print("next frame")
        return params

    else:
        print("no contour found")
        return None


def intersect(mask1,mask2,mask3):

    intersect0 = cv2.bitwise_and(mask1,mask2)
    interset_3 = cv2.bitwise_and(intersect0,mask3)
    return interset_3

def is_center(params,width,tresh):

    if params != None:
        (cx,cy),area,tag = params
        if cx<int(width/2-tresh):
            print("on the left")
            cx_string = "left"
        elif cx>int(width/2+tresh):
            print("on the right")
            cx_string = "right"
        else:
            print("on the middle")
            cx_string = "middle"
        params.append(cx_string)
        print(params)

        return params

    else:
        return None

def last_turn(lastTurnDir,mask):

  
    height,width = mask.shape
    
    if lastTurnDir == "sol":
        cv2.rectangle(mask, (0,0), (int(width/2),height), (0, 0, 0), -1)

    elif lastTurnDir == "sag":
        cv2.rectangle(mask, (int(width/2),0), (width,height), (0, 0, 0), -1)

    else:
        cv2.rectangle(mask, (0,0), (int(width/4),height), (0, 0, 0), -1)
        cv2.rectangle(mask, (int(width*3/4),0), (width,height), (0, 0, 0), -1)

    return mask

def closest(params):
    if params != None:
        cache = 0
        ind = None
        for index,object in enumerate(params):
            (cx,cy), area, tag = object
            if cache < cy:
                cache = cy
                ind = index
            else:
                continue
        if ind != None:
            return params[ind]
    else:
        return None




def gstreamer_pipeline(
    sensor_id=0,
    capture_width=480,
    capture_height=360,
    display_width=480,
    display_height=360,
    framerate=30,
    flip_method=0,
):

    """
    >>cv2.VideoCapture(gstreamer_pipeline()) 
    """
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def between_buoys(objs1, objs2): 
    # objs1 should on the rigth side
    ccx = 0
    ccy = 0
    isForward = None
    distence=0

    center_of_obj1 = closest(objs1)
    center_of_obj2 = closest(objs2)

    if center_of_obj1 != None  and  center_of_obj2 != None:
        (cx1,cy1), area1, tag1 = center_of_obj1
        (cx2,cy2), area2, tag2 = center_of_obj2

        ccx = int((cx1 + cx2)/2)
        ccy = int((cy1 + cy2)/2)
        distence = int(math.sqrt((cx1-cx2)**2 + (cy1 - cy2)**2))

        if cx1 > cx2:
            isForward = True
        else:
            isForward = False
    
    elif center_of_obj1 == None  and  center_of_obj2 != None:
        (cx2,cy2), area2, tag2 = center_of_obj2
        ccx = cx2
        ccy = cy2
        print(f"no object: {tag2}")

    elif center_of_obj1 != None  and  center_of_obj2 == None:
        (cx1,cy1), area1, tag1 = center_of_obj1
        ccx = cx1
        ccy = cy1
        print(f"no object: {tag1}")
    else:
        
        print("no objects")

    return [(ccx,ccy),isForward,distence]
   

