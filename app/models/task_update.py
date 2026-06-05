import uuid

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class TaskUpdate(Base):
    __tablename__ = "task_updates"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    task_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "tasks.id",
            ondelete="CASCADE"
        )
    )

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id")
    )

    status = Column(
        String(50)
    )

    note = Column(
        Text
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )