import requests

from app.core.config import settings


def send_message(
    chat_id: str,
    text: str,
    reply_markup=None
):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    requests.post(
        url,
        json=payload
    )