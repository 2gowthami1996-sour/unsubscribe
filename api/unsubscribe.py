import os
from pymongo import MongoClient
from urllib.parse import parse_qs
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Store temporary unsubscribe requests in memory (optional)
pending_unsubscribes = {}

def handler(request):
    method = request.get("method", "GET").upper()
    qs = parse_qs(request.get("queryString", ""))
    email = qs.get("email", [""])[0]

    if method == "GET":
        if not email:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "text/html"},
                "body": "<p>⚠ No email provided in URL.</p>"
            }

        # Show confirmation page
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unsubscribe</title>
            <style>
                body {{ font-family: Arial,sans-serif; text-align:center; margin-top:50px; }}
                button {{ padding:10px 20px; font-size:16px; cursor:pointer; }}
            </style>
        </head>
        <body>
            <h2>Unsubscribe from Morphius AI Emails</h2>
            <p>Click the button below to unsubscribe: <strong>{email}</strong></p>
            <form method="POST">
                <input type="hidden" name="email" value="{email}">
                <button type="submit">Confirm Unsubscribe</button>
            </form>
        </body>
        </html>
        """
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }

    elif method == "POST":
        # Get email from form submission
        form_data = parse_qs(request.get("body", ""))
        email = form_data.get("email", [""])[0]

        if email:
            query = {
                "$or": [
                    {"work_emails": {"$regex": fr"\b{email}\b", "$options": "i"}},
                    {"personal_emails": {"$regex": fr"\b{email}\b", "$options": "i"}}
                ]
            }
            result = db.cleaned_contacts.update_many(query, {"$set": {"subscribed": False}})
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Unsubscribed</title>
                <style>
                    body {{ font-family: Arial,sans-serif; text-align:center; margin-top:50px; color:green; }}
                </style>
            </head>
            <body>
                <h2>✅ You have been unsubscribed successfully!</h2>
                <p>{email}</p>
            </body>
            </html>
            """
            return {"statusCode": 200, "headers": {"Content-Type": "text/html"}, "body": html}
        else:
            return {
                "statusCode": 400,
                "headers": {"Content-Type": "text/html"},
                "body": "<p>⚠ No email provided.</p>"
            }

    else:
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "text/html"},
            "body": "<p>Method not allowed</p>"
        }
