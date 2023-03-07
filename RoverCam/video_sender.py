"""
A Video Sender made with Image ZMQ, specified as ZMQ Publisher
"""
import cv2
import zmq
import numpy as np
from VideoStreamer import VideoStreamWidget
import time

# Create ZMQ Context and Publisher Socket for sending frames
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5555")

# Set socket behavior
publisher.setsockopt(zmq.SNDHWM, 1)  # Set high water mark to 1 to drop frames if queue is full
publisher.setsockopt(zmq.SNDBUF, 1)  # Set send buffer to 1 to drop frames if queue is full

# Open camera instances for capturing streams
camera1 = VideoStreamWidget(0)  # For Windows: src=0,1,... For Linux: '/dev/video*'
camera2 = VideoStreamWidget(1)
time.sleep(1)                   # Let cameras bake

cameraList = [camera1 , camera2]

# Start sending images until CTRL+C
i = 0   # Index for numbering frames
while True:
    i = i + 1
    cameraIdx = 0   # For labeling Streams
    for camera in cameraList:
        
        # Read frame from camera
        try:
            frame = camera.read_frame()
        except AttributeError:
            pass

        # Add counter value to the image
        frame = cv2.resize(frame, (640, 480))
        cv2.putText(frame, str(i), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
        cv2.imshow(f"{cameraIdx} sender", frame)
        cv2.waitKey(1)

        # Encode Message
        quality = 95
        jpg_buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1].tobytes()
        
        md = dict(idx=cameraIdx, )
        publisher.send_json(md, zmq.SNDMORE)
        publisher.send(jpg_buffer)

        # Increment camera index
        cameraIdx = cameraIdx + 1
