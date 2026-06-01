import hashlib
import os
from datetime import datetime
from typing import Any

from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from config.env import UploadConfig
from exceptions.exception import ServiceException
from module_knowledge_base.dao.knowledge_base_dao import KnowledgeBaseDao
from module_knowledge_base.entity.vo.knowledge_base_vo import (
    DeleteKnowledgeBaseModel,
    KnowledgeBasePageQueryModel,
    UpdateKnowledgeBaseModel,
)
from module_knowledge_base.service.knowledge_vector_service import KnowledgeVectorService
from utils.reader import basename_from_filepath, read_filepath_bytes_sync
from utils.upload_util import UploadUtil


class KnowledgeBaseService:
    @classmethod
    async def get_knowledge_list_services(
        cls, query_db: AsyncSession, query_object: KnowledgeBasePageQueryModel, is_page: bool = True
    ) -> PageModel | list[dict[str, Any]]:
        return await KnowledgeBaseDao.get_knowledge_list(query_db, query_object, is_page)

    @classmethod
    async def upload_knowledge_services(
        cls, query_db: AsyncSession, request: Request, file: UploadFile, create_by: str
    ) -> CrudResponseModel:
        if not file.filename:
            raise ServiceException(message='请选择要上传的文件')
        if not UploadUtil.check_file_extension(file):
            raise ServiceException(message='文件类型不合法')

        content = await file.read()
        if not content:
            raise ServiceException(message='文件内容为空')

        md5_value = hashlib.md5(content).hexdigest()
        if await KnowledgeBaseDao.check_knowledge_existed(query_db, md5_value):
            raise ServiceException(message='文件已存在，请勿重复上传')

        relative_path = (
            f'knowledge/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%m")}/{datetime.now().strftime("%d")}'
        )
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        original_name = file.filename.rsplit('.', 1)[0]
        extension = file.filename.rsplit('.', 1)[-1]
        stored_name = (
            f'{original_name}_{datetime.now().strftime("%Y%m%d%H%M%S")}'
            f'{UploadConfig.UPLOAD_MACHINE}{UploadUtil.generate_random_number()}.{extension}'
        )
        stored_path = os.path.join(dir_path, stored_name)
        with open(stored_path, 'wb') as f:
            f.write(content)

        filepath = (
            f'{request.base_url}{UploadConfig.UPLOAD_PREFIX[1:]}/{relative_path}/{stored_name}'.rstrip('/')
        )
        filetype = extension[:10]

        try:
            await KnowledgeBaseDao.add_knowledge_base_dao(
                query_db,
                filename=file.filename,
                filepath=filepath,
                filetype=filetype,
                filesize=len(content),
                md5_value=md5_value,
                create_by=create_by,
            )
            vector_message = await KnowledgeVectorService.index_file_content(
                content, file.filename, create_by
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'上传成功；{vector_message}')
        except Exception as e:
            await query_db.rollback()
            if os.path.exists(stored_path):
                os.remove(stored_path)
            raise e

    @classmethod
    async def update_knowledge_by_filepath_services(
        cls, query_db: AsyncSession, page_object: UpdateKnowledgeBaseModel, create_by: str
    ) -> CrudResponseModel:
        filepath = (page_object.filepath or '').strip()
        if not filepath:
            raise ServiceException(message='filepath 不能为空')

        raw = read_filepath_bytes_sync(filepath)
        md5_value = hashlib.md5(raw).hexdigest()
        if await KnowledgeBaseDao.check_knowledge_existed(query_db, md5_value):
            return CrudResponseModel(is_success=True, message='文件已存在')

        filename = basename_from_filepath(filepath)
        try:
            await KnowledgeBaseDao.add_knowledge_from_bytes(
                query_db, filepath, md5_value, raw, create_by=create_by
            )
            vector_message = await KnowledgeVectorService.index_file_content(raw, filename, create_by)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message=f'更新成功；{vector_message}')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_knowledge_services(
        cls, query_db: AsyncSession, page_object: DeleteKnowledgeBaseModel
    ) -> CrudResponseModel:
        if not page_object.ids:
            raise ServiceException(message='传入文件 id 为空')

        try:
            removed_total = 0
            for knowledge_id in page_object.ids.split(','):
                kid = int(knowledge_id)
                record = await KnowledgeBaseDao.get_knowledge_by_id(query_db, kid)
                if record is None:
                    continue
                removed_total += await KnowledgeVectorService.delete_by_filename(record.filename)
                await KnowledgeBaseDao.delete_knowledge_base_dao(query_db, kid)
            await query_db.commit()
            message = '删除成功'
            if removed_total:
                message = f'删除成功；已清理 {removed_total} 条向量'
            return CrudResponseModel(is_success=True, message=message)
        except Exception as e:
            await query_db.rollback()
            raise e
