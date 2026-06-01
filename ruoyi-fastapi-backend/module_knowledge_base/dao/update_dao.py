"""兼容 gRPC 调用，实际逻辑见 knowledge_base_dao。"""

from module_knowledge_base.dao.knowledge_base_dao import KnowledgeBaseDao as UpdateDao

__all__ = ['UpdateDao']
