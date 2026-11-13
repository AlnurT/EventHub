import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Role


async def test_user_model(session: AsyncSession, user):
    assert user.id is not None
    assert user.role == Role.user
    assert user.created_at is not None


async def test_user_email_duplicate(session: AsyncSession, user, make_user):
    with pytest.raises(IntegrityError):
        await make_user("user@example.com")
