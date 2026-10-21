from app.ai.embedding_provider import EmbeddingProvider
from app.domain.search import EmbeddedDocumentChunk, KnowledgeDocument
from app.rag.chunking import chunk_text
from app.rag.repository import KnowledgeRepository
from app.ai import embedding_provider
from app.rag import knowledge_repository

class KnowledgeIngestionService:

    def __init__(self, embedding_provider: EmbeddingProvider,
                 repository: KnowledgeRepository,
                 chunk_size: int = 1000,
                 overlap: int = 200):
        self.embedding_provider = embedding_provider
        self.repository = repository
        self.chunk_size = chunk_size
        self.overlap = overlap

    async def ingest(self, document: KnowledgeDocument) -> int:
        if not document.id.strip():
            raise ValueError("Document ID cannot be empty.")

        if not document.text.strip():
            raise ValueError("Document text cannot be empty.")

        chunks = chunk_text(
            source_id=document.id,
            text=document.text,
            chunk_size=self.chunk_size,
            overlap=self.overlap
        )

        embeddings = await self.embedding_provider.embed_many([chunk.text for chunk in chunks])

        if len(embeddings) != len(chunks):
            raise RuntimeError("Embedding provider returned an unexpected number of embeddings.")

        embedded_chunks = [
            EmbeddedDocumentChunk(
                source_id=chunk.source_id,
                index=chunk.index,
                text=chunk.text,
                embedding=embedding
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]

        await self.repository.replace_document(document=document, chunks=embedded_chunks)

        return len(embedded_chunks)


knowledge_ingestion_service = KnowledgeIngestionService(
    embedding_provider=embedding_provider,
    repository=knowledge_repository,
)