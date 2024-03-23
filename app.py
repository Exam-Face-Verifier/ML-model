from flask import Flask, request, Response, jsonify
import json
import base64
import os
from model import *
from qr_generator import get_qr
from listener import *
import pandas as pd

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
        known_path = "util/" + roll_no + ".json"
        f = open(known_path)
        known = json.load(f)

        result = check_face(known, "temp/ver_img.jpg")
        f.close()
        
        if not result["face_found"]:
            Res_dict = {'rollno': roll_no, 'matched': None,
                        'message': "Face not Found. Please retry!" }
            Res_JSON = jsonify(Res_dict)
            return Res_JSON, 201
        if result["verified"]:
            Res_dict = {'rollno': roll_no, 'matched': True,
                        'message': "Face matched"}
            Res_JSON = jsonify(Res_dict)
            return Res_JSON, 200
        else:
            Res_dict = {'rollno': roll_no, 'matched': False,
                        'message': "Face not matched"}
            Res_JSON = jsonify(Res_dict)
            return Res_JSON, 200
    except Exception as e:
        return Response('{"matched":null, "message":"Please retry!"}', status=500, mimetype='application/json')
    
    
@app.route("/uploadList", methods=['POST'])
def uploadList():
    try:
        body = request.data
        data = json.loads(body)
        print("Request Recieved")
        
        roll_list = data["roll_list"]
        failed_list = get_imgs(roll_array=roll_list)
        
        if len(failed_list) == 0:
            return Response('{"message":"Success"}', status=200, mimetype='application/json')
        
        else:
            failed_dict = {'failed_rollNo' : failed_list, 'message' : "Failure"}
            Res_JSON = jsonify(failed_dict)
            return Res_JSON, 201
        
    except:
        return Response('{"matched":null, "message":"Internal error.Please retry!"}', status=500, mimetype='application/json')


@app.route("/DeleteImages", methods=['GET'])
def delete_imgs():
    try:
        if os.path.exists('util'):
            os.rmdir('util')
        return Response('{"message":"Images deleted successful"}', status=200, mimetype='application/json')
    except:
        return Response('{"message":"Delete Failed"}', status=500, mimetype='application/json')
    

@app.route("/EncodeImage", methods=['POST'])
def encode_imgs():
    try:
        body = request.data
        data = json.loads(body)

        unknown = data["img"]
        u_i = base64.decodebytes(unknown.encode('utf-8'))
        vfile = open("temp/enc_img.jpg", "wb")
        vfile.write(u_i)
        vfile.close()
        res = encoder("temp/enc_img.jpg")
        
        if(len(res) == 0):
            return Response('{"message":"Face not Found"}', status=201, mimetype='application/json')
        
        else:
            Res_JSON = pd.Series(res).to_json(orient='values')
            return Res_JSON, 200
        
    except Exception as e:
        print(e)
        return Response('{"message":"Encoding Failed"}', status=500, mimetype='application/json')
