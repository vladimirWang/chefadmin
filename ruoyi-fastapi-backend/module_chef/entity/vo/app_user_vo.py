from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class AppUserModel(BaseModel):
    """C 端用户"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: int | None = Field(default=None, description='用户ID')
    email: str | None = Field(default=None, description='邮箱')
    nickname: str | None = Field(default=None, description='昵称')
    avatar_url: str | None = Field(default=None, description='头像URL')
    like_count: int | None = Field(default=0, description='获赞总数')
    post_count: int | None = Field(default=0, description='发帖数')
    created_at: datetime | None = Field(default=None, description='注册时间')


class AppUserPageQueryModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    email: str | None = Field(default=None, description='邮箱')
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class UpdateAppUserModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    id: int = Field(description='用户ID')
    nickname: str | None = Field(default=None, description='昵称')
    avatar_url: str | None = Field(default=None, description='头像URL')
    like_count: int | None = Field(default=None, description='获赞总数（管理员可调）')
