import cv2
import numpy as np
import face_recognition
import os


def check_face(encode, img2_path):
    encodeList = []
    encodeList.append(encode)

    cap_path = img2_path
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
                return {"face_found": True, "verified": True}
        return {"face_found": True, "verified": False}


def encoder(img_path):
    img = cv2.imread(img_path)
    img_feature = face_recognition.face_encodings(
        img, known_face_locations=None, num_jitters=1, model='small')
    return img_feature
