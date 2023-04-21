import zmq
import cv2
import numpy as np
import threading

exit_event = threading.Event()

def video_player():
    global exit_event
    # Create a socket to receive frames through
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.setsockopt(zmq.SUBSCRIBE, b'')
    sub_socket.connect("tcp://127.0.0.1:5555")
    sub_socket.subscribe(b'')

    # Continously receive frames
    while not exit_event.is_set():

        # Receive, decode, and display image
        md = sub_socket.recv_json()
        jpq_buffer = sub_socket.recv()
        img_arr = np.frombuffer(jpq_buffer, dtype=np.uint8)
        image = cv2.imdecode(img_arr, 1)

        # Display image
        cv2.imshow(f"video receiver {md['idx']}",image)
        cv2.waitKey(1)

    sub_socket.close()
    context.term()
    cv2.destroyAllWindows()

def command_sender():
    global exit_event
    # Create a socket to send commands through
    context = zmq.Context()
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind("tcp://127.0.0.1:5556")

    while not exit_event.is_set():
        message = input("Enter a command(stop): ")
        push_socket.send_string(message)
        if message == "stop":
            print("Stopping video stream")
            exit_event.set()
            push_socket.close()
            context.term()

# Creates Threads to run the video player and command sender at the same time
videoThread = threading.Thread(target=video_player)
commandThread = threading.Thread(target=command_sender)

videoThread.start()
commandThread.start()

videoThread.join()
commandThread.join()
