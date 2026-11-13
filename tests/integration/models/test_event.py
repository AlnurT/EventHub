from sqlalchemy.ext.asyncio import AsyncSession


async def test_event_model(session: AsyncSession, user, event):
    assert event.id is not None
    assert event.starts_at is not None
    assert event.organizer_id == user.id
    assert event.created_at is not None
    assert event.is_cancelled is False


async def test_event_organizer_delete(session: AsyncSession, user, event):
    await session.delete(user)
    await session.flush()
    await session.refresh(event)

    assert event.id is not None
    assert event.organizer_id is None
