from deepface import DeepFace
import cv2
import numpy as np
import face_recognition
import os

def fce(img1_path,img2_path):
    print('-----model running -----')
    try:
        result = DeepFace.verify(img1_path, img2_path)
        print(result)
        result["face_found"] = True
        return result
    except Exception as e:
        print(e)
        result = {"face_found":False}
        return result
    

def check_face(img1_path, img2_path):
    encodeList = []
    curimg = cv2.imread(img2_path)
    img = cv2.cvtColor(curimg, cv2.COLOR_BGR2RGB)
    try:
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    except:
        return {"face_found": False}
    
    cap_path = img1_path
    while True:
        img = cv2.imread(cap_path)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeList, encodeFace)
            faceDis = face_recognition.face_distance(encodeList, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                return {"face_found": True, "verified":True}
        return {"face_found": True, "verified":False}

