"""
A Video Sender made with Image ZMQ, specified as ZMQ Publisher
"""
import cv2
import imagezmq
import numpy as np
from VideoStreamer import VideoStreamWidget
import time

# Create ZMQ Publisher Socket for sending videos 
sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)

# Open camera instances for capturing streams
camera1 = VideoStreamWidget(0)  # For Windows: src=0,1,... For Linux: '/dev/video*'
#camera2 = VideoStreamWidget(0)
time.sleep(1)                   # Let cameras bake

cameraList = [camera1] #, camera2]

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

        # Add counter value to the image and send it to the queue
        cv2.putText(frame, str(i), (100, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
        cv2.imshow(f"{cameraIdx} sender", frame)
        cv2.waitKey(1)

        # Encode and send image
        quality = 95
        jpg_buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1].tobytes()
        sender.send_jpg_pubsub(str(cameraIdx), jpg_buffer)
        cameraIdx = cameraIdx + 1
