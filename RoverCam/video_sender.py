import argparse
import socket
from signal import SIGINT, signal
from sys import exit
import time

import cv2
import numpy as np
import zmq

WIDTH = 1280
HEIGHT = 720


class VideoStream:
    '''
    Class to handle video streaming from a camera
    '''
    def __init__(self, src=0, name='VideoStream'):
        # initialize the video camera stream and set the
        # frame size and encoding
        self.src = src
        self._get_stream(src)

        # initialize the stream name
        self.name = name

        # initialize the capture stop event
        self.stopped = False

        self.error = False

    def _get_stream(self, src=0):
        # return the video camera stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.stream.set(cv2.CAP_PROP_FOURCC,
                        cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    def read(self):
        # return the frame most recently read
        grabbed, frame = self.stream.read()
        if grabbed:
            return frame

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def close(self):
        self.stream.release()


def encode_jpeg(image, quality):
    '''
    Encode an image as a jpeg
    
    Args:
        image: the image to encode
        quality: the quality of the image (0-100)
        
    Returns:
        the encoded image
    '''
    return cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])[1].tobytes()


def cleanup():
    cap.close()
    context.destroy()


def handler(signal_received, frame):
    cleanup()
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

# bind the handler to SIGINT
signal(SIGINT, handler)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, default="*",
                help="ip address of the device")
ap.add_argument("-o", "--port", type=int, default=5555,
                help="ephemeral port number of the server (1024 to 65535)")
args = vars(ap.parse_args())

pub_hostname = 'tcp://{}:{}'.format(args['ip'], args['port'])
cmd_hostname = 'tcp://{}:{}'.format(args['ip'], args['port']+1)

# create the zmq context and socket
# note, the zmq context only needs to be created once but it
# can create multiple sockets
context = zmq.Context()

# create a publisher socket
pub_socket = context.socket(zmq.PUB)

# set the high water mark to 2
# this means that if the subscriber is not receiving messages
# the publisher will drop all messages that are not the current frame
pub_socket.setsockopt(zmq.SNDHWM, 3)
pub_socket.setsockopt(zmq.RCVHWM, 3)

# set linger to 0
# this means that if the video stream is closed it won't try to deliver 
# any messages that are still in the queue
# socket.setsockopt(zmq.LINGER, 0)
# set immediate to 1
# this will only queue messages if the subscriber is ready to receive them
# socket.setsockopt(zmq.IMMEDIATE, 1)
pub_socket.bind(pub_hostname)

cmd_socket = context.socket(zmq.REP)
cmd_socket.bind(cmd_hostname)

cap = VideoStream(src=0)
other_cap = VideoStream(src=1)

captures = [cap, other_cap]

stopped = False

green = (0, 255, 0)

i = 0

while True:


    # check for a command
    try:
        cmd = cmd_socket.recv_json(zmq.NOBLOCK)
        print(f'Received command: {cmd}')
        if cmd == 'stop':
            stopped = True
            cmd_socket.send_string('stopped')
        elif cmd == 'start':
            stopped = False
            cmd_socket.send_string('started')
    except zmq.Again:
        pass
    except zmq.ZMQError as e:
        print(e)

    if stopped:
        continue

    i = i + 1
    print(f'Sending image {i}')
    msg = f'Image {i}'
    
    # open camera
    # print(captures[0].read())
    images = [cap.read() for cap in captures]

    if images[0] is None:
        print('No image')
        continue

    # add text to image
    for image in images:
        cv2.putText(image, f'Image {i}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, green, 2, cv2.LINE_AA)

    # create metadata
    md = dict(
        type='jpg',
        count=len(captures),
    )

    # send the metadata about the image first
    pub_socket.send_json(md, zmq.SNDMORE)

    # send the image
    # encode the image as a jpeg
    encoded = [encode_jpeg(image, 20) for image in images]
    for enc_image in encoded:
        pub_socket.send(enc_image, zmq.NOBLOCK)