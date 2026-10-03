import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.seat import Seat


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255), default="")
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    organizer_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_cancelled: Mapped[bool] = mapped_column(default=False)

    seats: Mapped[list["Seat"]] = relationship(back_populates="event")
