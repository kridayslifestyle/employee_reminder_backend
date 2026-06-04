from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: UUID
    due_time: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_time: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    assigned_to: UUID
    assigned_by: UUID
    status: str

    model_config = {
        "from_attributes": True
    }