import uuid

from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = DateTime(
        timezone=True,
        server_default=func.now()
    )


class UUIDMixin:
    id = UUID(
        as_uuid=True
    )