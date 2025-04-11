import os
import oracledb
import requests
from dotenv import load_dotenv
from datetime import timezone, timedelta
from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from twilio.rest import Client
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


# Load environment variables
load_dotenv()

print("SID:", os.getenv("TWILIO_SID"))
print("TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))

# Timezone setup
IST = timezone(timedelta(hours=5, minutes=30))

# Oracle client setup
oracledb.init_oracle_client(lib_dir="/app/oracle_client/instantclient_23_7")

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
#app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware (required for JS in browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Config
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")

# Twilio creds from .env

TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = "whatsapp:+14155238886"
TWILIO_TO = "whatsapp:+918277646669"


def send_whatsapp_alert(name, email, phone):
    print("Calling Twilio to send WhatsApp alert...")

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message_body = f"🚨 New Lead Submitted!\nName: {name}\nEmail: {email}\nPhone: {phone}"

    message = client.messages.create(
        body=message_body,
        from_=TWILIO_FROM,
        to=TWILIO_TO
    )

    print("WhatsApp message sent:", message.sid)

class Lead(BaseModel):
    name: str
    email: str
    phone: str

@app.post("/submit")
async def handle_submission(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    payload = {
        "NAME": name,
        "EMAIL": email,
        "PHONE": phone
    }

    ords_url = "https://GB806C347ABF915-USERDETAILS.adb.ap-mumbai-1.oraclecloudapps.com/ords/admin/leads/"
    headers = {"Content-Type": "application/json"}
    response = requests.post(ords_url, json=payload, headers=headers)

    if response.status_code == 201:
        send_whatsapp_alert(name, email, phone)
        return JSONResponse(content={"message": "Lead submitted"})
    else:
        print("ORDS Error:", response.text)
        return JSONResponse(status_code=500, content={"message": "Error submitting lead"})

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID, NAME, EMAIL, PHONE, SUBMITTED_AT FROM LEADS ORDER BY SUBMITTED_AT DESC")
            leads = []
            for row in cursor:
                id, name, email, phone, submitted_at = row
                if submitted_at:
                    submitted_at = submitted_at.astimezone(IST)
                    submitted_at_str = submitted_at.strftime("%d %B %Y, %-I:%M %p")
                else:
                    submitted_at_str = "N/A"
                leads.append((id, name, email, phone, submitted_at_str))

    return templates.TemplateResponse("dashboard.html", {"request": request, "leads": leads})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
