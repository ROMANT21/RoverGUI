from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS                             # This (on line 8) gets rid of the CORS error 
from api.HelloApiHandler import HelloApiHandler

# Create Flask web application and ready API
app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)
api = Api(app)


# Display index.html on homepage
@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')

api.add_resource(HelloApiHandler, '/flask/hello')