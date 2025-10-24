from pymongo import MongoClient
from urllib.parse import unquote
import os

# MongoDB settings from Vercel environment variables
MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME")

def handler(request, response):
    # Read email from query string
    email = request.args.get("email")
    email = unquote(email or "")
    
    if not email:
        response.status_code = 400
        response.text = "❌ Missing email parameter"
        return response

    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]

        # Mark the email as unsubscribed
        result = db.cleaned_contacts.update_one(
            {"work_emails": email},
            {"$set": {"unsubscribed": True}}
        )
        client.close()

        if result.matched_count:
            response.text = f"✅ {email} has been unsubscribed successfully!"
        else:
            response.text = f"⚠ No matching email found for {email}"

    except Exception as e:
        response.status_code = 500
        response.text = f"❌ Server Error: {str(e)}"
