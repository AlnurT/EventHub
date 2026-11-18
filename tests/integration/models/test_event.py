from sqlalchemy.ext.asyncio import AsyncSession


async def test_event_model(user, event) -> None:
    assert event.id is not None
    assert event.description == ""
    assert event.organizer_id == user.id
    assert event.created_at is not None
    assert event.is_cancelled is False


async def test_event_organizer_to_null_after_delete(session: AsyncSession, user, event) -> None:
    await session.delete(user)
    await session.flush()
    await session.refresh(event)

    assert event.organizer_id is None
