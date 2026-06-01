from typing import Annotated

from fastapi import File, Path, Query, Request, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.router import APIRouterPro
from common.vo import PageResponseModel, ResponseBaseModel
from module_knowledge_base.entity.vo.knowledge_base_vo import (
    DeleteKnowledgeBaseModel,
    KnowledgeBaseModel,
    KnowledgeBasePageQueryModel,
    UpdateKnowledgeBaseModel,
)
from module_knowledge_base.service.knowledge_base_service import KnowledgeBaseService
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.log_util import logger
from utils.response_util import ResponseUtil

knowledge_base_controller = APIRouterPro(
    prefix='/knowledgeBase',
    order_num=8,
    tags=['知识库管理'],
    dependencies=[PreAuthDependency()],
)


@knowledge_base_controller.get(
    '/list',
    summary='获取知识库文件分页列表',
    response_model=PageResponseModel[KnowledgeBaseModel],
    dependencies=[UserInterfaceAuthDependency('knowledgeBase:list')],
)
async def get_knowledge_base_list(
    request: Request,
    query: Annotated[KnowledgeBasePageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    page_result = await KnowledgeBaseService.get_knowledge_list_services(query_db, query, is_page=True)
    logger.info('获取知识库列表成功')
    return ResponseUtil.success(model_content=page_result)


@knowledge_base_controller.post(
    '/upload',
    summary='上传知识库文件',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('knowledgeBase:upload')],
)
async def upload_knowledge_base_file(
    request: Request,
    file: Annotated[UploadFile, File(...)],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    upload_result = await KnowledgeBaseService.upload_knowledge_services(
        query_db, request, file, current_user.user.user_name
    )
    logger.info(upload_result.message)
    return ResponseUtil.success(msg=upload_result.message)


@knowledge_base_controller.post(
    '/update',
    summary='通过 filepath 更新知识库',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('knowledgeBase:update')],
)
async def update_knowledge_base_by_filepath(
    request: Request,
    body: UpdateKnowledgeBaseModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    update_result = await KnowledgeBaseService.update_knowledge_by_filepath_services(
        query_db, body, current_user.user.user_name
    )
    logger.info(update_result.message)
    return ResponseUtil.success(msg=update_result.message)


@knowledge_base_controller.delete(
    '/{ids}',
    summary='删除知识库文件记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('knowledgeBase:remove')],
)
async def delete_knowledge_base(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的文件ID，多个以逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_result = await KnowledgeBaseService.delete_knowledge_services(
        query_db, DeleteKnowledgeBaseModel(ids=ids)
    )
    logger.info(delete_result.message)
    return ResponseUtil.success(msg=delete_result.message)
