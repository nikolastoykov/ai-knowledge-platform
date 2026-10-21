from typing import Protocol

from openai import AsyncOpenAI

from app.config import settings


class EmbeddingProvider(Protocol):
    async def embed(self, text: str) -> list[float]:
        ...

class OpenAIEmbeddingProvider:

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def embed(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
            dimensions=settings.embedding_dimensions
        )

        return response.data[0].embedding

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
            response = await self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=texts,
                dimensions=settings.embedding_dimensions
            )
    
            return [
                 item.embedding
                 for item in sorted(response.data, key=lambda item: item.index)
            ]