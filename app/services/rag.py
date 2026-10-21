from app.ai.llm_provider import LLMProvider
from app.ai import llm_provider
from app.ai.models import AIRequest
from app.domain.search import RAGResult
from app.services.knowledge_search import KnowledgeSearchService, knowledge_search_service
from app.config import settings


class RAGService:

    def __init__(self, llm_provider: LLMProvider, knowledge_search_service: KnowledgeSearchService):
        self.llm_provider = llm_provider
        self.knowledge_search_service = knowledge_search_service

    async def answer(self, question: str, limit: int = 5) -> RAGResult:
        sources = await self.knowledge_search_service.search_reranked(query=question, limit=limit, min_similarity=settings.rag_min_similarity)

        if not sources:
            return RAGResult(answer="I don't know based on the available documents.", sources=[])

        context = "\n\n".join(
            (
                f"[Source: {source.chunk.source_id}, "
                f"Chunk: {source.chunk.index}]\n"
                f"{source.chunk.text}"
            )
            for source in sources
        )

        response = await self.llm_provider.generate(
            AIRequest(
                instructions=(
                    "Answer the user's question using only the provided context. "
                    "Do not invent information. "
                    "If the context does not contain the answer, say you don't know. "
                ),
                input=f"""
                Context:
                {context}

                Question:
                {question}
                """,
            )
        )

        return RAGResult(
            answer=response.text,
            sources=sources,
        )


rag_service = RAGService(llm_provider=llm_provider, knowledge_search_service=knowledge_search_service)