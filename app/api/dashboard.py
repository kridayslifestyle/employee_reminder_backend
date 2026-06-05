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

@router.get("/recent-tasks")
def get_recent_tasks(
    db: Session = Depends(get_db)
):

    tasks = (
        db.query(Task)
        .order_by(Task.created_at.desc())
        .limit(10)
        .all()
    )

    data = []

    for task in tasks:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id == task.assigned_to
            )
            .first()
        )

        data.append({
            "id": str(task.id),
            "title": task.title,
            "employee_name": employee.name if employee else None,
            "status": task.status,
            "due_time": task.due_time,
            "created_at": task.created_at
        })

    return data