import os
from urllib.parse import unquote
from pymongo import MongoClient
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load MongoDB info from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db.cleaned_contacts

@app.route("/", methods=["GET"])
def unsubscribe():
    email = request.args.get("email")
    if not email:
        return "❌ No email provided.", 400

    email = unquote(email)

    result = collection.update_one(
        {"work_emails": {"$regex": email, "$options": "i"}},
        {"$set": {"subscribed": False}}
    )

    if result.matched_count > 0:
        return f"✅ {email} has been unsubscribed successfully!"
    else:
        return f"⚠ No matching email found for {email}.", 404

# Required for Vercel serverless
def handler(request, response):
    return app(request, response)
