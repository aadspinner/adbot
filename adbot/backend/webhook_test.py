from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

VERIFY_TOKEN = "test123"  # This must match what you enter in Meta

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

from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("🔔 Webhook received:", body)
    return {"status": "received"}