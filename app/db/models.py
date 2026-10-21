from pgvector.sqlalchemy import Vector
from sqlalchemy import Computed, ForeignKey, Integer, Index, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from app.config import settings
from app.db.base import Base


class SearchDocumentModel(Base):
    __tablename__ = "search_documents"
    __table_args__ = (
        Index(
            "ix_search_documents_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"}
        ),
    )

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embedding_dimensions), nullable=False)

class KnowledgeDocumentModel(Base):
    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)

class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "source_id",
            "chunk_index",
            name="uq_document_chunks_source_index",
        ),
        Index(
            "ix_document_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={
                "embedding": "vector_cosine_ops"
            },
        ),
        Index(
            "ix_document_chunks_search_vector_gin",
            "search_vector",
            postgresql_using="gin"
        )
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    source_id: Mapped[str] = mapped_column(ForeignKey("knowledge_documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(settings.embedding_dimensions), nullable=False)
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, Computed("to_tsvector('simple', text)", persisted=True))