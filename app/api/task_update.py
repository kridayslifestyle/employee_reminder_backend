from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.constants.task_status import VALID_STATUSES
from app.database.database import get_db

from app.models.task import Task
from app.models.task_update import TaskUpdate
from app.models.employee import Employee

from app.schemas.task_update import TaskUpdateCreate

router = APIRouter(
    prefix="/task-updates",
    tags=["Task Updates"]
)

@router.post("/")
def create_task_update(
    payload: TaskUpdateCreate,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == payload.task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    employee = (
        db.query(Employee)
        .filter(Employee.id == payload.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update = TaskUpdate(
        task_id=payload.task_id,
        employee_id=payload.employee_id,
        status=payload.status,
        note=payload.note
    )

    db.add(update)

    task.status = payload.status

    if payload.status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    if payload.status == "completed":
        task.completed_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Task updated successfully"
    }

@router.get("/{task_id}")
def get_task_updates(
    task_id: str,
    db: Session = Depends(get_db)
):
    updates = (
        db.query(TaskUpdate)
        .filter(TaskUpdate.task_id == task_id)
        .all()
    )

    return updates