"""
Automated Stereo Camera Calibration
"""

import cv2 as cv
import numpy as np
from utils import CameraObject
from settings import CameraSettings
from datetime import datetime
from settings import CAMERA_FRAME_SIZE, CHESSBOARD_SIZE, CHESSBOARD_SQUARES_SIZE, TERMINATION_CRITERIA

class MainApp:
    
    def __init__(self, *args, **kwargs):
        self.camera_right = None
        self.camera_left = None
        self.camera_right_frame = None
        self.camera_left_frame = None
        self.camera_right_frame_calb = None
        self.camera_left_frame_calb = None
        self.calibration_data = False
        self.calibration_data_auto_save = False
        self.calibration_data_ready = False
        self.camera_state = "Normal"

    def add_cameras(self, camera_right:CameraObject, camera_left:CameraObject):
        self.camera_right = camera_right
        success = self.camera_right.init_camera()
        if success:
            print(f"Right camera initialized successfully!, Frame size set to {self.camera_right.camera_settings.get_frame_size()}!")
        else:
            print("Right camera couldn't get initialized!")

        self.camera_left = camera_left
        success = self.camera_left.init_camera()
        if success:
            print(f"Left camera initialized successfully!, Frame size set to {self.camera_left.camera_settings.get_frame_size()}!")
        else:
            print("Left camera couldn't get initialized!")

    def run_cameras(self):
        if self.camera_right.camera.isOpened() and self.camera_left.camera.isOpened():
            ret_R, self.camera_right_frame = self.camera_right.camera.read()
            ret_L, self.camera_left_frame = self.camera_left.camera.read()            

            if ret_R and ret_L:
                self.update_camera_state()
                # Calibrate cameras
                if self.calibration_data:
                    success_right, self.camera_right_frame_calb = self.show_calibration_data(self.camera_right_frame.copy())
                    success_left, self.camera_left_frame_calb = self.show_calibration_data(self.camera_left_frame.copy())
                    
                    if success_left and success_right:
                        self.calibration_data_ready = True
                        if self.calibration_data_auto_save: self.save_calibration_data()
                    else:
                        self.calibration_data_ready = False
                    cv.imshow(self.camera_right.camera_name, self.camera_right_frame_calb)
                    cv.imshow(self.camera_left.camera_name, self.camera_left_frame_calb)
                else:                
                    cv.imshow(self.camera_right.camera_name, self.camera_right_frame)
                    cv.imshow(self.camera_left.camera_name, self.camera_left_frame)

    def show_calibration_data(self, frame):
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        success, corners = cv.findChessboardCorners(frame_gray, CHESSBOARD_SIZE, None)
        
        if success:
            # print("# of corners found:", len(corners))
            corners = cv.cornerSubPix(frame_gray, corners, (11, 11), (-1, -1), TERMINATION_CRITERIA)            
            frame = cv.drawChessboardCorners(frame, CHESSBOARD_SIZE, corners, success) # Draw and display the corners
        
        return success, frame

    def init_calibration_data(self, frame):
        # FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS
        obj_point = np.zeros((CHESSBOARD_SIZE[0]*CHESSBOARD_SIZE[1], 3), np.float32)
        obj_point[:, :2] = np.mgrid[0:CHESSBOARD_SIZE[0], 0:CHESSBOARD_SIZE[1]].T.reshape(-1, 2)
        obj_point = obj_point * CHESSBOARD_SQUARES_SIZE
        
        return frame
    
    def save_calibration_data(self):
        if self.calibration_data_ready:
            now = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"calbimage_{now}.png"            
            cv.imwrite(f"images/stereo_right/{filename}", self.camera_right_frame)
            cv.imwrite(f"images/stereo_left/{filename}", self.camera_left_frame)
            print(f"calibration images saved as {filename}!")
    
    def update_camera_state(self):
        if self.calibration_data:
            self.camera_state = "Show calibration data"
        elif self.calibration_data_ready & self.calibration_data_auto_save:
            self.camera_state = "Calibrating (Auto)"
        elif self.calibration_data_ready:
            self.camera_state = "Calibrating (Manual)"
        else:
            self.camera_state = "Normal"

    def close_app(self):
        self.camera_right.camera.release()
        self.camera_left.camera.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    app = MainApp()
    camera_right_settings = CameraSettings(frame_size=CAMERA_FRAME_SIZE, focal_length=10)
    camera_right = CameraObject(camera_id=0, camera_name="CAM Right", camera_settings=camera_right_settings)
    camera_left_settings = CameraSettings(frame_size=CAMERA_FRAME_SIZE, focal_length=10)
    camera_left = CameraObject(camera_id=1, camera_name="CAM Left", camera_settings=camera_left_settings)
    app.add_cameras(camera_right=camera_right, camera_left=camera_left)
    
    while True:
        app.run_cameras()    
        key_pressed = cv.waitKey(1)    
        if key_pressed == ord("q"):
            break
        elif key_pressed == ord("c"):
            app.calibration_data = not app.calibration_data
        elif key_pressed == ord("a"):
            app.calibration_data_auto_save = not app.calibration_data_auto_save
        elif key_pressed == ord("s"): # wait for 's' key to save and exit
            app.save_calibration_data()
    
    app.close_app()