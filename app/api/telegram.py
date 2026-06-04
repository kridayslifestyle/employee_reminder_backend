from fastapi import APIRouter

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"]
)


@router.post("/webhook")
async def telegram_webhook(payload: dict):
    print(payload)

    return {"ok": True}