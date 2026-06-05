from app.models.task import Task
from app.models.employee import Employee

from app.services.telegram_service import send_message


def send_task_reminder(
    task,
    employee
):

    message = f"""
⏰ TASK REMINDER

Task:
{task.title}

Status:
{task.status}

Please update your task status.
"""

    send_message(
        employee.telegram_chat_id,
        message
    )