from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.employee import Employee
from app.models.task import Task


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_employees = db.query(Employee).count()

    active_employees = (
        db.query(Employee)
        .filter(Employee.active == True)
        .count()
    )

    total_tasks = db.query(Task).count()

    completed_tasks = (
        db.query(Task)
        .filter(Task.status == "completed")
        .count()
    )

    in_progress_tasks = (
        db.query(Task)
        .filter(Task.status == "in_progress")
        .count()
    )

    pending_tasks = (
        db.query(Task)
        .filter(Task.status == "not_started")
        .count()
    )

    need_help_tasks = (
        db.query(Task)
        .filter(Task.status == "need_help")
        .count()
    )

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "pending_tasks": pending_tasks,
        "need_help_tasks": need_help_tasks
    }