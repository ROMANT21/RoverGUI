import time
import cv2
import zmq
import threading


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
    
    def get_frames(self):
        frames = []
        try:
            md = self.socket.recv_json(zmq.NOBLOCK)
            for _ in range(md['count']):
                frame = self.socket.recv(zmq.NOBLOCK)
                frames.append(frame)
            return frames
        except zmq.Again:
            return None
        except UnicodeDecodeError:
            return None

class StreamControl:
    def __init__(self, context, ip, port):
        self.context = context
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect('tcp://{}:{}'.format(ip, port))
    
    def send_command(self, command):
        self.socket.send_json(command)
        return self.socket.recv_string()

class FrameProvider(object):
    def __init__(self, stream):
        self.frames = []
        self.num_streams = 0
        self.stream = stream
        t = threading.Thread(target=self.query)
        t.daemon = True
        t.start()

    def query(self):
        while True:
            frames = self.stream.get_frames()
            if frames is not None:
                self.frames = frames
                self.num_streams = len(frames)
            time.sleep(0.001)

    def get_info(self):
        return {'num_streams': self.num_streams}

    def get_frame(self, ind):
        while True:
            if self.frames[ind] is not None:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + self.frames[ind] + b'\r\n')