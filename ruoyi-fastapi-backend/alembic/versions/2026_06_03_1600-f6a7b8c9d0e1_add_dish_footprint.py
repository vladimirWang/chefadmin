"""add dish_footprint table

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-06-03 16:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect


revision: str = 'f6a7b8c9d0e1'
down_revision: Union[str, Sequence[str], None] = 'e5f6a7b8c9d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FOOTPRINT_INDEX = 'dish_footprint_user_id_viewed_at_idx'


def upgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)

    if not insp.has_table('dish_footprint'):
        op.create_table(
            'dish_footprint',
            sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='足迹ID'),
            sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
            sa.Column('dish_id', sa.Integer(), nullable=False, comment='菜品ID'),
            sa.Column('viewed_at', sa.DateTime(), nullable=False, comment='最近浏览时间'),
            sa.ForeignKeyConstraint(['dish_id'], ['dish.id'], ondelete='CASCADE'),
            sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('user_id', 'dish_id', name='dish_footprint_user_id_dish_id_key'),
            comment='用户浏览菜品足迹',
        )

    unique_names = {uc['name'] for uc in insp.get_unique_constraints('dish_footprint')}
    if 'dish_footprint_user_id_dish_id_key' not in unique_names:
        has_pair = any(
            set(uc['column_names']) == {'user_id', 'dish_id'}
            for uc in insp.get_unique_constraints('dish_footprint')
        )
        if not has_pair:
            op.create_unique_constraint(
                'dish_footprint_user_id_dish_id_key',
                'dish_footprint',
                ['user_id', 'dish_id'],
            )

    index_names = {idx['name'] for idx in insp.get_indexes('dish_footprint')}
    if FOOTPRINT_INDEX not in index_names:
        op.create_index(FOOTPRINT_INDEX, 'dish_footprint', ['user_id', 'viewed_at'], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)

    if insp.has_table('dish_footprint'):
        index_names = {idx['name'] for idx in insp.get_indexes('dish_footprint')}
        if FOOTPRINT_INDEX in index_names:
            op.drop_index(FOOTPRINT_INDEX, table_name='dish_footprint')
        op.drop_table('dish_footprint')
