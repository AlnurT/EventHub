import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


async def test_seat_model(session: AsyncSession, seat, event) -> None:
    assert seat.id is not None
    assert seat.event_id == event.id


async def test_seat_another_event(session: AsyncSession, event, make_event, seat, make_seat) -> None:
    event2 = await make_event()
    seat2 = await make_seat(event2)

    assert seat2.id is not None
    assert seat2.event_id == event2.id
    assert seat.event_id != seat2.event_id
    assert seat.row == seat2.row
    assert seat.number == seat2.number


async def test_seat_event_delete(session: AsyncSession, event, seat):
    with pytest.raises(IntegrityError):
        await session.delete(event)
        await session.flush()
        await session.refresh(seat)


async def test_seat_duplicate(session: AsyncSession, event, seat, make_seat):
    with pytest.raises(IntegrityError):
        await make_seat(event)
