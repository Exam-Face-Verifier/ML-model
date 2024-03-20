import firebase_admin
from firebase_admin import credentials, firestore
import requests
import os
from studentDetails import *
# Initialize Firebase
cred = credentials.Certificate('serviceaccountkey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
print('-----Connection initialized-----')

# Reference to the collection
student_details_ref = db.collection('Student_Details')

# Iterate over documents in the collection

for doc in student_details_ref.stream():
    student_data = doc.to_dict()
    image_data = student_data.get('Student_Image')
    rollNo = student_data.get('Student_Rollno')
    StudentDetails[rollNo] = image_data

print(StudentDetails);