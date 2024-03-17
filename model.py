from deepface import DeepFace


def check_face(img1_path,img2_path):
    print('-----model running -----')
    try:
        result = DeepFace.verify(img1_path, img2_path,enforce_detection=False)
        print(result)
        return result
    except Exception as e:
        print(e)
        return "Hello"
    
# check_face("images.jpg","q1.jpg")