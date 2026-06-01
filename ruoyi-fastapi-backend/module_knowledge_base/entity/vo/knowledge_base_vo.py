from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class KnowledgeBaseModel(BaseModel):
    """
    知识库文件表对应 pydantic 模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='文件ID')
    filename: str | None = Field(default=None, description='文件名')
    filepath: str | None = Field(default=None, description='文件路径')
    filetype: str | None = Field(default=None, description='文件类型')
    filesize: int | None = Field(default=None, description='文件大小')
    md5: str | None = Field(default=None, description='md5值')
    create_by: str | None = Field(default=None, description='创建者')
    create_time: datetime | None = Field(default=None, description='创建时间')
    update_by: str | None = Field(default=None, description='更新者')
    update_time: datetime | None = Field(default=None, description='更新时间')


class KnowledgeBasePageQueryModel(KnowledgeBaseModel):
    """
    知识库文件分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteKnowledgeBaseModel(BaseModel):
    """
    删除知识库文件模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的文件ID')


class UpdateKnowledgeBaseModel(BaseModel):
    """
    通过已有 filepath 更新知识库
    """

    model_config = ConfigDict(alias_generator=to_camel)

    filepath: str = Field(description='文件访问路径或本地路径')
