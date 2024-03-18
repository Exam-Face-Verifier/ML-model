from deepface import DeepFace


def check_face(img1_path,img2_path):
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
    
