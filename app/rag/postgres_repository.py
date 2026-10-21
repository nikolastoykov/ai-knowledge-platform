from sqlalchemy import delete, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import DocumentChunkModel, KnowledgeDocumentModel
from app.domain.search import ChunkSearchResult, DocumentChunk, EmbeddedDocumentChunk, KnowledgeDocument, KeywordSearchResult


class PostgresKnowledgeRepository:

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def replace_document(self, document: KnowledgeDocument, chunks: list[EmbeddedDocumentChunk]) -> None:
        if any(chunk.source_id != document.id for chunk in chunks):
            raise ValueError("All chunks must belong to the document being replaced.")

        chunk_indexes = [chunk.index for chunk in chunks]

        if len(chunk_indexes) != len(set(chunk_indexes)):
            raise ValueError("Chunk indexes must be unique.")

        async with self.session_factory() as session:
            async with session.begin():
                document_statement = (
                    insert(KnowledgeDocumentModel)
                    .values(
                        id=document.id,
                        text=document.text
                    )
                    .on_conflict_do_update(
                        index_elements=[KnowledgeDocumentModel.id],
                        set_={
                            "text": document.text
                        }
                    )
                )

                await session.execute(document_statement)

                await session.execute(
                    delete(DocumentChunkModel).where(
                        DocumentChunkModel.source_id == document.id
                    )
                )

                if chunks:
                    await session.execute(
                        insert(DocumentChunkModel).values(
                            [
                                {
                                    "source_id": chunk.source_id,
                                    "chunk_index": chunk.index,
                                    "text": chunk.text,
                                    "embedding": chunk.embedding,
                                }
                                for chunk in chunks
                            ]
                        )
                    )
    async def search_chunks_semantic(self, query_embedding: list[float], limit: int = 5) -> list[ChunkSearchResult]:

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        distance = DocumentChunkModel.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                DocumentChunkModel.source_id,
                DocumentChunkModel.chunk_index,
                DocumentChunkModel.text,
                distance.label("distance")
            )
            .order_by(distance)
            .limit(limit)
        )

        async with self.session_factory() as session:
            rows = (await session.execute(statement)).all()

        return [
            ChunkSearchResult(
                chunk=DocumentChunk(
                    source_id=source_id,
                    index=chunk_index,
                    text=text
                ),
                similarity=1 - distance_value,
            )
            for source_id, chunk_index, text, distance_value in rows
        ]

    async def search_chunks_keyword(self, query: str, limit: int=5) -> list[KeywordSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        keyword_query = " OR ".join(query.strip().split())
        ts_query = func.websearch_to_tsquery("simple", keyword_query)
        rank = func.ts_rank_cd(DocumentChunkModel.search_vector, ts_query)

        statement = (
            select(
                DocumentChunkModel.source_id,
                DocumentChunkModel.chunk_index,
                DocumentChunkModel.text,
                rank.label("rank")
            )
            .where(DocumentChunkModel.search_vector.op("@@")(ts_query))
            .order_by(rank.desc())
            .limit(limit)
        )

        async with self.session_factory() as session:
            rows = (await session.execute(statement)).all()

        return [
            KeywordSearchResult(
                chunk=DocumentChunk(source_id=source_id, index=chunk_index, text=text),
                rank=rank_value
            )
            for source_id, chunk_index, text, rank_value in rows
        ]