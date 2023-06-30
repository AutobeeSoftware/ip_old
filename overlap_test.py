import cv2
import numpy as np
from utils2 import gstreamer_pipeline

import threading
import numpy as np


class CSI_Camera:

    def __init__(self):
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False

    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
            # Grab the first frame to start the video capturing
            self.grabbed, self.frame = self.video_capture.read()

        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)


    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running = True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running = False
        # Kill the thread
        self.read_thread.join()
        self.read_thread = None

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed = self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()



def camCombine(frameL,frameR,overlap):
   
    if frameL.shape[0] == frameR.shape[0] and frameL.shape[1] == frameR.shape[1]:
        h = frameL.shape[0]
        w = frameR.shape[1]
        frameL = frameL[:h, : w - overlap] 
        frameR = frameR[:h, overlap :]

        combined_frame = np.hstack((frameL, frameR))


        return combined_frame

    else:
        return None





#frameL = cv2.VideoCapture(gstreamer_pipeline(0),cv2.CAP_GSTREAMER)
#frameR = cv2.VideoCapture(gstreamer_pipeline(1),cv2.CAP_GSTREAMER)

left_camera = CSI_Camera()
left_camera.open(gstreamer_pipeline(0))
left_camera.start()

right_camera = CSI_Camera()
right_camera.open(gstreamer_pipeline(1))
right_camera.start()


_, frameL = left_camera.read()
_, frameR = right_camera.read()

width = frameL.shape[1]
heigth = frameL.shape[0]
print((width , heigth))





def empty(img):
    pass

cv2.namedWindow("TrackBar")  
cv2.resizeWindow("TrackBar", heigth+30, width*2, )
cv2.createTrackbar("overlap", "TrackBar", 0, width*2, empty)

# click s to save click q to quit


while True:  
    

    overlap = cv2.getTrackbarPos("overlap", "TrackBar")
    _, frameL = left_camera.read()
    _, frameR = right_camera.read()

    combined = camCombine(frameL, frameR,overlap)

    cv2.putText(combined, "left cam", (int(0), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(combined, "right cam" , (int(width-10), 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    

    cv2.imshow("TrackBar", combined)  
    cv2.getTrackbarPos("TrackBar", "Frame")
    k = cv2.waitKey(30)  
    
    if k == ord('q'):  
        break
    
    if k == ord('s'):  
        print("overlap: " + str(overlap))



cv2.destroyAllWindows()