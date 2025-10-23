import os
from urllib.parse import unquote
from pymongo import MongoClient

# Load environment variables from Vercel dashboard
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db.cleaned_contacts

def handler(request, response):
    # Get email from query string
    email = request.args.get("email")
    if not email:
        response.status_code = 400
        response.text = "❌ No email provided."
        return response

    email = unquote(email)

    try:
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
