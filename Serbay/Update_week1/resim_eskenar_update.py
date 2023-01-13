import cv2
import numpy as np
from sklearn.cluster import KMeans
import math


image = cv2.imread("/Users/emirysaglam/Documents/GitHub/IP_general/Serbay/Update_week1/hexa.jpeg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
corners = cv2.cornerHarris(gray, 2, 5, 0.04)
coords = np.argwhere(corners > 0.01*corners.max())

print(coords)

km = KMeans(
    n_clusters=6, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(coords)
merkezler = km.cluster_centers_
merkezler = merkezler.astype(int).tolist()

for i in range(6):
    cv2.circle(image, (merkezler[i][1],merkezler[i][0]), 3, (255,0,0), 4)

print(merkezler)

cv2.imshow("z",image)
cv2.waitKey(0)      
