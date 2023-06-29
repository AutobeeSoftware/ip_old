import cv2
import numpy as np

# Ekranın genişliği ve yüksekliği
screen_width = 640
screen_height = 480

# Parçaların sayısı
num_parts = 270

# Her bir parçanın yüksekliği
part_height = screen_height // num_parts



# Parçaları çizin
for i in range(num_parts):
    y_start = i * part_height
    y_end = (i + 1) * part_height
    screen[y_start:y_end, :] = (255, 255, 255)  # Beyaz parçalar oluşturmak için (255, 255, 255) kullanılıyor

# Ekranı gösterin
cv2.imshow('Screen', screen)
cv2.waitKey(0)
cv2.destroyAllWindows()
