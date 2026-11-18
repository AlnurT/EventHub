import pytest
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Event


async def test_seat_model(seat, event) -> None:
    assert seat.id is not None
    assert seat.event_id == event.id
    assert seat.version == 0


async def test_seat_another_event_same_places(event, make_event, make_seat) -> None:
    event2 = await make_event()

    seat = await make_seat(event, row=1, number=2)
    seat2 = await make_seat(event2, row=1, number=2)

    assert seat2.id is not None
    assert seat2.event_id == event2.id
    assert seat.event_id != seat2.event_id


async def test_seat_event_delete_restrict(session: AsyncSession, event, seat) -> None:
    stmt = delete(Event).where(Event.id == event.id)

    with pytest.raises(IntegrityError) as exc_info:
        await session.execute(stmt)

    assert 'violates foreign key constraint "fk_seats_event_id_events"' in str(exc_info.value)


async def test_seat_duplicate(event, make_seat) -> None:
    await make_seat(event, row=1, number=2)

    with pytest.raises(IntegrityError) as exc_info:
        await make_seat(event, row=1, number=2)

    assert 'violates unique constraint "uq_seats_event_id_row_number"' in str(exc_info.value)
