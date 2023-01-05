from flask import Flask, render_template, Response, request
from camera import Camera, RemoteStream, StreamControl
from configparser import ConfigParser

import zmq

config = ConfigParser()
config.read('../config.ini')
ip = config['DEFAULT']['STREAM_IP']
port = int(config['DEFAULT']['STREAM_PORT'])
context = zmq.Context()

sc = StreamControl(context, ip, port)
rs = RemoteStream(context, ip, port)

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(gen(rs), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream_control', methods=['POST'], strict_slashes=False)
def video_control():
    command = request.json['cmd']
    print(command)
    try:
        response = sc.send_command(command)
        print(response)
    except zmq.ZMQError as e:
        print(e)
    return {"response": 'OK'}


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)