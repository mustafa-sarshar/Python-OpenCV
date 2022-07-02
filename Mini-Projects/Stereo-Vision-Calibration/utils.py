import cv2 as cv

def set_camera_frame_size(camera, frame_size):
    camera.set(cv.CAP_PROP_FRAME_WIDTH, frame_size[0])
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, frame_size[1])
