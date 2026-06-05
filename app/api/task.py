from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.task import Task
from app.models.employee import Employee

from app.schemas.task import (
    TaskCreate,
    TaskResponse
)

from app.dependencies.auth import (
    get_current_user
)

from app.services.telegram_service import send_message


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "/",
    response_model=TaskResponse
)
def create_task(
    payload: TaskCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == payload.assigned_to
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    task = Task(
        title=payload.title,
        description=payload.description,
        assigned_to=payload.assigned_to,
        assigned_by=current_user["sub"],
        due_time=payload.due_time
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    if employee.telegram_chat_id:

        message = f"""
📌 NEW TASK ASSIGNED

📝 Title:
{task.title}

📄 Description:
{task.description}

⏰ Due:
{task.due_time}

❌ Status:
Not Started
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

    return task


@router.get("/")
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    result = []

    for task in tasks:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == task.assigned_to
            )
            .first()
        )

        result.append({
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "employee_name":
                employee.name
                if employee
                else "Unknown",
            "due_time": task.due_time
        })

    return result