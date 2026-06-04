from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class TaskUpdateCreate(BaseModel):
    task_id: UUID
    employee_id: UUID
    status: str
    note: Optional[str] = None