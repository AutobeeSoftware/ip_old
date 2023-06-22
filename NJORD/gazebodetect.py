#!/usr/bin/env python


from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from rover.msg import ball_location

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

        # Connect image topic
        self.img_topic = "/camera/rgb/image_raw"
        self.image_sub = rospy.Subscriber(self.img_topic, Image, self.callback)

        # Allow up to one second to connection
        rospy.sleep(1)

    def callback(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image
        #self.show_image(cv_image)
        self.find_object(cv_image)
        #self.move_to_object()

    def show_image(self,img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)
        

    def find_object(self,img):
        ball= ball_location()
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        hsv_frame = cv2.resize(hsv_frame,(640,300))

        low_H_R=0
        low_S_R=59
        low_V_R=21
        high_H_R=26
        high_S_R=255
        high_V_R=255

        low_H_B=0
        low_S_B=0
        low_V_B=0
        high_H_B=0
        high_S_B=0
        high_V_B=7
        
        low_H_G = 36 #53
        low_S_G= 0#87
        low_V_G=0#59
        high_H_G=86#130
        high_S_G=255
        high_V_G=255


        low_H_Y = 14
        low_S_Y= 0
        low_V_Y=0
        high_H_Y=36
        high_S_Y=255
        high_V_Y=119

        #<YELLOW
        mask_frame_yellow=cv2.inRange(hsv_frame, (low_H_Y, low_S_Y, low_V_Y), (high_H_Y, high_S_Y, high_V_Y))
        cv2.imshow("mask",mask_frame_yellow)
        _, contours_yellow, _= cv2.findContours(mask_frame_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #----------yellow>
        mask_frame_red=cv2.inRange(hsv_frame, (low_H_R, low_S_R, low_V_R), (high_H_R, high_S_R, high_V_R))
        cv2.imshow("mask",mask_frame_red)
        #contours, hierarchy = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        _, contours_red, _= cv2.findContours(mask_frame_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        mask_frame_green=cv2.inRange(hsv_frame, (low_H_G, low_S_G, low_V_G), (high_H_G, high_S_G, high_V_G))
        cv2.imshow("mask",mask_frame_green)
        #contours, hierarchy = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        _, contours_green, _= cv2.findContours(mask_frame_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #black
        mask_frame_black=cv2.inRange(hsv_frame, (low_H_B, low_S_B, low_V_B), (high_H_B, high_S_B, high_V_B))
        cv2.imshow("mask",mask_frame_black)
        _, contours_black, _= cv2.findContours(mask_frame_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        

        X_r,Y_r,W_r,H_r=0,0,0,0
        X_b,Y_b,W_b,H_b=0,0,0,0
        X_g,Y_g,W_g,H_g=0,0,0,0
        X_y,Y_y,W_y,H_y=0,0,0,0


        for pic, contour_r in enumerate(contours_red):
            area = cv2.contourArea(contour_r)
            
            if(area > 100):
                
                x_r, y_r, w_r, h_r = cv2.boundingRect(contour_r)
                if(w_r*h_r>W_r*H_r):
                    X_r, Y_r, W_r, H_r= x_r, y_r, w_r, h_r

        img = cv2.rectangle(img, (X_r+85, Y_r+280),(X_r +W_r+85, Y_r + H_r+280),(0, 0, 255), 2)
        self.cx_r =X_r
        self.cy_r = Y_r
        
        for pic, contour_g in enumerate(contours_green):
            area = cv2.contourArea(contour_g)
            
            if(area > 100):
                
                x_g, y_g, w_g, h_g = cv2.boundingRect(contour_g)
                if(w_g*h_g>W_g*H_g):
                    X_g, Y_g, W_g, H_g= x_g, y_g, w_g, h_g

        img = cv2.rectangle(img, (X_g+85, Y_g+280),(X_g +W_g+85, Y_g + H_g+280),(0, 0, 255), 2)
        self.cx_g =X_g
        self.cy_g = Y_g

        #YELLOW
        for pic, contour_y in enumerate(contours_yellow):
            area = cv2.contourArea(contour_y)
            
            if(area > 100):
                
                x_y, y_y, w_y, h_y = cv2.boundingRect(contour_y)
                if(w_y*h_y>W_y*H_y):
                    X_y, Y_y, W_y, H_y= x_y, y_y, w_y, h_y

        img = cv2.rectangle(img, (X_y+85, Y_y+280),(X_y +W_y+85, Y_y + H_y+280),(0, 0, 255), 2)
        self.cx_y =X_y
        self.cy_y = Y_y


        #BLACK
        for pic, contour_b in enumerate(contours_black):
            area = cv2.contourArea(contour_b)
            
            if(area > 40):
                
                x_b, y_b, w_b, h_b = cv2.boundingRect(contour_b)
                if(w_b*h_b>W_b*H_b):
                    X_b, Y_b, W_b, H_b= x_b, y_b, w_b, h_b

        img = cv2.rectangle(img, (X_b+85, Y_b+280),(X_b +W_b+85, Y_b + H_b+280),(0, 0, 255), 2)
        self.cx_b =X_b
        self.cy_b = Y_b
        
        print("Cx red: ",self.cx_r)
        print("Cx green: ", self.cx_g)
        print("Cx yellow: ", self.cx_y)
        print("Cx Black: ", self.cx_b)
        cv2.imshow("window", img)
        cv2.waitKey(3)
        obj_x=((self.cx_r+self.cx_g)/2)-320
        ball.middle= obj_x
        ball.black_location = self.cx_b
        ball.yellow_location = self.cx_y
        ball.isredfound  = True if self.cx_r > 0 else False
        ball.isgreenfound  = True if self.cx_g > 0 else False
        ball.isyellowfound  = True if self.cx_y > 0 else False
        ball.isblackfound  = True if self.cx_b > 0 else False
        self.pub.publish(ball)

if __name__ == '__main__':

    # Initialize
    rospy.init_node('take_photo', anonymous=False)
    camera = TakePhoto()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)
        rospy.spin()

    camera.stop