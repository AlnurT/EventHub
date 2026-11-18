import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, Status


async def test_booking_model(user, seat, booking) -> None:
    assert booking.id is not None
    assert booking.seat_id == seat.id
    assert booking.user_id == user.id
    assert booking.status == Status.confirmed
    assert booking.created_at is not None


async def test_booking_user_to_null_after_delete(session: AsyncSession, user, booking) -> None:
    await session.delete(user)
    await session.flush()
    await session.refresh(booking)

    assert booking.user_id is None


async def test_booking_seat_delete_restrict(session: AsyncSession, seat, booking) -> None:
    await session.delete(seat)

    with pytest.raises(IntegrityError) as exc_info:
        await session.flush()

    assert 'violates foreign key constraint "fk_bookings_seat_id_seats"' in str(exc_info.value)


async def test_double_booking(make_user, seat, booking, make_booking) -> None:
    user2 = await make_user("user2@example.com")

    with pytest.raises(IntegrityError) as exc_info:
        await make_booking(user2, seat)

    assert 'violates unique constraint "uq_confirmed_booking_per_seat"' in str(exc_info.value)


async def test_booking_after_cancel(session: AsyncSession, user, make_user, seat, booking, make_booking) -> None:
    booking.status = Status.cancelled
    await session.flush()

    user2 = await make_user("user2@example.com")
    await make_booking(user2, seat)

    stmt = (
        select(Booking.status, func.count(Booking.id))
        .where(Booking.seat_id == seat.id)
        .group_by(Booking.status)
    )
    result = await session.execute(stmt)
    counts_by_status = dict(result.all())

    assert counts_by_status == {
        Status.cancelled: 1,
        Status.confirmed: 1,
    }


async def test_booking_double_cancel(session: AsyncSession, user, make_user, seat, make_booking) -> None:
    await make_booking(user, seat, Status.cancelled)
    user2 = await make_user("user2@example.com")
    await make_booking(user2, seat, Status.cancelled)

    stmt = (
        select(Booking.status, func.count(Booking.id))
        .where(Booking.seat_id == seat.id)
        .group_by(Booking.status)
    )
    result = await session.execute(stmt)
    counts_by_status = dict(result.all())

    assert counts_by_status == {
        Status.cancelled: 2,
    }
