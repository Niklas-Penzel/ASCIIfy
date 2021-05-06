# render_template: Specify the template to refer to
#jsonify: json output
from flask import Flask, render_template, jsonify, request, make_response, send_file, Response
import werkzeug
from werkzeug.utils import secure_filename
#CORS: Library for Ajax communication
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
from random import *
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64
import os
from datetime import datetime
import numpy as np
from ASCIIfy import ASCIIfy



app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

ALLOWED_EXTENSIONS = set(["jpg", "png", "jpeg", "tiff", "bmp", "gif", "ppm", "pgm", "tif", "svg"])

def allowed_file(filename):
    """
    Check if this file format is allowed.
    filename -- the filename to be checked if correct
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Home(Resource):
    """
    The REST-Api response for the main directory.
    This will just return the name of the api.
    """

    def post(self):
        """
        Return the Post-Response upon request.
        This will just return the name 'asciify'
        """
        return {'name': 'asciify'}


class Fonts(Resource):
    """
    returns a list of fonts
    """

    def post(self):
        """
        Return the list of available fonts.
        """
        return {'fonts': [f.split(".ttf")[0] for f in sorted(os.listdir("fonts")) if f.endswith(".ttf")]}


class ASCIIfy_Image(Resource):
    """
    This class will handle the request on sending an image to the server.
    """
    def post(self):
        parser = reqparse.RequestParser()

        # we expect an image to be send, if not send message to the client
        #parser.add_argument('image', required=True, type=werkzeug.datastructures.FileStorage, location='form')
        parser.add_argument('debug', required=False, type=int)
        parser.add_argument("fontsize", required=True, type=int)
        parser.add_argument("font", required=True, type=str)
        parser.add_argument("resize", required=True, type=int)
        args = parser.parse_args()
        print(args)

        if args['debug'] is not None and args['debug'] == 1:
            print(args)
            return {"msg" : "nan"}  

        base64_ =  request.form['image']
        #print(base64_)
        code = base64.b64decode(base64_.split(',')[1])
        #print(code)
        image = Image.open(BytesIO(code))
        #print(type(image))
        
        # save the uploaded image ^^
        now = datetime.now().strftime("%H-%M-%S__%d-%m-%Y")
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], f"upload_{now}.jpg"))

        # asciify it:
        asciified = ASCIIfy(np.array(image), args["resize"],
                            os.path.join("fonts",f"{args['font']}.ttf"),
                            args["fontsize"], 1)

        asciified.seek(0)

        buffered = BytesIO()
        asciified.save(buffered, format="JPEG")
        asciified_str = base64.b64encode(buffered.getvalue())
        print(asciified_str[0:100])

        headers = {
            'Content-Type': "image/jpeg",    # This is important
        }
        return Response(response=asciified_str, status=200, headers=headers, mimetype="image/jpeg")

api.add_resource(Home, '/api/Home')
api.add_resource(Fonts, '/api/Fonts')
api.add_resource(ASCIIfy_Image, '/api/Asciify')

# app.run(host, port): Start flask server by specifying host and port
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)