"""
A Video Streamer class which starts a seperate thread for each camera, specified at source
"""
from threading import Thread
import cv2, time
 
class VideoStreamWidget(object):
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                self.status, self.frame = self.capture.read()
            time.sleep(.01)
    
    def read_frame(self):
        # Display frames in main program
        return self.frame