from typing import Annotated

from fastapi import Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_chef.entity.vo.app_user_vo import AppUserModel, AppUserPageQueryModel, UpdateAppUserModel
from module_chef.service.app_user_service import AppUserService
from utils.log_util import logger
from utils.response_util import ResponseUtil

app_user_controller = APIRouterPro(
    prefix='/chef/appUser',
    order_num=10,
    tags=['私厨-C端用户'],
    dependencies=[PreAuthDependency()],
)


@app_user_controller.get(
    '/list',
    summary='C端用户分页列表',
    response_model=PageResponseModel[AppUserModel],
    dependencies=[UserInterfaceAuthDependency('chef:appUser:list')],
)
async def get_app_user_list(
    request: Request,
    query: Annotated[AppUserPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    page_result = await AppUserService.get_user_list_services(query_db, query, is_page=True)
    return ResponseUtil.success(model_content=page_result)


@app_user_controller.get(
    '/{user_id}',
    summary='C端用户详情',
    response_model=DataResponseModel[AppUserModel],
    dependencies=[UserInterfaceAuthDependency('chef:appUser:query')],
)
async def get_app_user_detail(
    request: Request,
    user_id: Annotated[int, Path(description='用户ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    detail = await AppUserService.get_user_detail_services(query_db, user_id)
    return ResponseUtil.success(data=detail)


@app_user_controller.put(
    '',
    summary='更新C端用户（头像/获赞数）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('chef:appUser:edit')],
)
async def update_app_user(
    request: Request,
    body: UpdateAppUserModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await AppUserService.update_user_services(query_db, body)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)
