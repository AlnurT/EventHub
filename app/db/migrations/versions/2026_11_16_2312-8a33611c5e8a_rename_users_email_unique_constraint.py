"""rename users email unique constraint

Revision ID: 8a33611c5e8a
Revises: 849f95143e23
Create Date: 2026-11-16 23:12:49.367453

"""
from collections.abc import Sequence

from alembic import op

revision: str = '8a33611c5e8a'
down_revision: str | Sequence[str] | None = '849f95143e23'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('users_email_key'), 'users', type_='unique')
    op.create_unique_constraint('user_email_unique', 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('user_email_unique', 'users', type_='unique')
    op.create_unique_constraint(op.f('users_email_key'), 'users', ['email'], postgresql_nulls_not_distinct=False)
