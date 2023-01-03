from time import time
import cv2

class Camera(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
    
    def get_frame(self):
        captured, frame = self.cam.read()
        return cv2.imencode('.jpg', frame)[1].tobytes()