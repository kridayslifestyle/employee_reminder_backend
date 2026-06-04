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

    return task

@router.get(
    "/",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db)
):
    return db.query(Task).all()


