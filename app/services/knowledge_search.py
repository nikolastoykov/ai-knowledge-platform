from app.ai.embedding_provider import EmbeddingProvider
from app.domain.search import ChunkSearchResult, HybridSearchResult, KeywordSearchResult, RerankedSearchResult
from app.services.reranker import RerankerService, reranker_service
from app.rag.repository import KnowledgeRepository
from app.ai import embedding_provider
from app.rag import knowledge_repository
from app.rag.rank_fusion import reciprocal_rank_fusion

import asyncio


class KnowledgeSearchService:

    def __init__(self, embedding_provider: EmbeddingProvider, repository: KnowledgeRepository, reranker: RerankerService):
        self.embedding_provider = embedding_provider
        self.repository = repository
        self.reranker = reranker

    async def search(self, query: str, limit: int = 5) -> list[ChunkSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greather than 0.")

        query_embedding = await self.embedding_provider.embed(query)

        return await self.repository.search_chunks_semantic(query_embedding=query_embedding, limit=limit)

    async def search_keyword(self, query: str, limit: int = 5) -> list[KeywordSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        return await self.repository.search_chunks_keyword(query=query, limit=limit)

    async def search_hybrid(self, query: str, limit: int = 5, min_similarity: float | None = None) -> list[HybridSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        candidate_limit = max(limit * 2, 10)

        semantic_results, keyword_results = await asyncio.gather(
            self.search(query=query, limit=candidate_limit),
            self.search_keyword(query=query, limit=candidate_limit)
        )

        if min_similarity is not None:
            semantic_results = [result for result in semantic_results if result.similarity >= min_similarity]

        results = reciprocal_rank_fusion(semantic_results=semantic_results, keyword_results=keyword_results)

        return results[:limit]

    async def search_reranked(self, query: str, limit: int = 5, min_similarity: float | None = None) -> list[RerankedSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        candidate_limit = max(limit * 2, 10)

        candidates = await self.search_hybrid(query=query, limit=candidate_limit, min_similarity=min_similarity)

        return await self.reranker.rerank(query=query, candidates=candidates, limit=limit)


knowledge_search_service = KnowledgeSearchService(
    embedding_provider=embedding_provider,
    repository=knowledge_repository,
    reranker=reranker_service
)