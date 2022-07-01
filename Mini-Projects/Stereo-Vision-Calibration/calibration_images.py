"""
Main Source: https://www.youtube.com/watch?v=yKypaVl6qQo&list=RDCMUCpABUkWm8xMt5XmGcFb3EFg&index=5&ab_channel=NicolaiNielsen-ComputerVision%26AI
"""

import cv2 as cv

cap_0 = cv.VideoCapture(0)
cap_1 = cv.VideoCapture(1)

num = 0

while cap_0.isOpened() and cap_1.isOpened():

    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()

    key_pressed = cv.waitKey(5)

    if key_pressed == 27:
        break
    elif key_pressed == ord("s"): # wait for 's' key to save and exit
        if ret_0 and ret_1:
            cv.imwrite(f"images/stereo_0/image0_{num}.png", frame_0)
            cv.imwrite(f"images/stereo_1/image1_{num}.png", frame_1)
            print("images saved!")
            num += 1
    if ret_0 and ret_1:
        cv.imshow("Cap 0", frame_0)
        cv.imshow("Cap 1", frame_1)

# Release and destroy all windows before termination
cap_0.release()
cap_1.release()

cv.destroyAllWindows()
