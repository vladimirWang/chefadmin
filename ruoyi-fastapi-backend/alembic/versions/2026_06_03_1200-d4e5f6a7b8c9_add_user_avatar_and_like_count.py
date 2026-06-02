"""add user avatar_url like_count and dish like_count

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-06-03 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = 'd4e5f6a7b8c9'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user',
        sa.Column('avatar_url', sa.String(length=512), nullable=True, comment='头像URL'),
    )
    op.add_column(
        'user',
        sa.Column('like_count', sa.Integer(), nullable=False, server_default='0', comment='获赞总数'),
    )
    op.add_column(
        'dish',
        sa.Column('like_count', sa.Integer(), nullable=False, server_default='0', comment='点赞数'),
    )


def downgrade() -> None:
    op.drop_column('dish', 'like_count')
    op.drop_column('user', 'like_count')
    op.drop_column('user', 'avatar_url')
