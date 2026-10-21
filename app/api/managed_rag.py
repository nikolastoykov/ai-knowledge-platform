from fastapi import APIRouter
from pydantic import BaseModel

from app.services.managed_rag import managed_rag_service


router = APIRouter(prefix="/managed-rag", tags=["Managed RAG"])


class ManagedRAGIngestRequest(BaseModel):
    file_path: str
    vector_store_name: str


class ManagedRAGSearchRequest(BaseModel):
    vector_store_id: str
    query: str

class ManagedRAGAnswerRequest(BaseModel):
    vector_store_id: str
    question: str


@router.post("/ingest")
async def ingest_managed_rag(request: ManagedRAGIngestRequest) -> dict:
    vector_store_id, file_id = await managed_rag_service.ingest_file(
        file_path=request.file_path,
        vector_store_name=request.vector_store_name,
    )

    return {
        "vector_store_id": vector_store_id,
        "file_id": file_id,
    }

@router.post("/search")
async def search_managed_rag(request: ManagedRAGSearchRequest):
    return await managed_rag_service.search(
        vector_store_id=request.vector_store_id,
        query=request.query,
    )

@router.post("/answer")
async def answer_managed_rag(request: ManagedRAGAnswerRequest) -> dict:
    answer = await managed_rag_service.answer(
        vector_store_id=request.vector_store_id,
        question=request.question
    )

    return {
        "answer": answer
    }