import firebase_admin
from firebase_admin import credentials, firestore
import urllib.request
import os

cred = credentials.Certificate('serviceaccountkey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

student_details_ref = db.collection('Student_Details')

if not os.path.exists('util'):
    os.mkdir('util')
    
def get_imgs(roll_array):
    error_array = []
    for r in roll_array:
        try:
            student = student_details_ref.document(r).get()
            student_data = student.to_dict()
            rollNo = student_data["Student_Rollno"]
            url = student_data["Student_Image"]
            filename = rollNo + '.json'
            filepath = 'util/' + filename

            if not os.path.isfile(filepath):
                urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            error_array.append(r)        
    return error_array
    