from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.employee import router as employee_router
from app.api.task import router as task_router
from app.api.task_update import router as task_update_router
from app.api.telegram import router as telegram_router

app = FastAPI(
    title="Employee Reminder System"
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(task_router)
app.include_router(task_update_router)
app.include_router(telegram_router)

@app.get("/")
def health():
    return {
        "message": "Employee Reminder API Running"
    }