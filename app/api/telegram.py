from fastapi import APIRouter

from app.services.telegram_service import send_message

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"]
)


@router.post("/webhook")
async def telegram_webhook(payload: dict):

    message = payload.get("message")

    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]

    text = message.get("text", "")

    if text == "/start":

        send_message(
            chat_id,
            "Welcome to Hytoma Employee Reminder System\n\nPlease enter your Employee Code.\nExample: EMP001"
        )

    return {"ok": True} 