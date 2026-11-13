import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Status


async def test_booking_model(session, user, seat, booking):
    assert booking.id is not None
    assert booking.seat_id == seat.id
    assert booking.user_id == user.id
    assert booking.status == Status.confirmed
    assert booking.created_at is not None


async def test_booking_user_delete(session: AsyncSession, user, booking):
    await session.delete(user)
    await session.flush()
    await session.refresh(booking)

    assert booking.id is not None
    assert booking.user_id is None


async def test_booking_seat_delete(session: AsyncSession, seat, booking):
    with pytest.raises(IntegrityError):
        await session.delete(seat)
        await session.flush()
        await session.refresh(booking)


async def test_double_booking(session: AsyncSession, user, make_user, booking, make_booking) -> None:
    user2 = await make_user("user2@example.com")

    with pytest.raises(IntegrityError):
        await make_booking(user2)


async def test_booking_after_cancel(session: AsyncSession, user, make_user, booking, make_booking) -> None:
    user2 = await make_user("user2@example.com")
    booking.status = Status.cancelled
    booking2 = await make_booking(user2)

    assert booking2.id is not None
    assert booking2.seat_id == booking.seat_id
    assert booking2.user_id != booking.user_id
    assert booking.status == Status.cancelled
    assert booking2.status == Status.confirmed
    assert booking2.created_at is not None
