"""add content column to posts table

Revision ID: 64ca17f1648a
Revises: fa134f2fa439
Create Date: 2026-09-11 10:58:57.783377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64ca17f1648a'
down_revision: Union[str, Sequence[str], None] = 'fa134f2fa439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',sa.Column('content',sa.String(),nullable= False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
