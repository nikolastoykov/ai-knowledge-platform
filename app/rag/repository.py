from typing import Protocol

from app.domain.search import ChunkSearchResult, EmbeddedDocumentChunk, KeywordSearchResult, KnowledgeDocument


class KnowledgeRepository(Protocol):

    async def replace_document(self, document: KnowledgeDocument, chunks: list[EmbeddedDocumentChunk]) -> None:
        ...

    async def search_chunks_semantic_semantic(self, query_embedding: list[float], limit: int = 5) -> list[ChunkSearchResult]:
        ...

    async def search_chunks_keyword(self, query: str, limit: int = 5) -> list[KeywordSearchResult]:
        ...