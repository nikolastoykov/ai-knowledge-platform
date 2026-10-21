from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.models import SearchDocumentModel
from app.domain.search import SearchDocument, SearchResult


class PostgreVectorStore:

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def add(self, document: SearchDocument) -> None:
        async with self.session_factory() as session:
            statement = insert(SearchDocumentModel).values(
                id=document.id,
                text=document.text,
                embedding=document.embedding
            )

            statement = statement.on_conflict_do_update(
                index_elements=[SearchDocumentModel.id],
                set_={
                    "text": document.text,
                    "embedding": document.embedding
                }
            )

            await session.execute(statement)
            await session.commit()

    async def add_many(self, documents: list[SearchDocument]) -> None:
        if not documents:
            return
        
        statement = insert(SearchDocumentModel).values(
            [
                {
                    "id": document.id,
                    "text": document.text,
                    "embedding": document.embedding
                }
                for document in documents
            ]
        )

        statement = statement.on_conflict_do_update(
            index_elements=[SearchDocumentModel.id],
            set_={
                "text": statement.excluded.text,
                "embedding": statement.excluded.embedding
            }
        )

        async with self.session_factory() as session:
            await session.execute(statement)
            await session.commit()

    async def search(self, query_embedding: list[float], limit: int = 5) -> list[SearchResult]:
        distance = SearchDocumentModel.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                SearchDocumentModel,
                distance.label("distance"),
            )
            .order_by(distance)
            .limit(limit)
        )

        async with self.session_factory() as session:
            rows = (await session.execute(statement)).all()

        return [
            SearchResult(
                document=SearchDocument(
                    id=model.id,
                    text=model.text,
                    embedding=model.embedding
                ),
                similarity=1 - distance_value
            )
            for model, distance_value in rows
        ]