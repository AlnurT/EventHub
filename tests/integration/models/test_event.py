from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Event


async def test_event_model(session: AsyncSession) -> None:
    query = select(Event)
    result = await session.execute(query)
    event = result.scalar_one_or_none()

    query = select(User)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    assert event is not None
    assert event.id is not None
    assert event.title == "event"
    assert event.starts_at is not None
    assert event.organizer_id == user.id
    assert event.created_at is not None
    assert event.is_cancelled is False
