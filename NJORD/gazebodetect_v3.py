#!/usr/bin/env python


from __future__ import print_function
import sys
import subprocess
import rospy
import rosbag
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image, LaserScan
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from ball_detection_pck.msg import ball_location
import utils2
import math

class TakePhoto:
    def __init__(self):
        rospy.loginfo("started")
        self.pub=rospy.Publisher('/camera_data',ball_location,queue_size=10)
        self.rate=rospy.Rate(1)
        self.rot=Twist()
        self.x = 1
        self.cx_r=0
        self.cy_r=0
        self.cx_b=0
        self.cy_b=0 
        self.cx_g=0
        self.cy_g=0
        self.cx_y=0
        self.cy_y=0
        
        self.bridge = CvBridge()
        self.image_received = False
        """
        # Connect image topic
        self.img_topic = "/usb_cam/image_raw"
        self.image_sub = rospy.Subscriber(self.img_topic, Image, self.callback)
        cap = cv2.VideoCapture(utils2.gstreamer_pipeline())
        # Allow up to one second to connection
        rospy.sleep(1)

        while not rospy.is_shutdown():
        # Convert image to OpenCV format
            self.image_received,self.image=cap.read()

    
            #self.show_image(cv_image)
            self.find_object(self.image)
            #self.move_to_object()

    def show_image(self,img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(1)
        
        """
    def find_object(self):
        cap=cv2.VideoCapture(utils2.gstreamer_pipeline())#cv2.VideoCapture(0)
        while not rospy.is_shutdown():
            _,img=cap.read()
            ball= ball_location()
            hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
            #hsv_frame = cv2.resize(hsv_frame,(640,300))
            
            width = hsv_frame.shape[1]
            heigth = hsv_frame.shape[0]

            print((width,heigth))
            
    
            low_H_R=0
            low_S_R=92
            low_V_R=127
            high_H_R=10
            high_S_R=255
            high_V_R=255
    
    
    
            low_H_B=142
            low_S_B=0
            low_V_B=108
            high_H_B=255
            high_S_B=35
            high_V_B=174
            
            low_H_G = 46 #53
            low_S_G= 56#87
            low_V_G=106#59
            high_H_G=73#130
            high_S_G=255
            high_V_G=255
    
    
            low_H_Y = 25
            low_S_Y= 72
            low_V_Y=151
            high_H_Y=63
            high_S_Y=255
            high_V_Y=251
    
            #<YELLOW                                                                                                 # both are for removing parasites in mask 
            mask_frame_yellow = utils2.masking(hsv_frame, (low_H_Y, low_S_Y, low_V_Y), (high_H_Y, high_S_Y, high_V_Y), opening_kernel = 0, medianF_tresh = 0)
            yellows = utils2.bounding_box(mask_frame_yellow,100,"yellow")
            cv2.imshow("mask_yellow",mask_frame_yellow)
            #----------yellow>
    
            #<RED   
            mask_frame_red = utils2.masking(hsv_frame, (low_H_R, low_S_R, low_V_R), (high_H_R, high_S_R, high_V_R), opening_kernel = 0, medianF_tresh = 0)
            reds = utils2.bounding_box(mask_frame_red,100,"red")
            cv2.imshow("mask_red",mask_frame_red)
            #----------red>
            
            #<GREEN   
            mask_frame_green = utils2.masking(hsv_frame, (low_H_G, low_S_G, low_V_G), (high_H_G, high_S_G, high_V_G), opening_kernel = 0, medianF_tresh = 0)
            greens = utils2.bounding_box(mask_frame_green,100,"green")        
            cv2.imshow("mask_green",mask_frame_green)
            #----------green>
            
            #<BLACK   
            mask_frame_black = utils2.masking(hsv_frame, (low_H_B, low_S_B, low_V_B), (high_H_B, high_S_B, high_V_B), opening_kernel = 0, medianF_tresh = 0)
            blacks = utils2.bounding_box(mask_frame_black,100,"black")       
            cv2.imshow("mask_black",mask_frame_black)
             #----------black>
    
            X_r,Y_r,W_r,H_r=0,0,0,0
            X_b,Y_b,W_b,H_b=0,0,0,0
            X_g,Y_g,W_g,H_g=0,0,0,0
            X_y,Y_y,W_y,H_y=0,0,0,0
    
            try :
                self.cx_r = reds[0][0]
                self.cy_r = reds[0][1]
            except:
                self.cx_r = 0.0
                self.cy_r = 0.0
            
            try:
                self.cx_g = greens[0][0]
                self.cy_g = greens[0][1]
            except:
                self.cx_g = 0.0
                self.cy_g = 0.0
                
            try:
                self.cx_y = yellows[0][0]
                self.cy_y = yellows[0][1]
            except:
                self.cx_y = 0.0
                self.cy_y = 0.0
    
            try:
                self.cx_b = blacks[0][0]
                self.cy_b = blacks[0][0]
            except:
                self.cx_b = 0.0
                self.cy_b = 0.0
    
            middle = utils2.between_buoys(reds,greens)
    
            print("Cx red: ",self.cx_r)
            print("Cx green: ", self.cx_g)
            print("Cx yellow: ", self.cx_y)
            print("Cx Black: ", self.cx_b)
            print("middle:",middle)
    
    ##for visualising##
            font = cv2.FONT_HERSHEY_SIMPLEX
    
            try:
                if middle[1] == True: 
                    cv2.circle(img, middle[0], int(middle[2]*0.05), (255,255,255), 2)
                else:
                    cv2.circle(img, middle[0],  int(middle[2]*0.05), (0,0,0), 2)
            except:
                pass
            
            try:
                for i in greens:
                    radius = int( math.sqrt(i[1] / math.pi))
                    cv2.circle(img, i[0], radius, (0,255,0), 2)
                    cv2.putText(img, "green", (i[0][0], i[0][1] - 15), img, 0.7, (0,255,0), 2)
            except:
                pass
            
            try:
                for j in reds:
                    
                    radius = int( math.sqrt(j[1] / math.pi))
                    cv2.circle(img, j[0], radius, (0,0,255), 2)
                    cv2.putText(img, "red", (j[0][0], j[0][1] - 15), font, 0.7, (0,0,255), 2)
            except:
                pass    
            
            try:
                for k in yellows:
                    
                    radius = int( math.sqrt(k[1] / math.pi))
                    cv2.circle(img, k[0], radius, (0,255,255), 2)
                    cv2.putText(img, "yellow", (k[0][0], k[0][1] - 15), font, 0.7, (0,255,255), 2)
            except:
                pass
            
            try:
                for z in blacks:
                    
                    radius = int( math.sqrt(z[1] / math.pi))
                    cv2.circle(img, z[0], radius, (0,255,255), 2)
                    cv2.putText(img, "black", (z[0][0], z[0][1] - 15), font, 0.7, (0,255,255), 2)
                
            except:
                pass
    
    
            cv2.imshow("Image", img)
    
    
            cv2.waitKey(1)
            ########
    
    
            obj_x = middle[0][0]-width/2
            ball.middle= obj_x
            try:   
                ball.black_location = blacks[0][0][0]
            except:
                ball.black_location = self.cx_b
            try:   
                ball.yellow_location = yellows[0][0][0]
            except:
                ball.yellow_location = self.cx_y
    
            ball.isredfound  = True if self.cx_r > 0.0 else False
            ball.isgreenfound  = True if self.cx_g > 0.0 else False
            ball.isyellowfound  = False # if self.cx_y > 0.0 else False
            ball.isblackfound  = False #if self.cx_b > 0.0 else False
            self.pub.publish(ball)




if __name__ == '__main__':

      
    # Initialize
    rospy.init_node('take_photo', anonymous=False)
    """
    bag =rosbag.Bag("/home/autobee2023/rosbagfiles/test.bag", "w")
    bag.write("cam_data", ball_location)
    bag.write("lidar", LaserScan)
    """	
    camera = TakePhoto()
    camera.find_object()
    
    while not rospy.is_shutdown():
        rospy.sleep(0.1)
        rospy.spin()
    #bag.close()

    camera.stop
