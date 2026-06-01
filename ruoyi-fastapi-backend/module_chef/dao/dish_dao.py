from datetime import datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_chef.entity.do.chef_app_do import AppDish
from module_chef.entity.vo.dish_vo import DishModel, DishPageQueryModel
from utils.page_util import PageUtil


class DishDao:
    @classmethod
    async def get_dish_by_id(cls, db: AsyncSession, dish_id: int) -> AppDish | None:
        return (
            await db.execute(
                select(AppDish).where(AppDish.id == dish_id, AppDish.deleted_at.is_(None))
            )
        ).scalars().first()

    @classmethod
    async def get_dish_list(
        cls, db: AsyncSession, query_object: DishPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(AppDish)
            .where(
                AppDish.deleted_at.is_(None),
                AppDish.title.like(f'%{query_object.title}%') if query_object.title else True,
            )
            .order_by(AppDish.id.desc())
            .distinct()
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def add_dish_dao(cls, db: AsyncSession, dish: DishModel) -> AppDish:
        now = datetime.now()
        db_dish = AppDish(
            user_id=dish.user_id,
            image_url=dish.image_url or [],
            title=dish.title,
            content=dish.content or '',
            created_at=now,
            updated_at=now,
        )
        db.add(db_dish)
        await db.flush()
        return db_dish

    @classmethod
    async def edit_dish_dao(cls, db: AsyncSession, dish_id: int, dish: DishModel) -> None:
        values: dict[str, Any] = {'updated_at': datetime.now()}
        if dish.title is not None:
            values['title'] = dish.title
        if dish.content is not None:
            values['content'] = dish.content
        if dish.image_url is not None:
            values['image_url'] = dish.image_url
        await db.execute(update(AppDish).where(AppDish.id == dish_id).values(**values))

    @classmethod
    async def soft_delete_dish_dao(cls, db: AsyncSession, dish_id: int) -> None:
        await db.execute(
            update(AppDish)
            .where(AppDish.id == dish_id, AppDish.deleted_at.is_(None))
            .values(deleted_at=datetime.now(), updated_at=datetime.now())
        )
