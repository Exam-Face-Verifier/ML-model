from flask import Flask, request, Response
import json
import base64
from model import *

app = Flask(__name__)


@app.route("/verify", methods=['POST'])
def verify():
    try:
        body = request.data
        data = json.loads(body)

        unknown = data["unknown_img"]
        u_i = base64.decodebytes(unknown.encode('utf-8'))
        vfile = open("ver_img.png", "wb")
        vfile.write(u_i)
        vfile.close()

        known = data["known_img"]
        k_i = base64.decodebytes(known.encode('utf-8'))
        kvfile = open("kver_img.png", "wb")
        kvfile.write(k_i)
        kvfile.close()
        result = []

        result = check_face("kver_img.png", "ver_img.png")

        if result["verified"]:
            return Response('{"matched":True}', status=200, mimetype='application/json')
        else:
            return Response('{"matched":False}', status=200, mimetype='application/json')
    except Exception as e:
        return Response('{"matched":null}', status=500, mimetype='application/json')
