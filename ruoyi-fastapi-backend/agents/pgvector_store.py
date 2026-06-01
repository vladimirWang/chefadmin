from functools import lru_cache

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_postgres import PGVector
from sqlalchemy import select

import agents.config_data as config
from config.database import SYNC_SQLALCHEMY_DATABASE_URL
from utils.reader import logical_filename_from_storage_name


def get_embeddings() -> DashScopeEmbeddings:
    return DashScopeEmbeddings(model=config.embedding_model)


@lru_cache(maxsize=1)
def get_pgvector_store() -> PGVector:
    """获取 PGVector 向量库单例（与 ruoyi-fastapi 共用 PostgreSQL）。"""
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=config.collection_name,
        connection=SYNC_SQLALCHEMY_DATABASE_URL,
        use_jsonb=True,
        embedding_length=config.embedding_length,
        create_extension=True,
    )


def delete_by_logical_source(store: PGVector, logical_source: str) -> int:
    """删除同一逻辑文件的历史向量（含旧版带时间戳的 source）。"""
    ids_to_delete: list[str] = []
    with store._make_sync_session() as session:
        collection = store.get_collection(session)
        if not collection:
            return 0
        rows = session.execute(
            select(store.EmbeddingStore.id, store.EmbeddingStore.cmetadata).where(
                store.EmbeddingStore.collection_id == collection.uuid
            )
        ).all()
        for row_id, cmetadata in rows:
            src = (cmetadata or {}).get('source') or ''
            if logical_filename_from_storage_name(src) == logical_source:
                ids_to_delete.append(row_id)

    if ids_to_delete:
        store.delete(ids=ids_to_delete, collection_only=True)
    return len(ids_to_delete)
