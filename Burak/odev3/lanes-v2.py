import cv2
import numpy as np
import matplotlib.pyplot as plt

class LaneDetection:
    def __init__(self):
        self.image = cv2.imread("result1.png")      
        # cv2.namedWindow("result", cv2.WINDOW_NORMAL)    
        # cv2.resizeWindow("result", 1000, 500)
        self.lane_image = np.copy(self.image)
        self.canny_image = self.canny(self.lane_image)
        self.cropped_image = self.region_of_interest(self.canny_image)
        self.lines = cv2.HoughLinesP(self.cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)            
        self.averaged_lines = self.average_slope_intercept(self.lane_image, self.lines)
        self.line_image = self.display_lines(self.lane_image, self.averaged_lines)
        self.combo_image = cv2.addWeighted(self.lane_image, 0.8, self.line_image, 1, 1)
        # plt.imshow(canny_image)      
        # plt.show()         
        # cv2.imwrite("result2.png",combo_image)
        cv2.imshow("result", self.combo_image)
        cv2.waitKey(0)

    def make_coordinates(self, image, line_parameters):    
        if line_parameters[0]==1.0:
            y1,y2,x1,x2 = 2,2,1,2
        else:
            slope, intercept = line_parameters
            y1 = image.shape[0]
            y2 = int(y1*(3/5))
            x1 = int((y1-intercept)/slope)
            x2 = int((y2-intercept)/slope)    
        return np.array([x1,y1,x2,y2])

    def average_slope_intercept(self, image, lines):
        left_fit = []
        right_fit = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2), (y1,y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if slope<0:
                left_fit.append((slope,intercept))
            else:
                right_fit.append((slope,intercept))
                
        if len(left_fit)==0:
            left_fit.append([1])
        elif len(right_fit)==0:
            left_fit.append([1])

        left_fit_average = np.average(left_fit, axis=0)
        right_fit_average = np.average(right_fit, axis=0)    
        left_line = self.make_coordinates(image, left_fit_average)
        right_line = self.make_coordinates(image, right_fit_average)
        return np.array([left_line, right_line])
        
    def canny(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)    
        blur = cv2.GaussianBlur(gray, (5,5),0)    
        canny = cv2.Canny(blur,50,150)       
        return canny

    def display_lines(self, image, lines):
        line_image = np.zeros_like(image)
        if lines is not None:
            
            x1,y1,x2,y2 = lines[0].reshape(4)
            xx1,yy1,xx2,yy2 = lines[1].reshape(4)
            m1 = (y2-y1)/(x2-x1)
            m2 = (yy2-yy1)/(xx2-xx1)
            
            a = (x1+x2)/2
            b = (xx1+xx2)/2
            X1 = int((a+b)/2)        # orta noktanın x koordinatı
            c = (y1+y2)/2
            d = (yy1+yy2)/2
            Y1 = int((c+d)/2)        # orta noktanın y koordinatı  
            
            
            if m2<0.85:
                print("sola dön")
                
            elif m2>2.5:
                print("sağa dön")
                
            elif a>350:
                print("sola dön")
                
            elif b<350:
                print("sağa dön")            
            else:
                print("düz devam et") 
                       
            if -5<m1<-0.5:
                    cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
                    
            if 0<m2<12:
                    cv2.line(line_image, (xx1,yy1), (xx2,yy2), (255,0,0), 10)
                    
            if m1==0.0 or m2==0.0:
                cv2.circle(image,(0,0),1,(0,0,0),1)   
                
            if -5<m1<-0.5 and 0<m2<12:
                cv2.circle(image,(X1,Y1),10,(0,0,255),5)
        return line_image
                
    def region_of_interest(self, image):
        height = image.shape[0]
        polygons = np.array([
            [(0,500), (750,height), (200,175)]                    
            ])
        mask = np.zeros_like(image)    
        cv2.fillPoly(mask,polygons,(255))
        masked_image = cv2.bitwise_and(image, mask)
        return masked_image


#### VIDEO
# cap = cv2.VideoCapture("lane_video.mp4")
# while(cap.isOpened()):
#     _, frame = cap.read()
#     canny_image = canny(frame)
#     cropped_image = region_of_interest(canny_image)
#     lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
#     averaged_lines = average_slope_intercept(frame, lines)
#     line_image = display_lines(frame, averaged_lines)
#     combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

#     # plt.imshow(canny_image)      
#     # plt.show() 
#     cv2.imshow("result",combo_image)
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()

LaneDetection()