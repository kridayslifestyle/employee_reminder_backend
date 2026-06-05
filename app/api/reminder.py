from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.task import Task
from app.models.employee import Employee

from app.services.reminder_service import (
    send_task_reminder
)

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

    count = 0

    for task in tasks:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == task.assigned_to
            )
            .first()
        )

        if employee and employee.telegram_chat_id:

            send_task_reminder(
                task,
                employee
            )

            count += 1

    return {
        "reminders_sent": count
    }