from app.db.database import session_factory
from app.rag.postgres_repository import PostgresKnowledgeRepository


knowledge_repository = PostgresKnowledgeRepository(session_factory=session_factory)