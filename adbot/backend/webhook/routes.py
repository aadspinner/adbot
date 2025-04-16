from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

VERIFY_TOKEN = "your_meta_verify_token_here"

@router.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)
    return PlainTextResponse(content="Verification failed", status_code=403)

@router.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("📩 Webhook POST received:", body)
    return {"status": "received"}
