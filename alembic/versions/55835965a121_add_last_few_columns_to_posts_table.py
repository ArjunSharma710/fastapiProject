"""add last few columns to posts table

Revision ID: 55835965a121
Revises: d6afd1f5f33c
Create Date: 2026-09-16 17:02:56.886732

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '55835965a121'
down_revision: Union[str, Sequence[str], None] = 'd6afd1f5f33c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    print(">>> ENTERING add_last_few_columns upgrade()")
    try:
        op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
        op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
        print(">>> BOTH COLUMNS ADDED SUCCEEDED")
    except Exception as e:
        print(">>> FAILED:", repr(e))
        raise

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
