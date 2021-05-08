import cv2
import numpy as np
import werkzeug
from flask import Flask, request, Response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_talisman import Talisman
from PIL import Image
from pathlib import Path
from io import BytesIO
import base64
import tensorflow as tf

import asciify
import artify

app = Flask(__name__)
app.config.from_object("config.DevConfig")
CORS(app)
Talisman(app)
api = Api(app)

model_selection = dict(
    [
        (artist, artify.load_artist_graph(artist, Path(app.config["MODEL_FOLDER"])))
        for artist in app.config["ARTISTS"]
    ]
)


def allowed_file(filename):
    """
    Check if this file format is allowed.
    filename -- the filename to be checked if correct
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def pil_to_base64_str(img):
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return data64


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
        return {"name": "asciify"}


class Fonts(Resource):
    """
    returns a list of fonts
    """

    def get(self):
        """
        Return the list of available fonts.
        """
        font_folder = Path(app.config["FONT_FOLDER"])
        return {
            "fonts": [
                str(f.stem).split(".ttf")[0]
                for f in sorted(font_folder.iterdir())
                if str(f).endswith(".ttf")
            ]
        }


class ASCIIfyImage(Resource):
    """
    This class will handle the request on sending an image to the server.
    """

    def post(self):
        parser = reqparse.RequestParser()

        # we expect an image to be send, if not send message to the client
        parser.add_argument(
            "image", type=werkzeug.datastructures.FileStorage, location="files"
        )
        parser.add_argument("debug", required=False, type=int)
        parser.add_argument("resize", required=False, type=int, default=-1)
        parser.add_argument("fontsize", required=True, type=int)
        parser.add_argument("font", required=True, type=str)
        args = parser.parse_args()

        if args["debug"] is not None and args["debug"] == 1:
            print(args)
            return {"msg": "Server site test."}

        file = request.files["image"]
        image = Image.open(file)

        # asciify it:
        asciified = asciify.ASCIIfy(
            np.array(image),
            args["resize"],
            str(Path(app.config["FONT_FOLDER"], f"{args['font']}.ttf")),
            args["fontsize"],
            1,
        )
        data64 = pil_to_base64_str(asciified)

        return Response(
            response=data64.decode("utf-8"), status=200, mimetype="image/jpeg"
        )


class Styles(Resource):
    """
    returns a list of fonts
    """

    def get(self):
        """
        Return the list of available fonts.
        """
        return {"styles": [artist.title() for artist in app.config["ARTISTS"]]}


class ArtifyImage(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        # we expect an image to be send, if not send message to the client
        parser.add_argument(
            "image", type=werkzeug.datastructures.FileStorage, location="files"
        )
        parser.add_argument(
            "style", required=True, type=str, choices=app.config["ARTISTS"]
        )
        args = parser.parse_args()

        file = request.files["image"]
        image = Image.open(file)
        artified = artify.artify(image, model_selection[args["style"]])
        data64 = pil_to_base64_str(artified)

        return Response(
            response=data64.decode("utf-8"), status=200, mimetype="image/jpeg"
        )


class BeautifyImage(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        # we expect an image to be send, if not send message to the client
        parser.add_argument(
            "image", type=werkzeug.datastructures.FileStorage, location="files"
        )
        parser.add_argument("debug", required=False, type=int)
        parser.add_argument("resize", required=False, type=int, default=-1)
        parser.add_argument("fontsize", required=True, type=int)
        parser.add_argument("font", required=False, type=str)
        parser.add_argument(
            "style", required=False, type=str, choices=app.config["ARTISTS"]
        )
        args = parser.parse_args()

        file = request.files["image"]
        image = Image.open(file)

        if args["style"] is not None:
            image = artify.artify(image, model_selection[args["style"]])

        if args["font"] is not None:
            image = asciify.ASCIIfy(
                np.array(image),
                args["resize"],
                str(Path(app.config["FONT_FOLDER"], f"{args['font']}.ttf")),
                args["fontsize"],
                1,
            )

        data64 = pil_to_base64_str(image)

        return Response(
            response=data64.decode("utf-8"), status=200, mimetype="image/jpeg"
        )


api.add_resource(Home, "/api/home")
api.add_resource(Fonts, "/api/fonts")
api.add_resource(ASCIIfyImage, "/api/asciify")
api.add_resource(Styles, "/api/styles")
api.add_resource(ArtifyImage, "/api/artify")
api.add_resource(BeautifyImage, "/api/beautify")

# app.run(host, port): Start flask server by specifying host and port
if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], host="127.0.0.1", port=5000)
