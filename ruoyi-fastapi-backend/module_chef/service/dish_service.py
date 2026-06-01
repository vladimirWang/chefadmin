from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_chef.dao.dish_dao import DishDao
from module_chef.dao.system_user_dao import SystemUserDao
from module_chef.entity.vo.dish_vo import DeleteDishModel, DishModel, DishPageQueryModel
from utils.common_util import CamelCaseUtil


class DishService:
    @classmethod
    def _validate_write_payload(cls, page_object: DishModel, *, is_create: bool) -> None:
        content = (page_object.content or '').strip()
        if not content:
            raise ServiceException(message='文章正文不能为空')
        page_object.content = content

        image_urls = [u.strip() for u in (page_object.image_url or []) if u and u.strip()]
        if is_create and not image_urls:
            raise ServiceException(message='请至少上传一张封面图')
        page_object.image_url = image_urls

        if page_object.title is not None:
            page_object.title = page_object.title.strip() or None

    @classmethod
    async def get_dish_list_services(
        cls, query_db: AsyncSession, query_object: DishPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await DishDao.get_dish_list(query_db, query_object, is_page)

    @classmethod
    async def dish_detail_services(cls, query_db: AsyncSession, dish_id: int) -> DishModel:
        dish = await DishDao.get_dish_by_id(query_db, dish_id)
        if not dish:
            return DishModel()
        return DishModel(**CamelCaseUtil.transform_result(dish))

    @classmethod
    async def add_dish_services(cls, query_db: AsyncSession, page_object: DishModel) -> CrudResponseModel:
        cls._validate_write_payload(page_object, is_create=True)
        try:
            page_object.user_id = await SystemUserDao.get_or_create_system_user_id(query_db)
            await DishDao.add_dish_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='发布成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_dish_services(cls, query_db: AsyncSession, page_object: DishModel) -> CrudResponseModel:
        if page_object.id is None:
            raise ServiceException(message='文章ID不能为空')
        existing = await DishDao.get_dish_by_id(query_db, page_object.id)
        if not existing:
            raise ServiceException(message='文章不存在或已删除')
        cls._validate_write_payload(page_object, is_create=False)
        if not page_object.image_url:
            page_object.image_url = list(existing.image_url or [])
        try:
            await DishDao.edit_dish_dao(query_db, page_object.id, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_dish_services(
        cls, query_db: AsyncSession, page_object: DeleteDishModel
    ) -> CrudResponseModel:
        if not page_object.ids:
            raise ServiceException(message='传入文章 id 为空')
        try:
            for dish_id in page_object.ids.split(','):
                kid = int(dish_id.strip())
                if not await DishDao.get_dish_by_id(query_db, kid):
                    continue
                await DishDao.soft_delete_dish_dao(query_db, kid)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e
