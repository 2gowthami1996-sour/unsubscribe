from flask import Flask
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("MONGO_DB_NAME")

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collections = db.list_collection_names()
except Exception as e:
    collections = str(e)

@app.route("/test")
def test():
    return f"Collections: {collections}"
