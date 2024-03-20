from flask import Flask, request, Response, jsonify
import json
import base64
import os
from model import *
from qr_generator import get_qr
from listener import *

app = Flask(__name__)

if not os.path.exists('temp'):
    os.mkdir('temp')

get_qr()


@app.route("/verify", methods=['POST'])
def verify():
    try:
        body = request.data
        data = json.loads(body)

        unknown = data["unknown_img"]
        u_i = base64.decodebytes(unknown.encode('utf-8'))
        vfile = open("temp/ver_img.jpg", "wb")
        vfile.write(u_i)
        vfile.close()
        
        roll_no = data["roll_no"]
        known_path = "util/" + roll_no + ".jpg"

        result = check_face(known_path, "temp/ver_img.jpg")
        
        if not result["face_found"]:
            Res_dict = {'rollno': roll_no, 'matched': None,
                        'message': "Face not Found. Please retry!" }
            Res_JSON = jsonify(Res_dict)
            return Response(Res_JSON, status=201, mimetype='application/json')
        if result["verified"]:
            Res_dict = {'rollno': roll_no, 'matched': True,
                        'message': "Face matched"}
            Res_JSON = jsonify(Res_dict)
            return Response(Res_JSON, status=200, mimetype='application/json')
        else:
            Res_dict = {'rollno': roll_no, 'matched': False,
                        'message': "Face not matched"}
            Res_JSON = jsonify(Res_dict)
            return Response(Res_JSON, status=200, mimetype='application/json')
    except Exception as e:
        return Response('{"matched":null, "message":"Please retry!"}', status=500, mimetype='application/json')
    
    
@app.route("/uploadList", methods=['POST'])
def uploadList():
    try:
        body = request.data
        data = json.loads(body)
        
        roll_list = data["roll_list"]
        failed_list = get_imgs(roll_array=roll_list)
        
        if len(failed_list) == 0:
            return Response('{"message":"Success"}', status=200, mimetype='application/json')
        
        else:
            failed_dict = {'failed_rollNo' : failed_list, 'message' : "Failure"}
            Res_JSON = jsonify(failed_dict)
            return Response(Res_JSON, status=201, mimetype='application/json')
        
    except:
        return Response('{"matched":null, "message":"Internal error.Please retry!"}', status=500, mimetype='application/json')
