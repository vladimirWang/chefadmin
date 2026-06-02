from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class DishModel(BaseModel):
    """系统文章（dish 表）"""

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: int | None = Field(default=None, description='文章ID')
    user_id: int | None = Field(default=None, description='发布用户ID')
    image_url: list[str] = Field(default_factory=list, description='封面图URL列表')
    title: str | None = Field(default=None, description='标题')
    content: str | None = Field(default=None, description='正文')
    like_count: int | None = Field(default=0, description='点赞数')
    created_at: datetime | None = Field(default=None, description='创建时间')
    updated_at: datetime | None = Field(default=None, description='更新时间')
    deleted_at: datetime | None = Field(default=None, description='删除时间')


class DishPageQueryModel(DishModel):
    """分页查询"""

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDishModel(BaseModel):
    """批量删除"""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    ids: str = Field(description='文章ID，多个以逗号分隔')
