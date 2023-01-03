from flask import Flask, render_template, Response
from camera import Camera, RemoteStream

from flask import Flask

ip = 'localhost'
port = '5555'

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(gen(RemoteStream(ip, port)), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)