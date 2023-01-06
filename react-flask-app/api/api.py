from flask import Flask, render_template, Response, request
from camera import Camera, RemoteStream, StreamControl, FrameProvider
from configparser import ConfigParser
import base64
import zmq
import json

config = ConfigParser()
config.read('../config.ini')
ip = config['DEFAULT']['STREAM_IP']
port = int(config['DEFAULT']['STREAM_PORT'])

context = zmq.Context()
rs = RemoteStream(context, ip, port)
sc = StreamControl(context, ip, port+1)
fp = FrameProvider(rs)

app = Flask(__name__)

@app.route('/video_feed', methods=['GET'], strict_slashes=False)
def video_feed():
    stream_info = fp.get_info()
    return Response(stream_info, mimetype='application/json')

@app.route('/video_feed/<int:stream_id>', methods=['GET'], strict_slashes=False)
def video_feed_stream(stream_id):
    if stream_id < 0 or stream_id >= fp.num_streams:
        return Response('Invalid stream id', status=400)
    return Response(fp.get_frame(stream_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream_control', methods=['POST'], strict_slashes=False)
def video_control():
    command = request.json
    print(command)
    try:
        response = sc.send_command(command)
        print(response)
    except zmq.ZMQError as e:
        print(e)
    return {"response": 'OK'} 

def gen(camera, id):
    while True:
        frames = camera.get_frames()
        if frames is not None:
            frame = frames[id]
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)