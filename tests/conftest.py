from datetime import UTC, datetime

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.community.postgres import PostgresContainer

from app.models import Base, Booking, Event, Seat, User
from app.models.booking import Status


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine", driver="asyncpg") as postgres:
        yield postgres


@pytest.fixture(scope="session", name="engine")
async def async_test_engine(postgres_container):
    engine = create_async_engine(
        postgres_container.get_connection_url(), poolclass=NullPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="function", name="session")
async def async_test_session(engine):
    async with engine.connect() as conn:
        transaction = await conn.begin()
        async with AsyncSession(
                bind=conn,
                join_transaction_mode="create_savepoint",
                expire_on_commit=False
            ) as session:
            yield session

        await transaction.rollback()


@pytest.fixture
def make_user(session):
    async def _make_user(email: str, name: str = "user", password: str = "12345"):
        user = User(
            name=name,
            email=email,
            hashed_password=password,
        )
        session.add(user)
        await session.flush()
        return user

    return _make_user


@pytest.fixture
async def user(make_user):
    return await make_user("user@example.com")


@pytest.fixture
def make_event(session, user):
    async def _make_event(title: str = "event"):
        event = Event(
            title=title,
            starts_at=datetime.now(UTC),
            organizer_id=user.id,
        )
        session.add(event)
        await session.flush()
        return event

    return _make_event


@pytest.fixture
async def event(make_event):
    return await make_event()


@pytest.fixture
def make_seat(session):
    async def _make_seat(event, row: int = 1, number: int = 2):
        seat = Seat(
            event_id=event.id,
            row=row,
            number=number,
        )
        session.add(seat)
        await session.flush()
        return seat

    return _make_seat


@pytest.fixture
async def seat(make_seat, event):
    return await make_seat(event)


@pytest.fixture
def make_booking(session):
    async def _make_booking(user, seat, status: Status = Status.confirmed):
        booking = Booking(
            seat_id=seat.id,
            user_id=user.id,
            status=status,
        )
        session.add(booking)
        await session.flush()
        return booking

    return _make_booking


@pytest.fixture
async def booking(make_booking, seat, user):
    return await make_booking(user, seat)
