"""add content column to posts table

Revision ID: 588c42049648
Revises: ada0dddcf0e3
Create Date: 2024-05-08 16:06:03.818790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '588c42049648'
down_revision: Union[str, None] = 'ada0dddcf0e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
