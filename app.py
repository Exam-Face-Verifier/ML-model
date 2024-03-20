from flask import Flask, request, Response
import json
import base64
from model import *
from qr_generator import get_qr

app = Flask(__name__)
get_qr()


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
        
        if not result["face_found"]:
            return Response('{"matched":null, "message":"Face not Found. Please retry!"}', status=201, mimetype='application/json')
        if result["verified"]:
            return Response('{"matched":true, "message":"Face matched"}', status=200, mimetype='application/json')
        else:
            return Response('{"matched":false, "message":"Face not matched"}', status=200, mimetype='application/json')
    except Exception as e:
        return Response('{"matched":null, "message":"Please retry!"}', status=500, mimetype='application/json')
