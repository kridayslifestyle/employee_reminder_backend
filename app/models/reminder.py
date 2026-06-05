import uuid

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

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

    reminder_count = Column(
        Integer,
        default=0
    )

    sent_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    last_sent_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )