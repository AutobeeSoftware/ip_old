#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 19:30:49 2022

@author: emirysaglam
"""

import cv2
import numpy as np
import math


def empty(img):
    pass


def get_angle(p1, p2):
    a = math.atan2(p1[1] - p2[1], p1[0] - p2[0]) * 180 / math.pi
    return abs(a)


video = cv2.VideoCapture(1)  # kamerayı açar

cv2.namedWindow("TrackBar")  # istenilen rengin filtrelenmei için trackbar oluşturma
cv2.resizeWindow("TrackBar", 600, 300, )
cv2.createTrackbar("hue_min", "TrackBar", 0, 179, empty)
cv2.createTrackbar("hue_max", "TrackBar", 179, 179, empty)
cv2.createTrackbar("sat_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("val_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("val_max", "TrackBar", 255, 255, empty)

while True:  # sürekli kamerayı okutur

    ret, img = video.read()  # ret frame olup olmadığını söylüyor, img bir sonraki frame'i alıyor
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min, sat_min, val_min])  # beyaz olacak pixellerin değer olark alt ve üst sınırları belirler
    upper = np.array([hue_max, sat_max, val_max])

    mask = cv2.inRange(hsv, lower, upper)
    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # RETR_EXTERNAL en dıştaki şekli alır
    # CHAIN_APPROX_NONE
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 3000:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * peri, True)

            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

            (x1, y1), radius = cv2.minEnclosingCircle(c)
            center = (int(x1), int(y1))
            radius = int(radius)
            cv2.putText(img, "points: " + str(len(approx)), (x + w + 20, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
        if len(approx) == 4:
            if 80 < get_angle(approx[0][0], approx[1][0]) < 100 and 80 < get_angle(approx[2][0], approx[3][0]) < 100:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
                cv2.putText(img, "rectangle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            else:
                rec = np.int0(approx)
                cv2.drawContours(img, [rec], 0, (255, 0, 0), 2)
                cv2.putText(img, "quadrilateral", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
                            2)

        elif len(approx) == 3:
            tri = np.int0(approx)
            cv2.drawContours(img, [tri], 0, (255, 0, 0), 2)
            cv2.putText(img, "triangle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)
        else:
            cv2.circle(img, center, radius, (0, 0, 255), 2)
            cv2.putText(img, "circle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", img)  # img görüntüsünü gösteriyor
    cv2.imshow("hsv", hsv)  # hsv görüntüsünü gösteriyor
    cv2.imshow("Mask", mask)  # mask görüntüsünü gösteriyor

    k = cv2.waitKey(1)
    if k == ord('q'):  # ord function returns an integer representing the Unicode character
        break

video.release()
cv2.destroyAllWindows()
