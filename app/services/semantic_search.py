from app.ai.embedding_provider import EmbeddingProvider
from app.domain.search import SearchDocument, SearchResult
from app.search.vector_store import VectorStore
from app.ai import embedding_provider
from app.search import search_vector_store


class SemanticSearchService:

    def __init__(self, embedding_provider: EmbeddingProvider, vector_store:  VectorStore):
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    async def search(self, query: str, limit: int = 5) -> list [SearchResult]:
        query_embedding = await self.embedding_provider.embed(query)

        return await self.vector_store.search(query_embedding=query_embedding, limit=limit)

    async def add_document(self, document_id: str, text: str) -> None:
        embedding = await self.embedding_provider.embed(text)

        document = SearchDocument(id=document_id, text=text, embedding=embedding)

        await self.vector_store.add(document)

    async def add_documents(self, documents: list[str, str]) -> None:
        if not documents:
            return

        ids = [document_id for document_id, _ in documents]
        if len(ids) != len(set(ids)):
            raise ValueError("Document IDs must be unique within a batch.")

        texts = [text for _, text in documents]

        embeddings = await self.embedding_provider.embed_many(texts)

        if len(embeddings) != len(documents):
            raise RuntimeError("Embedding provider returned an unexpected number of embeddings.")

        search_documents = [
            SearchDocument(
                id=document_id,
                text=text,
                embedding=embedding
            )
            for (document_id, text), embedding in zip(documents, embeddings)
        ]

        await self.vector_store.add_many(search_documents)


semantic_search_service = SemanticSearchService(
    embedding_provider=embedding_provider,
    vector_store=search_vector_store,
)