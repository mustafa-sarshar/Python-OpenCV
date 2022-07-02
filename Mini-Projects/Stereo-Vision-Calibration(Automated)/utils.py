import cv2 as cv
from settings import CameraSettings

class CameraObject:
    
    def __init__(self, camera_id:int, camera_name:str, camera_settings:CameraSettings):
        self.camera = None
        self.camera_name = camera_name
        self.camera_id = camera_id
        self.camera_settings = camera_settings
    
    def init_camera(self):
        self.camera = cv.VideoCapture(self.camera_id)
        if self.camera.isOpened():
            self.set_camera_frame_size(self.camera)
    
    def set_camera_frame_size(self):
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, self.camera_settings.camera_frame_size[0])
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, self.camera_settings.camera_frame_size[1])
    
    def get_camera_settings(self):
        for setting in self.camera_settings:
            print(setting)
    
    def __kill__(self):
        # Release and destroy all windows before termination
        self.camera.release()
    
