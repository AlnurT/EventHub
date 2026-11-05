from datetime import datetime

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.community.postgres import PostgresContainer

from app.models import Base, User, Event, Seat, Booking


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:16-alpine", driver="asyncpg") as postgres:
        yield postgres


async def set_data(session):
    user = User(
        name="new_user",
        email="user@mail.ru",
        hashed_password="12345",
    )
    session.add(user)
    await session.flush()

    event = Event(
        title="event",
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
    await session.flush()

    booking = Booking(
        seat_id=seat.id,
        user_id=user.id,
    )
    session.add(booking)

    await session.commit()


@pytest.fixture(scope="session", name="engine")
async def async_test_engine(postgres_container):
    engine = create_async_engine(
        postgres_container.get_connection_url(), poolclass=NullPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        await set_data(session)

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