import os
from urllib.parse import unquote
from pymongo import MongoClient

# Load MongoDB info from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Connect to MongoDB once
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db.cleaned_contacts

# Vercel serverless handler
def handler(request, response):
    try:
        # Vercel passes query parameters in request.query
        email = request.args.get("email")
        if not email:
            response.status_code = 400
            response.text = "❌ No email provided."
            return response

        email = unquote(email)

        result = collection.update_one(
            {"work_emails": {"$regex": email, "$options": "i"}},
            {"$set": {"subscribed": False}}
        )

        if result.matched_count > 0:
            response.text = f"✅ {email} has been unsubscribed successfully!"
        else:
            response.status_code = 404
            response.text = f"⚠ No matching email found for {email}."
        return response

    except Exception as e:
        response.status_code = 500
        response.text = f"❌ Server Error: {str(e)}"
        return response
