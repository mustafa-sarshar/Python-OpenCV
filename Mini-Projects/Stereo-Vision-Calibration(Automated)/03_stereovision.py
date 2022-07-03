"""
Main Source: https://www.youtube.com/watch?v=yKypaVl6qQo&list=RDCMUCpABUkWm8xMt5XmGcFb3EFg&index=5&ab_channel=NicolaiNielsen-ComputerVision%26AI
"""

import cv2 as cv
from settings import CAMERA_FRAME_SIZE, CV2_BORDER_MODES, CV2_INTERPOLATION_METHODS

def set_camera_frame_size(camera, frame_size):
    camera.set(cv.CAP_PROP_FRAME_WIDTH, frame_size[0])
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, frame_size[1])


# Camera parameters to undistort and rectify images
cv_file = cv.FileStorage()
cv_file.open("stereo_map.xml", cv.FileStorage_READ)

stereo_map_0_x = cv_file.getNode("stereoMap0_x").mat()
stereo_map_0_y = cv_file.getNode("stereoMap0_y").mat()
stereo_map_1_x = cv_file.getNode("stereoMap1_x").mat()
stereo_map_1_y = cv_file.getNode("stereoMap1_y").mat()

maping_settings = dict(
    interpolation=CV2_INTERPOLATION_METHODS["lanczos4"],            # cv.INTER_LANCZOS4
    borderMode=CV2_BORDER_MODES["constant"],                       # cv.BORDER_CONSTANT
    borderValue=0,
)
# Open both cameras                    
cap_0 =  cv.VideoCapture(0, cv.CAP_DSHOW)
cap_1 = cv.VideoCapture(1, cv.CAP_DSHOW)

if cap_0.isOpened() and cap_1.isOpened():
    set_camera_frame_size(cap_0, frame_size=CAMERA_FRAME_SIZE)
    set_camera_frame_size(cap_1, frame_size=CAMERA_FRAME_SIZE)

while(cap_0.isOpened() and cap_1.isOpened()):

    ret_0, frame_0 = cap_0.read()
    ret_1, frame_1 = cap_1.read()

    if ret_0 and ret_1:
        # Undistort and rectify images
        frame_0_mapped = frame_0.copy()
        frame_1_mapped = frame_1.copy()
        cv.remap(
            src=frame_0, dst=frame_0_mapped, map1=stereo_map_0_x, map2=stereo_map_0_y,
            interpolation=maping_settings["interpolation"],
            borderMode=maping_settings["borderMode"],
            borderValue=maping_settings["borderValue"]
        )
        cv.remap(
            src=frame_1, dst=frame_1_mapped, map1=stereo_map_1_x, map2=stereo_map_1_y,
            interpolation=maping_settings["interpolation"],
            borderMode=maping_settings["borderMode"],
            borderValue=maping_settings["borderValue"]
        )
                        
        # Show original frames
        cv.imshow("Camera 0", frame_0)
        cv.imshow("Camera 1", frame_1)
        
        # Show mapped frames
        cv.imshow("Camera 0 - mapped", frame_0_mapped)
        cv.imshow("Camera 1 - mapped", frame_1_mapped)


    # Hit "q" to close the window
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release and destroy all windows before termination
cap_0.release()
cap_1.release()
cv.destroyAllWindows()
