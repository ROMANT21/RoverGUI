"""
A Video Streamer class which starts a seperate thread for each camera, specified at source
"""
from threading import Thread
import cv2, time
 
class VideoStreamWidget(object):
    def __init__(self, src=0):
        # Open and configure camera
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.fps = 1/30     # Set FPS of camera stream (default 30 fps)
        self.fps_ms = int(self.fps * 1000)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                self.status, self.frame = self.capture.read()
            time.sleep(self.fps)
    
    # Set FPS of camera stream
    def set_fps(self, fps):
        self.fps = fps
        self.fps_ms = int(self.fps * 1000)

    def read_frame(self):
        # Display frames in main program
        return self.frame