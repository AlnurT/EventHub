import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from app.models.base import Base


class Status(StrEnum):
    confirmed = "confirmed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index(
            "uq_confirmed_booking_per_seat",
            "seat_id",
            unique=True,
            postgresql_where=text("status = 'confirmed'"),
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    seat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("seats.id", ondelete="RESTRICT"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    status: Mapped[Status] = mapped_column(default=Status.confirmed)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
