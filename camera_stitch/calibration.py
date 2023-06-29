import numpy as np
import cv2 as cv
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
pointsX = 5
pointsY = 5
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((pointsX*pointsY,3), np.float32)
objp[:,:2] = np.mgrid[0:pointsY,0:pointsX].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


img = cv.imread('/Users/emirysaglam/GitHub/IP_general/camera_stitch/calib.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('img', img)

# Find the chess board corners
ret, corners = cv.findChessboardCorners(gray, (pointsX,pointsY), None)
# If found, add object points, image points (after refining them)
print(ret)
if ret == True:
    objpoints.append(objp)
    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    imgpoints.append(corners2)
    print("objpoints :")
    print(len(objpoints[0]))
    print("imgpoints :")
    print(len(imgpoints[0]))
    # Draw and display the corners
    cv.drawChessboardCorners(img, (pointsX,pointsY), corners2, ret)
    cv.imshow('img', img)
    print("**************")

cv.waitKey(0)

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
print("camera matrix :" )
print(mtx)
print("distortion coefficients :")
print(dist)
print("rotation :")
print(rvecs)
print("translation :")
print(tvecs)


h, w = img.shape[:2]

newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
cv.imwrite('calibresult2.png', dst)

mean_error = 0
for i in range(len(objpoints)):
 imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
 error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
 mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )





cv.destroyAllWindows()
