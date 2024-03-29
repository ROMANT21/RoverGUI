"""
A Video (or general) receiver made as a ZMQ Subscriber socket
"""
import zmq
import cv2
import numpy as np

# Create a socket to receive frames through
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.setsockopt(zmq.SUBSCRIBE, b'')
sub_socket.connect("tcp://127.0.0.1:5555")
sub_socket.subscribe(b'')

# Continously receive frames
while True:

    # Receive, decode, and display image
    md = sub_socket.recv_json()
    jpq_buffer = sub_socket.recv()
    img_arr = np.frombuffer(jpq_buffer, dtype=np.uint8)
    image = cv2.imdecode(img_arr, 1)

    # Display image
    cv2.imshow(f"video receiver {md['idx']}",image)
    cv2.waitKey(1)