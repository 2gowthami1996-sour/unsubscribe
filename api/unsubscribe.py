import os
from pymongo import MongoClient
from urllib.parse import parse_qs
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def handler(request):
    qs = parse_qs(request.get("queryString", ""))
    email = qs.get("email", [""])[0]

    if not email:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "text/html"},
            "body": "<p>⚠ No email provided in URL.</p>"
        }

    db.cleaned_contacts.update_many(
        {"$or": [
            {"work_emails": {"$regex": fr"\b{email}\b", "$options": "i"}},
            {"personal_emails": {"$regex": fr"\b{email}\b", "$options": "i"}}
        ]},
        {"$set": {"subscribed": False}}
    )

    html = f"""
    <html><body style="text-align:center;margin-top:50px;">
    <h2>✅ {email} has been unsubscribed successfully!</h2>
    </body></html>
    """

    return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": html}
