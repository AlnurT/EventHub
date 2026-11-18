import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import Role


async def test_user_model(user) -> None:
    assert user.id is not None
    assert user.role == Role.user
    assert user.created_at is not None


async def test_user_email_duplicate(user, make_user) -> None:
    with pytest.raises(IntegrityError) as exc_info:
        await make_user(user.email)

    assert 'violates unique constraint "uq_users_email"' in str(exc_info.value)
