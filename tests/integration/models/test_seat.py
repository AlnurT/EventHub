from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Event, Seat, User


async def test_seat_model(session: AsyncSession) -> None:
    query = select(Seat)
    result = await session.execute(query)
    seat = result.scalar_one_or_none()

    query = select(Event)
    result = await session.execute(query)
    event = result.scalar_one_or_none()

    assert seat is not None
    assert seat.id is not None
    assert seat.event_id == event.id
    assert seat.row == 1
    assert seat.number == 2
    assert seat.version == 0


async def test_seat_another_event(session: AsyncSession) -> None:
    query = select(User)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    event = Event(
        title="event2",
        starts_at=datetime.now(),
        organizer_id=user.id,
    )
    session.add(event)
    await session.flush()

    seat = Seat(
        event_id=event.id,
        row=1,
        number=2,
    )
    session.add(seat)
    await session.commit()

    assert seat is not None
    assert seat.id is not None
    assert seat.event_id == event.id
    assert seat.row == 1
    assert seat.number == 2
    assert seat.version == 0


async def test_seat_duplicate(session: AsyncSession) -> None:
    query = select(Event)
    result = await session.execute(query)
    event = result.scalar_one_or_none()

    seat = Seat(
        event_id=event.id,
        row=1,
        number=2,
    )
    session.add(seat)

    with pytest.raises(IntegrityError):
        await session.commit()
