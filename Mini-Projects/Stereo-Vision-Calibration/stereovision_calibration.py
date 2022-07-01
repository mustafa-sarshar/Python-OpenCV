"""
Main Source: https://www.youtube.com/watch?v=yKypaVl6qQo&list=RDCMUCpABUkWm8xMt5XmGcFb3EFg&index=5&ab_channel=NicolaiNielsen-ComputerVision%26AI
"""

import numpy as np
import cv2 as cv
import glob

################ FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS #############################

chessboard_size = (7, 7)
frame_size = (640, 480)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 22
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
obj_points = [] # 3d point in real world space
img_points_0 = [] # 2d points in image plane.
img_points_1 = [] # 2d points in image plane.

images_0 = sorted(glob.glob("images\stereo_0\*.png"))
images_1 = sorted(glob.glob("images\stereo_1\*.png"))
print(images_0)
print(images_1)

for img_0, img_1 in zip(images_0, images_1):

    img0 = cv.imread(img_0)
    img1 = cv.imread(img_1)
    gray_0 = cv.cvtColor(img0, cv.COLOR_BGR2GRAY)
    gray_1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret_0, corners_0 = cv.findChessboardCorners(gray_0, chessboard_size, None)
    ret_1, corners_1 = cv.findChessboardCorners(gray_1, chessboard_size, None)

    # If found, add object points, image points (after refining them)
    if ret_0 and ret_1 == True:
        print(ret_0)
        obj_points.append(objp)

        corners_0 = cv.cornerSubPix(gray_0, corners_0, (11, 11), (-1, -1), criteria)
        img_points_0.append(corners_0)

        corners_1 = cv.cornerSubPix(gray_1, corners_1, (11, 11), (-1, -1), criteria)
        img_points_1.append(corners_1)

        # Draw and display the corners
        cv.drawChessboardCorners(img0, chessboard_size, corners_0, ret_0)
        cv.imshow("Img 0", img0)
        cv.drawChessboardCorners(img1, chessboard_size, corners_1, ret_1)
        cv.imshow("Img 1", img1)
        cv.waitKey(1000)

cv.destroyAllWindows()

############## CALIBRATION #######################################################

ret_0, cam_mat_0, dist_0, rot_vec_0, trans_vec_0 = cv.calibrateCamera(obj_points, img_points_0, frame_size, None, None)
height_0, width_0, channels_0 = img0.shape
new_cam_mat_0, roi_0 = cv.getOptimalNewCameraMatrix(cam_mat_0, dist_0, (width_0, height_0), 1, (width_0, height_0))

ret_1, cam_mat_1, dist_1, rot_vec_1, trans_vec_1 = cv.calibrateCamera(obj_points, img_points_1, frame_size, None, None)
height_1, width_1, channels_1 = img1.shape
new_cam_mat_1, roi_1 = cv.getOptimalNewCameraMatrix(cam_mat_1, dist_1, (width_1, height_1), 1, (width_1, height_1))

########## Stereo Vision Calibration #############################################

flags = 0
flags |= cv.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 

criteria_stereo = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
ret_stereo, new_cam_mat_0, dist_0, new_cam_mat_1, dist_1, rot, trans, essential_matrix, fundamental_matrix = \
    cv.stereoCalibrate(
        obj_points,
        img_points_0, img_points_1,
        new_cam_mat_0, dist_0,
        new_cam_mat_1, dist_1,
        gray_0.shape[::-1], criteria_stereo, flags
    )

########## Stereo Rectification #################################################

rectify_scale = 1
rect_0, rect_1, proj_matrix_0, proj_matrix_1, Q, roi_0, roi_1 = cv.stereoRectify(
    new_cam_mat_0, dist_0, new_cam_mat_1, dist_1, gray_0.shape[::-1], rot, trans, rectify_scale, (0, 0)
)

stereo_map_0 = cv.initUndistortRectifyMap(new_cam_mat_0, dist_0, rect_0, proj_matrix_0, gray_0.shape[::-1], cv.CV_16SC2)
stereo_map_1 = cv.initUndistortRectifyMap(new_cam_mat_1, dist_1, rect_1, proj_matrix_1, gray_1.shape[::-1], cv.CV_16SC2)

print("Saving parameters!")
cv_file = cv.FileStorage("stereo_map.xml", cv.FILE_STORAGE_WRITE)

cv_file.write("stereoMap0_x", stereo_map_0[0])
cv_file.write("stereoMap0_y", stereo_map_0[1])
cv_file.write("stereoMap1_x", stereo_map_1[0])
cv_file.write("stereoMap1_y", stereo_map_1[1])

cv_file.release()
