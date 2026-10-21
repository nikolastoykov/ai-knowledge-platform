from fastapi import APIRouter, HTTPException
from typing import Annotated
from pydantic import BaseModel, Field, StringConstraints

from app.services.semantic_search import semantic_search_service


router = APIRouter(prefix="/search", tags=["Search"])

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

class AddDocumentRequest(BaseModel):
    id: NonEmptyString
    text: NonEmptyString

class SearchRequest(BaseModel):
    query: NonEmptyString
    limit: int = Field(default=5, ge=1, le=100)

class SearchResultResponse(BaseModel):
    id: str
    text: str
    similarity: float

@router.post("/documents")
async def add_document(request: AddDocumentRequest) -> dict:
    await semantic_search_service.add_document(document_id=request.id, text=request.text)

    return {
        "status": "added",
        "id": request.id
    }

@router.post("/documents/batch")
async def add_documents(requests: Annotated[list[AddDocumentRequest], Field(min_length=1, max_length=100)]) -> dict:
    ids = [request.id for request in requests]

    if len(ids) != len(set(ids)):
        raise HTTPException(status_code=422, detail="Document IDs must be unique within a batch.")

    await semantic_search_service.add_documents([(request.id, request.text) for request in requests])

    return {
        "status": "added",
        "count": len(requests)
    }

@router.post("/query", response_model=list[SearchResultResponse])
async def search (request: SearchRequest) -> list[SearchRequest]:
    results = await semantic_search_service.search(query=request.query, limit=request.limit)

    return [
        SearchResultResponse(
            id=result.document.id,
            text=result.document.text,
            similarity=result.similarity
        )
        for result in results
    ]