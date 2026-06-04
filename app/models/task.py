import uuid

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text
    )

    assigned_to = Column(
        UUID(as_uuid=True),
        ForeignKey("employees.id")
    )

    assigned_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id")
    )

    status = Column(
        String(50),
        default="not_started"
    )

    due_time = Column(
        DateTime(timezone=True)
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )