import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from os import path, environ
from json import loads

# Either .json file or env json string
if path.exists("./Firebase-admin-creds.json"): cred = "./Firebase-admin-creds.json"
else: cred = loads(environ.get('firebase_cred') or '')

cred = credentials.Certificate(cred)
firebase_admin.initialize_app(cred)

db = firestore.client()
