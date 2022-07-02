"""
Main Source: https://www.youtube.com/watch?v=yKypaVl6qQo&list=RDCMUCpABUkWm8xMt5XmGcFb3EFg&index=5&ab_channel=NicolaiNielsen-ComputerVision%26AI
"""

import cv2 as cv
import os
from utils import set_camera_frame_size
from settings import CAMERA_FRAME_SIZE

cap_0 = cv.VideoCapture(0)
cap_1 = cv.VideoCapture(1)

if cap_0.isOpened() and cap_1.isOpened():
    set_camera_frame_size(cap_0, frame_size=CAMERA_FRAME_SIZE)
    set_camera_frame_size(cap_1, frame_size=CAMERA_FRAME_SIZE)
else:
    os.exit(0)

img_index = 0
while cap_0.isOpened() and cap_1.isOpened():    
    
    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()

    key_pressed = cv.waitKey(5)

    # Hit "q" to close the window
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

    elif key_pressed == ord("s"): # wait for 's' key to save and exit
        if ret_0 and ret_1:
            cv.imwrite(f"images/stereo_0/image0_{img_index}.png", frame_0)
            cv.imwrite(f"images/stereo_1/image1_{img_index}.png", frame_1)
            print("images saved!")
            img_index += 1
    if ret_0 and ret_1:
        cv.imshow("Cap 0", frame_0)
        cv.imshow("Cap 1", frame_1)

# Release and destroy all windows before termination
cap_0.release()
cap_1.release()

cv.destroyAllWindows()
