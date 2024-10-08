import firebase_admin
from firebase_admin import credentials, firestore

# Đường dẫn đến tệp JSON chứa thông tin xác thực Firebase
cred = credentials.Certificate("C:/Users/ADMIN/pythondjango-c501a-firebase-adminsdk-jx6cs-ee00f6fdc7.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
