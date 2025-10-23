import os
from urllib.parse import parse_qs
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

def handler(request):
    # Parse query parameters
    query = parse_qs(request.query_string.decode())
    email = query.get('email', [None])[0]

    if not email:
        return {
            "statusCode": 400,
            "body": "⚠ Missing email parameter!"
        }

    # Connect to MongoDB
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db.cleaned_contacts
    except ConnectionFailure as e:
        return {
            "statusCode": 500,
            "body": f"❌ Database connection error: {e}"
        }

    # Remove or mark unsubscribed
    result = collection.update_one({"work_emails": {"$regex": email}}, {"$set": {"unsubscribed": True}})

    if result.matched_count > 0:
        return {
            "statusCode": 200,
            "body": f"{email} has been unsubscribed successfully!"
        }
    else:
        return {
            "statusCode": 404,
            "body": f"No matching email found for {email}."
        }
