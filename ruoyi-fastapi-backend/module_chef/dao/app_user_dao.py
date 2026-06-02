from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_chef.entity.do.chef_app_do import AppDish, AppUser
from module_chef.entity.vo.app_user_vo import AppUserPageQueryModel, UpdateAppUserModel
from utils.page_util import PageUtil


class AppUserDao:
    @classmethod
    async def get_user_by_id(cls, db: AsyncSession, user_id: int) -> AppUser | None:
        return (
            await db.execute(select(AppUser).where(AppUser.id == user_id))
        ).scalars().first()

    @classmethod
    async def count_user_posts(cls, db: AsyncSession, user_id: int) -> int:
        return (
            await db.execute(
                select(func.count())
                .select_from(AppDish)
                .where(AppDish.user_id == user_id, AppDish.deleted_at.is_(None))
            )
        ).scalar_one()

    @classmethod
    async def get_user_list(
        cls, db: AsyncSession, query_object: AppUserPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(AppUser)
            .where(AppUser.email.like(f'%{query_object.email}%') if query_object.email else True)
            .order_by(AppUser.id.desc())
            .distinct()
        )
        result = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        if not is_page:
            return result
        rows = []
        for row in result.rows:
            user_id = row.get('id')
            if user_id is not None:
                row['postCount'] = await cls.count_user_posts(db, user_id)
            rows.append(row)
        result.rows = rows
        return result

    @classmethod
    async def update_user_dao(cls, db: AsyncSession, page_object: UpdateAppUserModel) -> None:
        values: dict[str, Any] = {}
        if page_object.nickname is not None:
            values['nickname'] = page_object.nickname.strip() or None
        if page_object.avatar_url is not None:
            values['avatar_url'] = page_object.avatar_url.strip() or None
        if page_object.like_count is not None:
            values['like_count'] = max(0, page_object.like_count)
        if not values:
            return
        await db.execute(update(AppUser).where(AppUser.id == page_object.id).values(**values))

    @classmethod
    async def increment_user_like_count(cls, db: AsyncSession, user_id: int, delta: int = 1) -> None:
        user = await cls.get_user_by_id(db, user_id)
        if not user:
            return
        new_count = max(0, (user.like_count or 0) + delta)
        await db.execute(update(AppUser).where(AppUser.id == user_id).values(like_count=new_count))

    @classmethod
    async def increment_dish_like_count(cls, db: AsyncSession, dish_id: int, delta: int = 1) -> AppDish | None:
        dish = (
            await db.execute(
                select(AppDish).where(AppDish.id == dish_id, AppDish.deleted_at.is_(None))
            )
        ).scalars().first()
        if not dish:
            return None
        new_count = max(0, (dish.like_count or 0) + delta)
        await db.execute(update(AppDish).where(AppDish.id == dish_id).values(like_count=new_count))
        dish.like_count = new_count
        return dish
