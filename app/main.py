from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.employee import router as employee_router
from app.api.task import router as task_router
from app.api.task_update import router as task_update_router
from app.api.telegram import router as telegram_router
from app.api.dashboard import router as dashboard_router
from app.api.reminder import router as reminder_router
from app.api.notification import router as notification_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(task_router)
app.include_router(task_update_router)
app.include_router(telegram_router)
app.include_router(dashboard_router)
app.include_router(reminder_router)
app.include_router(notification_router)


@app.get("/")
def health():
    return {
        "message": "Employee Reminder API Running"
    }