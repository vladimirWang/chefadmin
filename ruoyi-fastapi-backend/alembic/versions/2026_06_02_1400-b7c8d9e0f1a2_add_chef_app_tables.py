"""add chef app tables (user, dish, chat_session, agent_chat_message)

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2026-06-02 14:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = 'b7c8d9e0f1a2'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='用户ID'),
        sa.Column('email', sa.String(length=255), nullable=False, comment='邮箱'),
        sa.Column('password', sa.String(length=255), nullable=False, comment='密码'),
        sa.Column('salt', sa.String(length=255), nullable=False, comment='密码盐'),
        sa.PrimaryKeyConstraint('id'),
        comment='C端用户表',
    )
    op.create_index('user_email_key', 'user', ['email'], unique=True)

    op.create_table(
        'dish',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='菜品ID'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('image_url', postgresql.ARRAY(sa.Text()), nullable=False, comment='图片URL列表'),
        sa.Column('title', sa.String(length=255), nullable=True, comment='标题'),
        sa.Column('content', sa.Text(), nullable=False, comment='内容'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='删除时间'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        comment='菜品表',
    )
    op.create_index('dish_user_id_idx', 'dish', ['user_id'], unique=False)

    op.create_table(
        'chat_session',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False, comment='会话ID'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('title', sa.String(length=255), nullable=True, comment='会话标题'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='聊天会话表',
    )

    op.create_table(
        'agent_chat_message',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='消息ID'),
        sa.Column('session_id', postgresql.UUID(as_uuid=False), nullable=False, comment='会话ID'),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False, comment='消息内容'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='更新时间'),
        sa.Column('deleted_at', sa.DateTime(), nullable=True, comment='删除时间'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.ForeignKeyConstraint(['session_id'], ['chat_session.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id'),
        comment='Agent聊天消息表',
    )
    op.create_index('agent_chat_message_session_id_idx', 'agent_chat_message', ['session_id'], unique=False)
    op.create_index('agent_chat_message_user_id_idx', 'agent_chat_message', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('agent_chat_message_user_id_idx', table_name='agent_chat_message')
    op.drop_index('agent_chat_message_session_id_idx', table_name='agent_chat_message')
    op.drop_table('agent_chat_message')
    op.drop_table('chat_session')
    op.drop_index('dish_user_id_idx', table_name='dish')
    op.drop_table('dish')
    op.drop_index('user_email_key', table_name='user')
    op.drop_table('user')
