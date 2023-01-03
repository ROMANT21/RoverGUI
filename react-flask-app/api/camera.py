import time
import cv2
import zmq


class Camera(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
    
    def get_frame(self):
        captured, frame = self.cam.read()
        return cv2.imencode('.jpg', frame)[1].tobytes()

class RemoteStream(object):
    def __init__(self, ip, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.socket.setsockopt(zmq.SNDHWM, 5)
        self.socket.setsockopt(zmq.RCVHWM, 5)
        self.socket.connect('tcp://{}:{}'.format(ip, port))
    
    def get_frame(self):
        try:
            md = self.socket.recv_json(zmq.NOBLOCK)
            frame = self.socket.recv(zmq.NOBLOCK)
            return frame
        except zmq.Again:
            return None