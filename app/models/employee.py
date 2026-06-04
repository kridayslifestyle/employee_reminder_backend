import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    employee_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    phone = Column(
        String(20)
    )

    department = Column(
        String(100)
    )

    telegram_chat_id = Column(
        String(100),
        nullable=True
    )

    active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )