from app.domain.search import SearchDocument, SearchResult
from app.search.similarity import cosine_similarity


class InMemoryVectorStore:

    def __init__(self):
        self.documents: list[SearchDocument] = {}

    async def add(self, document: SearchDocument) -> None:
        self.documents[document.id] = document

    async def add_many(self, documents: list[SearchDocument]) -> None:
        for document in documents:
            self.documents[document.id] = document

    async def search(self, query_embedding: list[float], limit: int = 5) -> list[SearchResult]:
        results = []

        for document in self.documents.values():
            similarity = cosine_similarity(query_embedding, document.embedding)

            results.append(SearchResult(document=document, similarity=similarity))

        results.sort(key=lambda result: result.similarity, reverse=True)

        return results[:limit]