"""seed home page dish feed demo data

Revision ID: c3d4e5f6a7b8
Revises: 5e687dcaacd1
Create Date: 2026-06-03 10:00:00.000000

"""
from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = '5e687dcaacd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SYSTEM_USER_EMAIL = 'system@private-chef.local'

SEED_DISHES = [
    {
        'title': '低脂鸡胸肉轻食沙拉',
        'content': '减脂期必备餐食，饱腹无负担\n#美食',
        'image_url': ['https://picsum.photos/id/292/400/520'],
    },
    {
        'title': '居家平板支撑训练',
        'content': '核心力量训练，每天5分钟塑形\n#健身',
        'image_url': ['https://picsum.photos/id/176/400/600'],
    },
    {
        'title': '全麦粗粮早餐吐司',
        'content': '低卡高纤维，健康早餐首选\n#美食',
        'image_url': ['https://picsum.photos/id/431/400/480'],
    },
    {
        'title': '户外慢跑有氧锻炼',
        'content': '燃脂瘦身，提升身体代谢\n#健身',
        'image_url': ['https://picsum.photos/id/119/400/550'],
    },
    {
        'title': '新鲜果蔬减脂果盘',
        'content': '维生素满满，清爽解腻\n#美食',
        'image_url': ['https://picsum.photos/id/106/400/500'],
    },
    {
        'title': '哑铃手臂力量训练',
        'content': '打造紧致手臂线条\n#健身',
        'image_url': ['https://picsum.photos/id/342/400/620'],
    },
    {
        'title': '无糖燕麦代餐粥',
        'content': '饱腹代餐，懒人减脂好物\n#美食',
        'image_url': ['https://picsum.photos/id/493/400/460'],
    },
    {
        'title': '瑜伽拉伸放松体态',
        'content': '舒缓肌肉，改善驼背\n#健身',
        'image_url': ['https://picsum.photos/id/613/400/580'],
    },
]


def upgrade() -> None:
    conn = op.get_bind()
    now = datetime.now()

    user_id = conn.execute(
        sa.text('SELECT id FROM "user" WHERE email = :email LIMIT 1'),
        {'email': SYSTEM_USER_EMAIL},
    ).scalar()
    if user_id is None:
        user_id = conn.execute(
            sa.text(
                'INSERT INTO "user" (email, password, salt) '
                'VALUES (:email, :password, :salt) RETURNING id'
            ),
            {'email': SYSTEM_USER_EMAIL, 'password': '-', 'salt': '-'},
        ).scalar()

    dish_table = sa.table(
        'dish',
        sa.column('user_id', sa.Integer),
        sa.column('image_url', postgresql.ARRAY(sa.Text)),
        sa.column('title', sa.String),
        sa.column('content', sa.Text),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
        sa.column('deleted_at', sa.DateTime),
    )

    for item in SEED_DISHES:
        exists = conn.execute(
            sa.text(
                'SELECT 1 FROM dish WHERE title = :title AND deleted_at IS NULL LIMIT 1'
            ),
            {'title': item['title']},
        ).scalar()
        if exists:
            continue
        conn.execute(
            dish_table.insert().values(
                user_id=user_id,
                image_url=item['image_url'],
                title=item['title'],
                content=item['content'],
                created_at=now,
                updated_at=now,
                deleted_at=None,
            )
        )


def downgrade() -> None:
    titles = [item['title'] for item in SEED_DISHES]
    conn = op.get_bind()
    for title in titles:
        conn.execute(
            sa.text('DELETE FROM dish WHERE title = :title'),
            {'title': title},
        )
