from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from module_chef.entity.do.chef_app_do import AppUser

SYSTEM_USER_EMAIL = 'system@private-chef.local'


class SystemUserDao:
    @classmethod
    async def get_or_create_system_user_id(cls, db: AsyncSession) -> int:
        """管理员推送文章使用的系统账号（满足 dish.user_id 外键）。"""
        user = (
            await db.execute(select(AppUser).where(AppUser.email == SYSTEM_USER_EMAIL))
        ).scalars().first()
        if user:
            return user.id

        user = AppUser(email=SYSTEM_USER_EMAIL, password='-', salt='-')
        db.add(user)
        await db.flush()
        return user.id
