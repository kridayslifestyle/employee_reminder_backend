from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.task import Task
from app.models.employee import Employee
from app.models.reminder import Reminder

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

        existing_reminder = (
            db.query(Reminder)
            .filter(
                Reminder.task_id == task.id
            )
            .order_by(
                Reminder.last_sent_at.desc()
            )
            .first()
        )

        if existing_reminder:

            thirty_minutes_ago = (
                datetime.now(timezone.utc) - timedelta(minutes=15)
            )

            if existing_reminder.last_sent_at > thirty_minutes_ago:
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
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🟡 In Progress",
                        "callback_data": f"in_progress:{task.id}"
                    }
                ],
                [
                    {
                        "text": "✅ Completed",
                        "callback_data": f"completed:{task.id}"
                    }
                ],
                [
                    {
                        "text": "🆘 Need Help",
                        "callback_data": f"need_help:{task.id}"
                    }
                ]
            ]
        }

        send_message(
            employee.telegram_chat_id,
            message,
            keyboard
        )

        if existing_reminder:

            existing_reminder.reminder_count += 1
            existing_reminder.last_sent_at = datetime.now(timezone.utc)

        else:

            reminder = Reminder(
                task_id=task.id,
                employee_id=employee.id,
                reminder_count=1
            )

            db.add(reminder)

        db.commit()

        reminders_sent += 1

    return {
        "success": True,
        "reminders_sent": reminders_sent
    }


@router.get("/stats")
def reminder_stats(
    db: Session = Depends(get_db)
):

    total_reminders = db.query(Reminder).count()

    return {
        "total_reminders_sent": total_reminders
    }