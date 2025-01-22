import cv2
import numpy as np
import face_recognition
import os


def check_face(vec, img2_path):
    encodeList = []
    encodeList.append(vec)
    # print(vec)
    print(type(vec))
    
    try:
        cap_path = img2_path
        while True:
            img = cv2.imread(cap_path)
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
            print(type(encodesCurFrame))

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeList, encodeFace)
                faceDis = face_recognition.face_distance(encodeList, encodeFace)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    return {"face_found": True, "verified": True}
            return {"face_found": True, "verified": False}
    except Exception as e:
        print(e)
        


def encoder(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_feature = face_recognition.face_encodings(img)[0]
    return img_feature
