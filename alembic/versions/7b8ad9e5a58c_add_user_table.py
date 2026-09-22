"""add user table

Revision ID: 7b8ad9e5a58c
Revises: 64ca17f1648a
Create Date: 2026-09-11 17:28:09.191162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b8ad9e5a58c'
down_revision: Union[str, Sequence[str], None] = '64ca17f1648a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    print(">>> ENTERING add_user_table upgrade()")
    try:
        op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )
        print(">>> create_table SUCCEEDED")
    except Exception as e:
        print(">>> create_table FAILED:", repr(e))
        raise
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
