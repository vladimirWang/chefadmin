"""add dish_footprint user_id+dish_id unique constraint

Revision ID: g7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-06-03 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import inspect


revision: str = 'g7b8c9d0e1f2'
down_revision: Union[str, Sequence[str], None] = 'f6a7b8c9d0e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

UNIQUE_NAME = 'dish_footprint_user_id_dish_id_key'


def _has_user_dish_unique(insp, table: str) -> bool:
    if not insp.has_table(table):
        return True
    for uc in insp.get_unique_constraints(table):
        if set(uc['column_names']) == {'user_id', 'dish_id'}:
            return True
    return False


def upgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)

    if _has_user_dish_unique(insp, 'dish_footprint'):
        return

    op.create_unique_constraint(
        UNIQUE_NAME,
        'dish_footprint',
        ['user_id', 'dish_id'],
    )


def downgrade() -> None:
    bind = op.get_bind()
    insp = inspect(bind)

    if not insp.has_table('dish_footprint'):
        return

    uq_names = {uc['name'] for uc in insp.get_unique_constraints('dish_footprint')}
    if UNIQUE_NAME in uq_names:
        op.drop_constraint(UNIQUE_NAME, 'dish_footprint', type_='unique')
