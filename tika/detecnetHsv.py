#!/usr/bin/env python3
#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#







from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, cudaAllocMapped, cudaResize,cudaToNumpy,cudaFromNumpy

net = detectNet(argv=['--model=/home/autobee2023/Desktop/tika-ssd-v0.2/mb2-ssd-lite-v3.3-e32-b33-L2.0.onnx', '--labels=/home/autobee2023/Desktop/tika-ssd-v0.2/labelsv2.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'])
#net = detectNet("ssd-mobilenet-v2", threshold=0.5)

camera = videoSource("csi://0",argv=['--input - flip=rotate-180'])# '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file


import cv2
import numpy as np
from utils2 import masking,bounding_box,closest,is_center

lower_green = np.array([48,22,80])
upper_green = np.array([67,180,180])
font = cv2.FONT_HERSHEY_SIMPLEX



while display.IsStreaming():
    img_in = camera.Capture()
    img = cudaAllocMapped( width = img_in.width * 0.2 ,
                           height = img_in.height * 0.2,
                           format = img_in.format)
    cudaResize(img_in, img)
    
    herbs = []
    ############green
    
    image = cudaToNumpy(img)
    mask_green = masking(image, lower_green, upper_green)
    green = bounding_box(mask_green,50,"herb")
    if green != None:
        herbs = herbs + green
    #############red
    detections = net.Detect(img)
    for i in detections:
        cx = int(i.Center[0])
        cy = int(i.Center[1])
        herbs.append([(cx,cy),"wild"])
    #############combined
    

    obj_loc = None
    nearest = None
    
    if herbs != None :
        nearest = closest(herbs)
        obj_loc = is_center(nearest,img.width,int(img.width/4))
    
    if obj_loc != None:
    		(cx,cy),tag ,cx_string = obj_loc
    	
    ####################display    
    try:
    		for i in herbs:
    			cv2.circle(image, i[0], 2, (0,255,0), 2)
    			cv2.putText(image, i[1], (i[0][0], i[0][1] +-15), font, 0.7, (0,255,0), 2)
    
    except:
    		pass
    
    if nearest != None:
    		cv2.circle(image, nearest[0], 2, (255,0,0), 2)
    		cv2.putText(image, nearest[1], (nearest[0][0], nearest[0][1] -15), font, 0.7, (255,0,0), 2)
    		cv2.putText(image, nearest[2], (nearest[0][0], nearest[0][1] -40), font, 0.7, (255,0,0), 2)
    
    
    img = cudaFromNumpy(image)
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
