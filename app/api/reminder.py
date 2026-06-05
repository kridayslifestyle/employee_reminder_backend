from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.task import Task
from app.models.employee import Employee

from app.services.telegram_service import send_message


router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)


@router.post("/run")
def run_reminders(
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .filter(
            Task.status != "completed"
        )
        .all()
    )

    reminders_sent = 0

    for task in tasks:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == task.assigned_to
            )
            .first()
        )

        if not employee:
            continue

        if not employee.telegram_chat_id:
            continue

        message = f"""
⏰ TASK REMINDER

📝 Task:
{task.title}

📄 Description:
{task.description}

📊 Status:
{task.status}

Please update your task status.
"""

        send_message(
            employee.telegram_chat_id,
            message
        )

        reminders_sent += 1

    return {
        "success": True,
        "reminders_sent": reminders_sent
    }