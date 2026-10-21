from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.rag import rag_service


router = APIRouter(prefix="/rag", tags=["RAG"])


class RAGRequest(BaseModel):
    question: str
    limit: int = Field(default=5, ge=1, le=20)

class RAGSourceResponse(BaseModel):
    source_id: str
    chunk_index: int
    text: str
    relevance_score: float

class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSourceResponse]


@router.post("/ask")
async def ask(request: RAGRequest) -> RAGResponse:
    result = await rag_service.answer(question=request.question, limit=request.limit)

    return RAGResponse(answer=result.answer, sources=[
        RAGSourceResponse(
            source_id=source.chunk.source_id,
            chunk_index=source.chunk.index,
            text=source.chunk.text,
            relevance_score=source.relevance_score,
        )
        for source in result.sources
        ],
    )