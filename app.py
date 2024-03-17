from flask import Flask, request
import json
import base64
from model import *

app = Flask(__name__)


@app.route("/verify", methods=['POST'])
def verify():
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
    print(result)
    if result["verified"]:
        return "True"
    else:
        return "False"