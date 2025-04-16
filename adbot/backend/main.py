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
from fastapi import FastAPI, Request
import hashlib
from fastapi.responses import PlainTextResponse

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "your_expected_token_here"  # Replace this with your actual VERIFY_TOKEN from .env

from fastapi import FastAPI
from webhook.routes import router as webhook_router

# ✅ Webhook verification
VERIFY_TOKEN = "test123"

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("🔍 MODE:", mode)
    print("🔍 TOKEN RECEIVED:", token)
    print("🔐 TOKEN EXPECTED:", VERIFY_TOKEN)
    print("🎯 CHALLENGE:", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        return PlainTextResponse(content="Verification failed", status_code=403)

# ✅ Webhook event POST handler
@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("🔔 Webhook received:", body)
    return {"status": "received"}

# ✅ Example: Your regular routes can go here too
@app.get("/")
async def root():
    return {"message": "AdBot backend is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

