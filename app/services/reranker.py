from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.models import AIRequest
from app.domain.reranking import RerankResponse
from app.domain.search import HybridSearchResult, RerankedSearchResult
from app.config import settings


class RerankerService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def rerank(self, query: str, candidates: list[HybridSearchResult], limit: int = 5) -> list[RerankedSearchResult]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("limit must be greater than 0.")

        if not candidates:
            return []

        candidates_text = "\n\n".join(
            f"Candidate {candidate_id}:\n{candidate.chunk.text}"
            for candidate_id, candidate in enumerate(candidates)
        )

        response = await self.llm_provider.generate_structured(
            AIRequest(
                instructions="Score every candidate from 0 to 1 based on whether it contains enough information to directly answer the user's exact query. A candidate that is only generally related to the topic but does not answer the specific question should receive a low score. Return every candidate exactly once.",
                input=f"Query:\n{query}\n\nCandidates:\n{candidates_text}",
            ),
            RerankResponse,
        )

        expected_ids = set(range(len(candidates)))
        returned_ids = [item.candidate_id for item in response.results]

        if len(returned_ids) != len(set(returned_ids)) or set(returned_ids) != expected_ids:
            raise RuntimeError("Reranker returned invalid candidate IDs.")

        results = [
            RerankedSearchResult(
                chunk=candidates[item.candidate_id].chunk,
                relevance_score=item.relevance_score,
            )
            for item in response.results
        ]

        results = [result for result in results if result.relevance_score >= settings.rag_min_relevance]

        return sorted(results, key=lambda result: result.relevance_score, reverse=True)[:limit]


reranker_service = RerankerService(llm_provider=llm_provider)