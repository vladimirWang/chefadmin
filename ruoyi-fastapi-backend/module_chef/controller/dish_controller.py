from typing import Annotated

from fastapi import Path, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import PreAuthDependency
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_chef.entity.vo.dish_vo import DeleteDishModel, DishModel, DishPageQueryModel
from module_chef.service.dish_service import DishService
from utils.log_util import logger
from utils.response_util import ResponseUtil

dish_controller = APIRouterPro(
    prefix='/chef/dish',
    order_num=9,
    tags=['私厨-系统文章'],
    dependencies=[PreAuthDependency()],
)


@dish_controller.get(
    '/list',
    summary='系统文章分页列表',
    response_model=PageResponseModel[DishModel],
    dependencies=[UserInterfaceAuthDependency('chef:dish:list')],
)
async def get_dish_list(
    request: Request,
    query: Annotated[DishPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    page_result = await DishService.get_dish_list_services(query_db, query, is_page=True)
    logger.info('获取系统文章列表成功')
    return ResponseUtil.success(model_content=page_result)


@dish_controller.get(
    '/{dish_id}',
    summary='系统文章详情',
    response_model=DataResponseModel[DishModel],
    dependencies=[UserInterfaceAuthDependency('chef:dish:query')],
)
async def get_dish_detail(
    request: Request,
    dish_id: Annotated[int, Path(description='文章ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    detail = await DishService.dish_detail_services(query_db, dish_id)
    logger.info('获取系统文章详情成功 id=%s', dish_id)
    return ResponseUtil.success(data=detail)


@dish_controller.post(
    '',
    summary='发布系统文章',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('chef:dish:add')],
)
async def add_dish(
    request: Request,
    body: DishModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await DishService.add_dish_services(query_db, body)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@dish_controller.put(
    '',
    summary='编辑系统文章',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('chef:dish:edit')],
)
async def edit_dish(
    request: Request,
    body: DishModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await DishService.edit_dish_services(query_db, body)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@dish_controller.delete(
    '/{ids}',
    summary='删除系统文章（软删）',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('chef:dish:remove')],
)
async def delete_dish(
    request: Request,
    ids: Annotated[str, Path(description='文章ID，多个以逗号分隔')],
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    result = await DishService.delete_dish_services(query_db, DeleteDishModel(ids=ids))
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)
