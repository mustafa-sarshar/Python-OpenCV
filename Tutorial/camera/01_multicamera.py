"""
Source: https://www.youtube.com/watch?v=jGYNFssXiAQ&ab_channel=CodesofInterest
"""
import cv2 as cv

cam_0 = cv.VideoCapture(0)
cam_1 = cv.VideoCapture(1)

while True:
    # Capture frame-by-frame
    ret_0, frame_0 = cam_0.read()
    ret_1, frame_1 = cam_1.read()
    
    if (ret_0):
        cv.imshow("Cam 0", frame_0)
    
    if (ret_1):
        cv.imshow("Cam 1", frame_1)
    
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cam_0.release()
cam_1.release()
cv.destroyAllWindows()