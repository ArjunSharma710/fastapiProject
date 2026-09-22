"""add foreign-key to posts table

Revision ID: d6afd1f5f33c
Revises: 7b8ad9e5a58c
Create Date: 2026-09-12 11:20:28.738978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6afd1f5f33c'
down_revision: Union[str, Sequence[str], None] = '7b8ad9e5a58c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    print(">>> ENTERING add_foreign_key upgrade()")
    try:
        op.add_column('posts', sa.Column('owner_id', sa.INTEGER, nullable=False))
        op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
        print(">>> add_column + create_foreign_key SUCCEEDED")
    except Exception as e:
        print(">>> FAILED:", repr(e))
        raise


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
