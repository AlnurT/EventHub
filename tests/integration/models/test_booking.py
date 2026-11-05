import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Seat, Booking
from app.models.booking import Status


async def test_booking_model(session: AsyncSession) -> None:
    query = select(Booking)
    result = await session.execute(query)
    booking = result.scalar_one_or_none()

    query = select(User)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    query = select(Seat)
    result = await session.execute(query)
    seat = result.scalar_one_or_none()

    assert booking is not None
    assert booking.id is not None
    assert booking.seat_id == seat.id
    assert booking.user_id == user.id
    assert booking.status == Status.confirmed
    assert booking.created_at is not None


async def test_double_booking(session: AsyncSession) -> None:
    user2 = User(
        name="new_user2",
        email="user2@mail.ru",
        hashed_password="12345",
    )
    session.add(user2)
    await session.flush()

    query = select(Seat)
    result = await session.execute(query)
    seat = result.scalar_one_or_none()

    booking = Booking(
        seat_id=seat.id,
        user_id=user2.id,
    )
    session.add(booking)

    with pytest.raises(IntegrityError):
        await session.commit()


async def test_booking_after_cancel(session: AsyncSession) -> None:
    user2 = User(
        name="new_user2",
        email="user2@mail.ru",
        hashed_password="12345",
    )
    session.add(user2)
    await session.flush()

    query = select(Seat)
    result = await session.execute(query)
    seat = result.scalar_one_or_none()

    query = select(Booking)
    result = await session.execute(query)
    booking = result.scalar_one_or_none()
    booking.status = Status.cancelled

    booking2 = Booking(
        seat_id=seat.id,
        user_id=user2.id,
    )
    session.add(booking2)
    await session.commit()

    assert booking2 is not None
    assert booking2.id is not None
    assert booking2.seat_id == seat.id
    assert booking2.user_id == user2.id
    assert booking.status == Status.cancelled
    assert booking2.status == Status.confirmed
    assert booking2.created_at is not None
