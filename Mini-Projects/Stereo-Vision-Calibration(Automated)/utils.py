import cv2 as cv
from settings import CameraSettings

class CameraObject:
    
    def __init__(self, camera_id:int, camera_name:str, camera_settings:CameraSettings):
        self.camera = None
        self.camera_name = camera_name
        self.camera_id = camera_id
        self.camera_settings = camera_settings
    
    def init_camera(self):
        try:
            self.camera = cv.VideoCapture(self.camera_id)            
            if self.camera.isOpened():
                self.update_camera_frame_size()
                return True
            else:
                return False
        except Exception as e:
            print("Error raised: ", e)
    
    def update_camera_frame_size(self):
        width, height = self.camera_settings.get_frame_size()
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    
    def get_camera_settings(self):
        for setting in self.camera_settings:
            print(setting)
    
    def __kill__(self):
        # Release and destroy all windows before termination
        self.camera.release()
    
