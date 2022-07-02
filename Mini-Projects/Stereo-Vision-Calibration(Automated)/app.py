"""
Automated Stereo Camera Calibration
"""

import cv2 as cv
from utils import CameraObject
from settings import CameraSettings

class MainApp:
    def __init__(self, *args, **kwargs):
        self.camera_right = None
        self.camera_left = None
    
    def add_camera_right(self, camera:CameraObject):
        self.camera_right = camera
    
    def close_app(self):
        cv.destroyAllWindows()


if __name__ == "__main__":
    app = MainApp()
    camera_right_settings = CameraSettings()
    camera_right_settings.camera_frame_size = (120, 60)
    camera_right = CameraObject(camera_id=0, camera_name="CAM Right", camera_settings=camera_right_settings)
    app.add_camera_right(camera_right)
    while True:
        print("App running!")
        if cv.waitKey(100) & 0xFF == ord("q"):
            break
    
    app.close_app()