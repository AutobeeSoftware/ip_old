import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

img = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/tika/images/neut.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

hue = list(np.concatenate(hsv[:,:,0]).flat)
sat = list(np.concatenate(hsv[:,:,1]).flat)
val = list(np.concatenate(hsv[:,:,2]).flat)


arr = [1,2,3,4,5]
print(arr[:3])
#plt.hist(val, bins=255)
#plt.show() 


"""
cv2.imshow("img", img)
cv2.imshow("hsv", hsv)

cv2.waitKey(0)
"""
