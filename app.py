from flask import Flask, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import json, os

creds_dict = json.loads(os.environ["GOOGLE_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict, scope
)
client = gspread.authorize(creds)

# 🔑 PASTE YOUR GOOGLE SHEET ID BELOW
sheet = client.open_by_key("1x31XCMZTnfam8Z3MGdGpHuMJMHU8aeYk-59FXayI4KA").sheet1

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.form.get("Body")
    resp = MessagingResponse()

    try:
        name, phone, city, profession, dob = msg.split(",")

        sheet.append_row([
            name.strip(),
            phone.strip(),
            city.strip(),
            profession.strip(),
            dob.strip()
        ])

        # ✅ AUTO REPLY
        resp.message("Thanks! Mee details save ayyayi 👍")

    except:
        resp.message(
            "Wrong format ❌\n"
            "Use:\n"
            "Name,Phone,City,Profession,DOB\n"
            "Example:\n"
            "Ramesh,9876543210,Hyderabad,Engineer,15-08-1992"
        )

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)

