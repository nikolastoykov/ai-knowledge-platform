from openai import AsyncOpenAI
import asyncio

from app.config import settings
from app.domain.managed_rag import ManagedSearchResult


class ManagedRAGService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def create_vector_store(self, name: str) -> str:
        vector_store = await self.client.vector_stores.create(name=name)
        return vector_store.id

    async def upload_file(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            upload_file = await self.client.files.create(file=file, purpose="assistants")

        return upload_file.id

    async def attach_file(self, vector_store_id: str, file_id: str) -> None:
        await self.client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id
        )

    async def wait_until_file_ready(self, vector_store_id: str, file_id: str) -> None:
        while True:
            vector_store_file = await self.client.vector_stores.files.retrieve(
                vector_store_id=vector_store_id,
                file_id=file_id
            )

            if vector_store_file.status == "completed":
                return

            if vector_store_file.status == "failed":
                raise RuntimeError("Managed RAG file processing failed.")

            await asyncio.sleep(1)

    async def search(self, vector_store_id: str, query: str):
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        response = await self.client.vector_stores.search(
            vector_store_id=vector_store_id,
            query=query
        )

        results = []

        for item in response.data:
            text = "\n".join(
                content.text
                for content in item.content
                if content.type == "text"
            )

            results.append(
                ManagedSearchResult(
                    file_id=item.file_id,
                    filename=item.filename,
                    text=text,
                    score=item.score
                )
            )

        return results

    async def ingest_file(self, file_path: str, vector_store_name: str) -> tuple[str, str]:
        vector_store_id = await self.create_vector_store(vector_store_name)
        file_id = await self.upload_file(file_path)
        await self.attach_file(vector_store_id=vector_store_id, file_id=file_id)
        await self.wait_until_file_ready(vector_store_id=vector_store_id, file_id=file_id)

        return vector_store_id, file_id

    async def answer(self, vector_store_id: str, question: str) -> str:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        response = await self.client.responses.create(
            model=settings.openai_model,
            input=question,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [vector_store_id]
                }
            ]
        )

        return response.output_text


managed_rag_service = ManagedRAGService()