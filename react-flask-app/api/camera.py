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
    def __init__(self, context, ip, port):
        self.context = context
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
        except UnicodeDecodeError:
            return None

class StreamControl:
    def __init__(self, context, ip, port):
        self.context = context
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(ip, port+1))
    
    def send_command(self, command):
        self.socket.send_json(command)
        return self.socket.recv_string()