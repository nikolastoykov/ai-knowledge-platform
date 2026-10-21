from typing import Protocol

from app.domain.search import SearchDocument, SearchResult


class VectorStore(Protocol):

    async def add(self, document: SearchDocument) -> None:
        ...

    async def add_many(self, document: list[SearchDocument]) -> None:
        ...

    async def search(self, query_embedding: list[float], limit: int = 5) -> list[SearchResult]:
        ...
