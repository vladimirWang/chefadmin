from datetime import datetime

from sqlalchemy import CHAR, Column, DateTime, Integer, LargeBinary, String, BigInteger
from sqlalchemy.dialects import mysql

from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil

class KnowledgeBase(Base):
    """
    用户与岗位关联表
    """

    __tablename__ = 'knowledge_base'
    __table_args__ = {'comment': '知识库表'}

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='文件ID')
    filename = Column(String(100), nullable=False, comment='文件名')
    filepath = Column(String(200), nullable=False, comment='文件路径')
    filetype = Column(String(10), nullable=False, comment='文件类型')
    filesize = Column(BigInteger, nullable=False, comment='文件大小')
    md5 = Column(String(32), nullable=False, comment='md5值')
    create_by = Column(String(64), nullable=True, server_default="''", comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), nullable=True, server_default="''", comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')

# model KnowledgeFile {
#   id Int @id @default(autoincrement())
#   filename String
#   filepath String @unique
#   filetype String
#   filesize Int
#   md5 String @unique
#   createdAt DateTime @default(now())
#   updatedAt DateTime @updatedAt
#   deletedAt DateTime?
# }