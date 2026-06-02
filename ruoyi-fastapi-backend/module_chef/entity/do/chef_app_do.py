from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship

from config.database import Base


class AppUser(Base):
    """C 端用户（对应 Prisma model User）"""

    __tablename__ = 'user'
    __table_args__ = {'comment': 'C端用户表'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment='用户ID')
    email = Column(String(255), nullable=False, unique=True, comment='邮箱')
    password = Column(String(255), nullable=False, comment='密码')
    salt = Column(String(255), nullable=False, comment='密码盐')
    avatar_url = Column(String(512), nullable=True, comment='头像URL')
    nickname = Column(String(32), nullable=True, comment='昵称')
    like_count = Column(Integer, nullable=False, default=0, comment='获赞总数')

    dishes = relationship('AppDish', back_populates='user')
    chat_messages = relationship('AppAgentChatMessage', back_populates='user')
    dish_footprints = relationship('AppDishFootprint', back_populates='user')


class AppDish(Base):
    """菜品（对应 Prisma model Dish）"""

    __tablename__ = 'dish'
    __table_args__ = {'comment': '菜品表'}

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment='菜品ID')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, comment='用户ID')
    image_url = Column(ARRAY(Text), nullable=False, comment='图片URL列表')
    title = Column(String(255), nullable=True, comment='标题')
    content = Column(Text, nullable=False, comment='内容')
    like_count = Column(Integer, nullable=False, default=0, comment='点赞数')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')

    user = relationship('AppUser', back_populates='dishes')
    footprints = relationship('AppDishFootprint', back_populates='dish')


class AppDishFootprint(Base):
    """用户浏览菜品足迹（LRU 上限由业务层控制）"""

    __tablename__ = 'dish_footprint'
    __table_args__ = (
        UniqueConstraint('user_id', 'dish_id', name='dish_footprint_user_id_dish_id_key'),
        {'comment': '用户浏览菜品足迹'},
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment='足迹ID')
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    dish_id = Column(Integer, ForeignKey('dish.id', ondelete='CASCADE'), nullable=False, comment='菜品ID')
    viewed_at = Column(DateTime, nullable=False, default=datetime.now, comment='最近浏览时间')

    user = relationship('AppUser', back_populates='dish_footprints')
    dish = relationship('AppDish', back_populates='footprints')


class AppChatSession(Base):
    """聊天会话（对应 Prisma model ChatSession）"""

    __tablename__ = 'chat_session'
    __table_args__ = {'comment': '聊天会话表'}

    id = Column(UUID(as_uuid=False), primary_key=True, nullable=False, comment='会话ID')
    user_id = Column(Integer, nullable=False, comment='用户ID')
    title = Column(String(255), nullable=True, comment='会话标题')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    messages = relationship('AppAgentChatMessage', back_populates='session')


class AppAgentChatMessage(Base):
    """Agent 聊天消息（对应 Prisma model AgentChatMessage）"""

    __tablename__ = 'agent_chat_message'
    __table_args__ = {'comment': 'Agent聊天消息表'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='消息ID')
    session_id = Column(
        UUID(as_uuid=False),
        ForeignKey('chat_session.id'),
        nullable=False,
        index=True,
        comment='会话ID',
    )
    payload = Column(JSONB, nullable=False, comment='消息内容')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, comment='用户ID')

    session = relationship('AppChatSession', back_populates='messages')
    user = relationship('AppUser', back_populates='chat_messages')
