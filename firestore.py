import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./mrpool-firebase-adminsdk-svtnn-1b17d72bcc.json")
firebase_admin.initialize_app(cred)

db = firestore.client()