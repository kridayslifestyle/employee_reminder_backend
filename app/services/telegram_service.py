import requests

from app.core.config import settings


def send_message(
    chat_id: str,
    text: str
):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": text
        }
    )