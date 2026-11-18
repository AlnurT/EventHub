"""fix constraint naming

Revision ID: f7faf6ee7756
Revises: 8a33611c5e8a
Create Date: 2026-11-17 21:58:11.449887

"""
from collections.abc import Sequence

from alembic import op

revision: str = 'f7faf6ee7756'
down_revision: str | Sequence[str] | None = '8a33611c5e8a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('uq_event_row_number'), 'seats', type_='unique')
    op.create_unique_constraint(op.f('uq_seats_event_id'), 'seats', ['event_id', 'row', 'number'])
    op.drop_constraint(op.f('user_email_unique'), 'users', type_='unique')
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_users_email'), 'users', type_='unique')
    op.create_unique_constraint(op.f('user_email_unique'), 'users', ['email'], postgresql_nulls_not_distinct=False)
    op.drop_constraint(op.f('uq_seats_event_id'), 'seats', type_='unique')
    op.create_unique_constraint(op.f('uq_event_row_number'), 'seats', ['event_id', 'row', 'number'], postgresql_nulls_not_distinct=False)
