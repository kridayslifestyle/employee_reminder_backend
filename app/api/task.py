from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.employee import Employee
from app.models.telegram_state import TelegramState

from app.services.telegram_service import send_message


router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"]
)


@router.post("/webhook")
async def telegram_webhook(
    payload: dict,
    db: Session = Depends(get_db)
):

    # TELEGRAM BUTTON CLICKS
    callback_query = payload.get("callback_query")

    if callback_query:

        data = callback_query["data"]

        chat_id = str(
            callback_query["message"]["chat"]["id"]
        )

        print("CALLBACK:", data)

        send_message(
            chat_id,
            f"You clicked: {data}"
        )

        return {"ok": True}

    # TELEGRAM MESSAGES
    message = payload.get("message")

    if not message:
        return {"ok": True}

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "").strip()

    # START COMMAND
    if text == "/start":

        state = (
            db.query(TelegramState)
            .filter(
                TelegramState.chat_id == chat_id
            )
            .first()
        )

        if state:
            state.state = "waiting_employee_code"

        else:
            state = TelegramState(
                chat_id=chat_id,
                state="waiting_employee_code"
            )

            db.add(state)

        db.commit()

        send_message(
            chat_id,
            "Welcome to Hytoma Employee Reminder System\n\nPlease enter your Employee Code.\nExample: EMP001"
        )

        return {"ok": True}

    # EMPLOYEE CODE LINKING
    state = (
        db.query(TelegramState)
        .filter(
            TelegramState.chat_id == chat_id
        )
        .first()
    )

    if state and state.state == "waiting_employee_code":

        employee = (
            db.query(Employee)
            .filter(
                Employee.employee_code == text
            )
            .first()
        )

        if not employee:

            send_message(
                chat_id,
                "❌ Invalid Employee Code.\nPlease try again."
            )

            return {"ok": True}

        employee.telegram_chat_id = chat_id

        state.state = "linked"

        db.commit()

        send_message(
            chat_id,
            f"✅ Welcome {employee.name}\n\nYour account has been linked successfully."
        )

        return {"ok": True}

    return {"ok": True}