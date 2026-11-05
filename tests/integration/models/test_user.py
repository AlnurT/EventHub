from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.user import Role


async def test_user_model(session: AsyncSession) -> None:
    query = select(User)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.id is not None
    assert user.name == "new_user"
    assert user.email == "user@mail.ru"
    assert user.hashed_password == "12345"
    assert user.role == Role.user
    assert user.created_at is not None
