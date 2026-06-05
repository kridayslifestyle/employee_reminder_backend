from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.models.task import Task

from app.database.database import get_db
from app.models.employee import Employee

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.post(
    "/",
    response_model=EmployeeResponse
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = (
        db.query(Employee)
        .filter(
            Employee.employee_code == payload.employee_code
        )
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee code already exists"
        )

    employee = Employee(
        employee_code=payload.employee_code,
        name=payload.name,
        phone=payload.phone,
        department=payload.department
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee

@router.get(
    "/",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    return db.query(Employee).all()

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: str,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data = payload.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee

@router.delete("/{employee_id}")
def deactivate_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.active = False

    db.commit()

    return {
        "message": "Employee deactivated"
    }

@router.put("/{employee_id}/activate")
def activate_employee(
    employee_id: str,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    employee.active = True

    db.commit()

    return {
        "message": "Employee activated"
    }

@router.get("/{employee_id}/details")
def employee_details(
    employee_id: str,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    tasks = (
        db.query(Task)
        .filter(Task.assigned_to == employee_id)
        .all()
    )

    completed = len([
        t for t in tasks
        if t.status == "completed"
    ])

    pending = len([
        t for t in tasks
        if t.status == "not_started"
    ])

    need_help = len([
        t for t in tasks
        if t.status == "need_help"
    ])

    return {
        "employee": {
            "id": str(employee.id),
            "employee_code": employee.employee_code,
            "name": employee.name,
            "phone": employee.phone,
            "department": employee.department,
            "active": employee.active
        },

        "stats": {
            "total_tasks": len(tasks),
            "completed_tasks": completed,
            "pending_tasks": pending,
            "need_help_tasks": need_help
        },

        "tasks": [
            {
                "id": str(task.id),
                "title": task.title,
                "status": task.status,
                "due_time": task.due_time,
                "description": task.description
            }
            for task in tasks
        ]
    }