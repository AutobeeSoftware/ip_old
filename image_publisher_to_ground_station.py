#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time
from utils import masking,bounding_box,closest,is_center
from operator import add
from cv_bridge import CvBridge
import rospy
from tika_img_test.msg import herb_location
from utils import gstreamer_pipeline
from sensor_msgs.msg import Image

        
def image_publisher():

    # atolye ici aksam test
    lower_green = np.array([54,73,49])
    upper_green = np.array([64,180,195])

    lower_red = np.array([0,70,110])
    upper_red = np.array([33,255,255])
    
    lower_white = np.array([0,0,214])
    upper_white = np.array([255,21,255])
    """# atolye dısı gunduz test
    lower_green = np.array([35,55,50])
    upper_green = np.array([67,255,255])

    lower_red = np.array([0,100,136])
    upper_red = np.array([17,255,255])"""

    font = cv2.FONT_HERSHEY_SIMPLEX

    ### fps icin ###
    prev_image_time = 0
    new_image_time = 0
    a = 0
    ################

    #camera_id = "/dev/video0"
    #cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2) #usb camera
    cap = cv2.VideoCapture(gstreamer_pipeline(sensor_id = 0))  #csi camera

    
    
    
    fourcc = cv2.VideoWriter_fourcc(*"h264")
    out = cv2.VideoWriter("test3g.avi",fourcc,10.0,((960, 180)))

    bridge=CvBridge()


    rospy.init_node("image_publisher")
    pub = rospy.Publisher("location_of_the_herb", herb_location, queue_size=1)
    img_pub = rospy.Publisher("image_raw", Image, queue_size=1)
    msg = herb_location()
    
    while not rospy.is_shutdown():
        ret,image = cap.read()
        if not ret:
            break

        width = image.shape[1]
        height = image.shape[0]

        msg.isfound = False

        #anlık maskeleme yapılıyor
        mask_red = masking(image, lower_red, upper_red)
        mask_green = masking(image, lower_green, upper_green)
        mask_white = masking(image, lower_white, upper_white)


        #wild_herbs = bounding_box(red_inter,30,"wild herb")
        wild_herbs = bounding_box(mask_red,30,"wild herb")
        herbs = bounding_box(mask_green,30,"herb")
        mermer = bounding_box(mask_white,200,"mermer")
        if mermer != None :
            print(mermer)
        for ind,obj in enumerate(mermer):
            (x, y), (w, h),tag = obj
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)

            if w/h < 2:
                mermer.pop(ind)
                print("no obj")
                
            elif y > height*0.5 :
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,0), 2)
                cv2.putText(image, "STOP!", (int((x/2)+w),int((h/2)+y)), font, 0.7, (0,0,255), 2)
                ###########
                #ros
                print("STOP!")

            else:
                mermer.pop(ind)
                print("no obj")
        obj_loc = None
        nearest = None
        
        if herbs == None and wild_herbs != None:
            combined = wild_herbs
            nearest = closest(combined)
            obj_loc = is_center(nearest,width,int(width/4))
            # int(width/4) orta sayılcak genişliği belirler

        elif wild_herbs == None and herbs != None:
            combined = herbs
            nearest = closest(combined)
            obj_loc = is_center(nearest,width,int(width/4))
            # int(width/4) orta sayılcak genişliği belirler

        elif wild_herbs != None and herbs != None:
            combined = herbs + wild_herbs
            nearest = closest(combined)
            obj_loc = is_center(nearest,width,int(width/4))
            
            # int(width/4) orta sayılcak genişliği belirler
        
        else:
            print("no object found")

        if obj_loc != None:
            cx, cx_string = obj_loc
            (x,y), (w,h), tag = nearest

            msg.isfound = True
            msg.location.data = cx_string
            msg.herb_type.data = tag
        
        else:
            msg.isfound = False
            msg.location.data = ""
            msg.herb_type.data = ""
            
        print(herbs)
        print(wild_herbs)
        # imshow yapilmiyosa gereksiz
        try:
            #bounding boxlari goruntude ciktisi aliniyor
           
            for i in herbs:
                cv2.rectangle(image, i[0], tuple(map(add, i[0], i[1])), (0,255,0), 2)
                cv2.putText(image, "herb", (i[0][0], i[0][1] +-15), font, 0.7, (0,255,0), 2)

        except:
            pass
        
        try:
            
            for j in wild_herbs:
                cv2.rectangle(image, j[0],tuple(map(add, j[0], j[1])), (0,0,255), 2)
                cv2.putText(image, "wild herb",(j[0][0], j[0][1] - 15),font, 0.7, (0,0,255), 2)
            
        except:
            pass
       
        if nearest != None:
            print(nearest[0])
            print( list(map(add, nearest[0], nearest[1])))
            cv2.rectangle(image, nearest[0], tuple(map(add, nearest[0], nearest[1])), (255,0,0), 2)
            cv2.putText(image, nearest[2], (nearest[0][0], nearest[0][1] -15), font, 0.7, (255,0,0), 2)
            cv2.putText(image, cx_string, (nearest[0][0], nearest[0][1] -40), font, 0.7, (255,0,0), 2)
            
        ### fps icin ##
        new_image_time = time.time()
        fps = 1 / (new_image_time - prev_image_time)
        prev_image_time = new_image_time
        fps = int(fps)
        fps = str(fps)
        print("fps"+fps)
        cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.3, (0, 255, 255), 1, cv2.LINE_AA)
        ##########

        cv2.line(image,(int(width/4),0),(int(width/4),height),(255,0,0),2)
        cv2.line(image,(int(width*3/4),0),(int(width*3/4),height),(255,0,0),2)
        mask_red = cv2.merge((mask_red,mask_red,mask_red))
        mask_green = cv2.merge((mask_green,mask_green,mask_green))
        
        cv2.putText(mask_green, "geenmask" + fps, (width/2, 25), font, 0.3, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(mask_red, "redmask" + fps, (width/2, 25), font, 0.3, (0, 255, 255), 1, cv2.LINE_AA)
        


        test_out0 = cv2.hconcat([mask_green,image])
        test_out = cv2.hconcat([test_out0,mask_red])
        
        img_to_publish = bridge.cv2_to_imgmsg(image,"bgr8")
        print((test_out.shape[1],test_out.shape[0]))
        out.write(test_out)
        
        img_pub.publish(img_to_publish)
        pub.publish(msg)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        image_publisher()
    except rospy.ROSInterruptException:
        pass
