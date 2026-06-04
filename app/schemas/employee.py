from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class EmployeeCreate(BaseModel):
    employee_code: str
    name: str
    phone: Optional[str] = None
    department: Optional[str] = None


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    id: UUID
    employee_code: str
    name: str
    phone: Optional[str]
    department: Optional[str]
    telegram_chat_id: Optional[str]
    active: bool

    model_config = {
        "from_attributes": True
    }