from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"))
    row: Mapped[int]
    number: Mapped[int]

    __table_args__ = (
        UniqueConstraint("event_id", "row", "number", name="uq_event_row_number"),
    )
