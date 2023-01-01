import time
from argparse import ArgumentParser
from signal import SIGINT, signal
from sys import exit

import cv2
import numpy as np
import zmq


def cleanup():
    '''
    Clean up the context and socket
    '''
    context.destroy()


def handler(signal_received, frame):
    '''
    Handle any cleanup here
    '''
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

# bind the handler to SIGINT
signal(SIGINT, handler)

# construct the argument parser and parse the arguments
parser = ArgumentParser()
parser.add_argument('-i', type=str, default='localhost',
                    help='IP address of the server')
parser.add_argument('-o', type=int, default=5555, help='Port of the server')
args = parser.parse_args()
hostname = 'tcp://{}:{}'.format(args.i, args.o)

# create the zmq context and socket
# note, the zmq context only needs to be created once but it
# can create multiple sockets
context = zmq.Context()

# create a subscriber socket
socket = context.socket(zmq.SUB)

# set the subscription to receive all messages (the '' part)
socket.setsockopt_string(zmq.SUBSCRIBE, '')

# set the high water mark to 2
# what this means is that the socket will only buffer 2 messages at a time
# if the socket is full, it will drop any new messages
socket.setsockopt(zmq.SNDHWM, 3)
socket.setsockopt(zmq.RCVHWM, 3)

# connect the socket to the server
socket.connect(hostname)

# loop and receive the messages
while True:
    # measure time to receive the message
    start = time.perf_counter()
    images = []
    # receive the message
    try:
        md = socket.recv_json(zmq.NOBLOCK)
        for i in range(md['count']):
            msg = socket.recv(zmq.NOBLOCK)
            A = np.frombuffer(msg, dtype=np.uint8)
            image = cv2.imdecode(A, 1)
            images.append(image)
    except zmq.Again:
        # if the msg is empty, wait 10ms and try again
        time.sleep(0.05)
        continue
    except UnicodeDecodeError:
        # if the msg is empty, wait 10ms and try again
        time.sleep(0.05)
        continue
    end = time.perf_counter()

    print('Time to receive: {0:3.2f} ms'.format(
        (end - start) * 1000))

    # display the image
    for i, image in enumerate(images):
        if image is not None:
            cv2.imshow('Video Stream {}'.format(i), image)
    cv2.waitKey(1)