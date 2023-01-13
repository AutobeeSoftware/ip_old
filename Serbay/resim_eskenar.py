import cv2
import numpy as np
from sklearn.cluster import KMeans
import math


image = cv2.imread("dik.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
corners = cv2.cornerHarris(gray, 2, 3, 0.04)
coords = np.argwhere(corners > 0.01*corners.max())

km = KMeans(
    n_clusters=3, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(coords)
merkezler = km.cluster_centers_

print(merkezler)
a = int(math.sqrt((merkezler[0][0] - merkezler[1][0])**2 + (merkezler[0][1]-merkezler[1][1])**2))
b = int(math.sqrt((merkezler[0][0] - merkezler[2][0])**2 + (merkezler[0][1]-merkezler[2][1])**2))
c = int(math.sqrt((merkezler[1][0] - merkezler[2][0])**2 + (merkezler[1][1]-merkezler[2][1])**2))

if a == b == c:
    print("EŞKENAR ÜÇGEN")
else:
    print("EŞKENAR ÜÇGEN DEĞİL")