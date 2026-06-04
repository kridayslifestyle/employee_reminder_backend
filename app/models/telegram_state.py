import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class TelegramState(Base):
    __tablename__ = "telegram_states"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    chat_id = Column(
        String(100),
        unique=True
    )

    state = Column(
        String(50)
    )