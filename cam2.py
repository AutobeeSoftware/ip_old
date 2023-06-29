import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()

# İki kameradan alınan kareleri aynı boyuta getiriyoruz
min_height = min(frame1.shape[0], frame2.shape[0])
min_width = min(frame1.shape[1], frame2.shape[1])
frame1 = frame1[:min_height, :min_width]
frame2 = frame2[:min_height, :min_width]

# İki kareyi yatay olarak birleştiriyoruz
combined_frame = np.hstack((frame1, frame2))

# Çakışan bölgeyi kaldırma rastgele böyle yaptım daha sonra test edilip ayarlanıcak
overlap_width = min(frame1.shape[1], frame2.shape[1]) // 10  # Çakışan alanın genişliği
combined_frame[:, -overlap_width:] = 0

cv2.imshow('Combined', combined_frame)
cv2.waitKey(0)

cap1.release()
cap2.release()
cv2.destroyAllWindows()
