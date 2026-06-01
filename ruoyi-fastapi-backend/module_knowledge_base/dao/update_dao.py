from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from module_knowledge_base.entity.do.knowledge_base_do import KnowledgeBase
from utils.log_util import logger
from utils.reader import basename_from_filepath


class UpdateDao:
    @classmethod
    async def check_knowledge_existed(cls, db: AsyncSession, md5_value: str) -> bool:
        existed = (
            await db.execute(select(KnowledgeBase).where(KnowledgeBase.md5 == md5_value))
        ).scalars().first()
        logger.info('check_knowledge_existed md5=%s existed=%s', md5_value, existed is not None)
        return existed is not None

    @classmethod
    async def update_knowledge_base_dao(cls, db: AsyncSession, filepath: str, md5_value: str, raw: bytes) -> str:
        logger.info(
            'UpdateKnowledge Read %d bytes from filepath, preview: %r',
            len(raw),
            raw[:100],
        )
        filename = basename_from_filepath(filepath)
        suffix = Path(filename).suffix.lstrip('.') or 'txt'

        db_knowledge_base = KnowledgeBase(
            filename=filename,
            filepath=filepath,
            filetype=suffix[:10],
            filesize=len(raw),
            md5=md5_value,
        )
        db.add(db_knowledge_base)
        await db.flush()

        return f'success: {filename}'