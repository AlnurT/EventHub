from enum import StrEnum

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Status(StrEnum):
    confirmed = "confirmed"
    cancelled = "cancelled"


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seat.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[Status] = mapped_column(default=Status.confirmed)

    __table_args__ = (
        Index(
            "idx_status_confirmed",
            "status",
            unique=True,
            postgresql_where=(status == Status.confirmed),
        ),
    )
