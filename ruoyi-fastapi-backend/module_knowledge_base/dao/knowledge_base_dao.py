from pathlib import Path
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_knowledge_base.entity.do.knowledge_base_do import KnowledgeBase
from module_knowledge_base.entity.vo.knowledge_base_vo import KnowledgeBasePageQueryModel
from utils.log_util import logger
from utils.page_util import PageUtil
from utils.reader import basename_from_filepath


class KnowledgeBaseDao:
    @classmethod
    async def check_knowledge_existed(cls, db: AsyncSession, md5_value: str) -> bool:
        existed = (
            await db.execute(select(KnowledgeBase).where(KnowledgeBase.md5 == md5_value))
        ).scalars().first()
        logger.info('check_knowledge_existed md5=%s existed=%s', md5_value, existed is not None)
        return existed is not None

    @classmethod
    async def get_knowledge_list(
        cls, db: AsyncSession, query_object: KnowledgeBasePageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        query = (
            select(KnowledgeBase)
            .where(
                KnowledgeBase.filename.like(f'%{query_object.filename}%') if query_object.filename else True,
                KnowledgeBase.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
            )
            .order_by(KnowledgeBase.id.desc())
            .distinct()
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def add_knowledge_base_dao(
        cls,
        db: AsyncSession,
        *,
        filename: str,
        filepath: str,
        filetype: str,
        filesize: int,
        md5_value: str,
        create_by: str | None = None,
    ) -> KnowledgeBase:
        db_knowledge_base = KnowledgeBase(
            filename=filename,
            filepath=filepath,
            filetype=filetype[:10],
            filesize=filesize,
            md5=md5_value,
            create_by=create_by or '',
            update_by=create_by or '',
        )
        db.add(db_knowledge_base)
        await db.flush()
        return db_knowledge_base

    @classmethod
    async def add_knowledge_from_bytes(
        cls,
        db: AsyncSession,
        filepath: str,
        md5_value: str,
        raw: bytes,
        create_by: str | None = None,
    ) -> KnowledgeBase:
        filename = basename_from_filepath(filepath)
        suffix = Path(filename).suffix.lstrip('.') or 'txt'
        logger.info(
            'UpdateKnowledge Read %d bytes from filepath, preview: %r',
            len(raw),
            raw[:100],
        )
        return await cls.add_knowledge_base_dao(
            db,
            filename=filename,
            filepath=filepath,
            filetype=suffix,
            filesize=len(raw),
            md5_value=md5_value,
            create_by=create_by,
        )

    @classmethod
    async def delete_knowledge_base_dao(cls, db: AsyncSession, knowledge_id: int) -> None:
        await db.execute(delete(KnowledgeBase).where(KnowledgeBase.id == knowledge_id))
