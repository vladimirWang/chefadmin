import asyncio
import os

from agents.knowledge_base import KnowledgeBase
from exceptions.exception import ServiceException
from utils.log_util import logger
from utils.reader import basename_from_filepath


class KnowledgeVectorService:
    @classmethod
    def _ensure_dashscope_api_key(cls) -> None:
        if not os.getenv('DASHSCOPE_API_KEY'):
            raise ServiceException(message='未配置 DASHSCOPE_API_KEY，无法更新向量库')

    @classmethod
    async def index_file_content(cls, content: bytes, filename: str, operator: str = 'system') -> str:
        """
        将文件文本内容写入 PGVector 向量库（同步 embedding 逻辑在线程池中执行）。
        """
        cls._ensure_dashscope_api_key()
        text = content.decode('utf-8', errors='replace')
        if not text.strip():
            raise ServiceException(message='文件内容无法解析为文本，无法更新向量库')

        def _index() -> str:
            return KnowledgeBase().upload_by_str(text, filename=filename, operator=operator)

        try:
            message = await asyncio.to_thread(_index)
        except ServiceException:
            raise
        except Exception as e:
            logger.exception('Knowledge vector index failed filename=%s', filename)
            raise ServiceException(message=f'向量库更新失败: {e}') from e

        logger.info('Knowledge vector indexed filename=%s message=%s', filename, message)
        return message

    @classmethod
    async def delete_by_filename(cls, filename: str) -> int:
        """删除与文件名对应的向量片段（无需调用 embedding API）。"""

        def _delete() -> int:
            return KnowledgeBase().delete_by_filename(filename)

        try:
            removed = await asyncio.to_thread(_delete)
        except Exception as e:
            logger.exception('Knowledge vector delete failed filename=%s', filename)
            raise ServiceException(message=f'向量库删除失败: {e}') from e

        logger.info('Knowledge vector deleted filename=%s removed=%s', filename, removed)
        return removed

    @classmethod
    async def index_filepath(cls, filepath: str, operator: str = 'system') -> str:
        from utils.reader import read_filepath_bytes_sync

        raw = read_filepath_bytes_sync(filepath)
        filename = basename_from_filepath(filepath)
        return await cls.index_file_content(raw, filename, operator)
