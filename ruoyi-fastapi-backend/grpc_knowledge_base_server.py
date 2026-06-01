"""供 private_chef_server 调用的 gRPC：KnowledgeService/Update 更新知识库。"""

import asyncio
import hashlib
import logging
import os
import threading
from concurrent import futures

import grpc

from config.database import AsyncSessionLocal
from grpc_generated import knowledge_base_pb2, knowledge_base_pb2_grpc
from module_knowledge_base.dao.knowledge_base_dao import KnowledgeBaseDao
from module_knowledge_base.service.knowledge_vector_service import KnowledgeVectorService
from utils.reader import basename_from_filepath, read_filepath_bytes_sync

logger = logging.getLogger('ruoyi.knowledge_base.grpc')


async def _update_knowledge_base(filepath: str) -> str:
    raw = read_filepath_bytes_sync(filepath)
    md5_value = hashlib.md5(raw).hexdigest()

    async with AsyncSessionLocal() as db:
        try:
            if await KnowledgeBaseDao.check_knowledge_existed(db, md5_value):
                return '文件已存在'

            filename = basename_from_filepath(filepath)
            await KnowledgeBaseDao.add_knowledge_from_bytes(db, filepath, md5_value, raw)
            vector_message = await KnowledgeVectorService.index_file_content(raw, filename)
            await db.commit()
            return f'success: {filename}；{vector_message}'
        except Exception:
            await db.rollback()
            raise


class KnowledgeBaseServicer(knowledge_base_pb2_grpc.KnowledgeServiceServicer):
    pass


def _build_knowledge_base_server() -> tuple[grpc.Server, str]:
    port = os.environ.get('CHEFADMIN_KNOWLEDGE_BASE_GRPC_PORT', '50053')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    knowledge_base_pb2_grpc.add_KnowledgeServiceServicer_to_server(KnowledgeBaseServicer(), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    return server, listen_addr


def start_knowledge_base_grpc_in_thread() -> grpc.Server:
    """在同进程内启动 gRPC；后台线程 wait_for_termination，主线程立即返回供 FastAPI lifespan yield。"""
    server, listen_addr = _build_knowledge_base_server()
    server.start()
    logger.info('KnowledgeService gRPC listening on %s', listen_addr)
    threading.Thread(
        target=server.wait_for_termination,
        name='grpc-KnowledgeBase',
        daemon=True,
    ).start()
    return server


def serve() -> None:
    server, listen_addr = _build_knowledge_base_server()
    server.start()
    logger.info('KnowledgeService gRPC listening on %s', listen_addr)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
