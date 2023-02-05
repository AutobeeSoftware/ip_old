import cv2
import numpy as np
from scipy import ndimage
import time
from utils import masking,bounding_box
"""
font = cv2.FONT_HERSHEY_SIMPLEX
path = "C:/Users/ertug/Desktop/frame/"



frame1 = cv2.imread(path + "5.png")
frame2 = cv2.imread(path + "6.png")
frame3 = cv2.imread(path + "7.png")

width = frame1.shape[1]
height = frame1.shape[0]

def intersect(mask1,mask2,mask3):
    intersect0 = cv2.bitwise_and(mask1,mask2)
    interset_3 = cv2.bitwise_and(intersect0,mask3)
    return interset_3



lower_red = np.array([0,88,43])
upper_red = np.array([20,255,255])




mask1 = masking(frame1, lower_red, upper_red)
mask2 = masking(frame2, lower_red, upper_red)
mask3 = masking(frame3, lower_red, upper_red)

cv2.imshow("1",mask1)
cv2.imshow("2",mask2)
cv2.imshow("3",mask3)

cv2.imshow("int",intersect(mask1,mask2,mask3))


cv2.waitKey(0)
cv2.destroyAllWindows()
"""

from operator import add


"""arr = (1,3)
arr2 = (3,4)
print(list( map(add, arr, arr2) ))"""

arr = [[(1,2),(2,3)],[(3,4),(4,5)],[(5,6),(6,7)]]
names = ["herb" for i in range(len(arr))]

t = dict(zip(names, arr))
print(t)

fruits = ["Apple", "Pear", "Peach", "Banana"]
prices = [0.35, 0.40, 0.40, 0.28]

fruit_dictionary = dict(zip(fruits, prices))

print(fruit_dictionary)