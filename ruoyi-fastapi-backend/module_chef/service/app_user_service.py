from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_chef.dao.app_user_dao import AppUserDao
from module_chef.entity.vo.app_user_vo import AppUserModel, AppUserPageQueryModel, UpdateAppUserModel
from utils.common_util import CamelCaseUtil


class AppUserService:
    @classmethod
    async def get_user_list_services(
        cls, query_db: AsyncSession, query_object: AppUserPageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await AppUserDao.get_user_list(query_db, query_object, is_page)

    @classmethod
    async def get_user_detail_services(cls, query_db: AsyncSession, user_id: int) -> AppUserModel:
        user = await AppUserDao.get_user_by_id(query_db, user_id)
        if not user:
            return AppUserModel()
        data = CamelCaseUtil.transform_result(user)
        data['postCount'] = await AppUserDao.count_user_posts(query_db, user_id)
        return AppUserModel(**data)

    @classmethod
    async def update_user_services(
        cls, query_db: AsyncSession, page_object: UpdateAppUserModel
    ) -> CrudResponseModel:
        user = await AppUserDao.get_user_by_id(query_db, page_object.id)
        if not user:
            raise ServiceException(message='用户不存在')
        try:
            await AppUserDao.update_user_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def like_dish_services(cls, query_db: AsyncSession, dish_id: int) -> CrudResponseModel:
        try:
            dish = await AppUserDao.increment_dish_like_count(query_db, dish_id, delta=1)
            if not dish:
                raise ServiceException(message='文章不存在或已删除')
            await AppUserDao.increment_user_like_count(query_db, dish.user_id, delta=1)
            await query_db.commit()
            return CrudResponseModel(
                is_success=True,
                message='点赞成功',
                result={'dishLikeCount': dish.like_count},
            )
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e
