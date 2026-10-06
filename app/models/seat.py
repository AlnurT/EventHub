import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import uuid7

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.event import Event


class Seat(Base):
    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint("event_id", "row", "number", name="uq_event_row_number"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid7)
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id", ondelete="RESTRICT"))
    row: Mapped[int]
    number: Mapped[int]
    version: Mapped[int] = mapped_column(default=0)

    event: Mapped["Event"] = relationship(back_populates="seats")
