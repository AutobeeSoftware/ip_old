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
from jetson_utils import videoSource, videoOutput,cudaToNumpy
import cv2
import numpy as np
import time
from utils import masking,bounding_box,closest,is_center,intersect,gstreamer_pipeline
import matplotlib.pyplot as plt
from operator import add



net = detectNet(argv=['--model=path-to.onnx', '--labels=path-to-labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'])


camera = videoSource("csi://0")      # '/dev/video0' for V4L2
display = videoOutput("display://0") # 'my_video.mp4' for file

lower_green = np.array([48,22,80])
upper_green = np.array([67,180,180])
font = cv2.FONT_HERSHEY_SIMPLEX


while display.IsStreaming():
	img = camera.Capture()
	print(img.shape())
	"""	
	image = img.cudaToNumpy()
	mask_green = masking(image, lower_green, upper_green)
	herbs = bounding_box(mask_green,50,"herb")

	obj_loc = None
	if herbs != None :
		nearest = closest(herbs)
		obj_loc = is_center(nearest,img.width(),int(img.width()/4))
		obj_loc.append("herb")
    # int(width/4) orta sayılcak genişliği belirler
	if obj_loc != None:
		cx, cx_string , tag = obj_loc
	
	try:
	#bounding boxlari goruntude ciktisi aliniyor
		for i in herbs:
			cv2.rectangle(image, i[0], tuple(map(add, i[0], i[1])), (0,255,0), 2)
			cv2.putText(image, "herb", (i[0][0], i[0][1] +-15), font, 0.7, (0,255,0), 2)

	except:
		pass

	if nearest != None:
		cv2.rectangle(image, nearest[0], tuple(map(add, nearest[0], nearest[1])), (255,0,0), 2)
		cv2.putText(image, nearest[2], (nearest[0][0], nearest[0][1] -15), font, 0.7, (255,0,0), 2)
		cv2.putText(image, cx_string, (nearest[0][0], nearest[0][1] -40), font, 0.7, (255,0,0), 2)

	cv2.line(image,(int(img.width()/4),0),(int(img.width()/4),img.heigth()),(255,0,0),2)
	cv2.line(image,(int(img.width()*3/4),0),(int(img.width()*3/4),img.heigth()),(255,0,0),2)

	img = image.cudaFromNumpy()
	"""
	detections = net.Detect(img)
	print(detections)

	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

