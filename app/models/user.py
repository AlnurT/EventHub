import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from app.models.base import Base


class Role(StrEnum):
    user = "user"
    organizer = "organizer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Role] = mapped_column(default=Role.user)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
