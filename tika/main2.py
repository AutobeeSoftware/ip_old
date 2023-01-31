import cv2
import numpy as np
from scipy import ndimage
import time
import matplotlib.pyplot as plt

# hue values must be discrete

# lower_blue = np.array([130, 74, 230])
# upper_blue = np.array([185, 170, 255])

lower_green = np.array([76,31,56])
upper_green = np.array([104,62,30])

lower_red = np.array([24,65,78])
upper_red = np.array([9,92,65])



def masking(img, lower_hsv, upper_hsv):

    # creating mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    bitw = cv2.bitwise_and(mask, mask, mask=mask)

    # applying opening operation
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(bitw, cv2.MORPH_OPEN, kernel)

    # removing parasites
    mask_f = ndimage.median_filter(opening, size=5)

    return mask_f

def bounding_box(mask):
    # try:
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        obj_area = cv2.contourArea(sorted_contours[0])

        if obj_area > 100:
            flag = 1
            while flag == 1:
                # M = cv2.moments(sorted_contours[0])
                # #finding biggest area's center
                # gX = int(M["m10"] / M["m00"])
                # gY = int(M["m01"] / M["m00"])
                try:
                    # finding minimum enclosing circle and bounding box
                    x, y, w, h = cv2.boundingRect(sorted_contours[0])
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 2)
                    obj_area = cv2.contourArea(sorted_contours[0])

                    radius = w / 2
                    if radius < h / 2:
                        radius = h / 2

                    circle_area = 3.14 * (radius ** 2)
                    sf = obj_area / circle_area

                    print("possible object found")
                    print("object area= {}".format(obj_area))
                    print("radius= {}".format(radius))
                    print("circle area = {}".format(circle_area))
                    print("sf value = {}".format(sf))

                    gX = int(x + (w / 2))
                    gY = int(y + (h / 2))


                    isCircleEnough = sf > 0.4 and sf < 1.5

                    if isCircleEnough == True:
                        print("object found")
                        return [x, y, w, h, int(radius * 2), gX, gY, sorted_contours]

                    else:
                        print("popped")
                        sorted_contours.pop(0)
                except:
                    return None

    else:
        print("none")
        return None

font = cv2.FONT_HERSHEY_SIMPLEX

image = cv2.imread("result1.png")
width = image.shape[1]
height = image.shape[0]
mask_red = masking(image, lower_red, upper_red)
red_ball = bounding_box(mask_red)


mask_green = masking(image, lower_green, upper_green)
green_ball = bounding_box(mask_green)


try:
    cv2.drawContours(image, red_ball[7], -1, (0, 0, 255), 2)
    cv2.circle(image, (red_ball[5], red_ball[6]), int(red_ball[4] / 2), (0, 0, 0), 2)
    print("the image is {} pixels on x plane and the object lies between {}-{}. pixels ".format(width,red_ball[1],red_ball[3]))

except:
    pass

# new_image_time = time.time()
# fps = 1 / (new_image_time - prev_image_time)
# prev_image_time = new_image_time
# fps = int(fps)
# fps = str(fps)
# cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
cv2.imshow("Image", image)

cv2.waitKey(0)

cv2.destroyAllWindows()






"""# resizing image for faster runtime
scale_percent = 20
dim = (int(width * scale_percent / 100), int(height * scale_percent / 100))
img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
"""
# prev_image_time = 0
# # used to record the time at which we processed current image
# new_image_time = 0
# a = 0






"""
while True:
    ret,image = cap.read()
    if not ret:
        break
    width = image.shape[1]
    height = image.shape[0]

    mask_red = masking(image, lower_red, upper_red)
    red_ball = bounding_box(mask_red)


    mask_green = masking(image, lower_green, upper_green)
    green_ball = bounding_box(mask_green)


    try:
        cv2.drawContours(image, red_ball[7], -1, (0, 0, 255), 2)
        cv2.circle(image, (red_ball[5], red_ball[6]), int(red_ball[4] / 2), (0, 0, 0), 2)
        print("the image is {} pixels on x plane and the object lies between {}-{}. pixels ".format(width,red_ball[1],red_ball[3]))

    except:
        pass

    new_image_time = time.time()
    fps = 1 / (new_image_time - prev_image_time)
    prev_image_time = new_image_time
    fps = int(fps)
    fps = str(fps)
    cv2.putText(image, "fps: " + fps, (width - 100, 25), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Image", image)

    cv2.waitKey(0)

cv2.destroyAllWindows()

"""