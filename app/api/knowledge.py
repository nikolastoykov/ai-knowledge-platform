from typing import Annotated

from fastapi import APIRouter
from pydantic import BaseModel, Field, StringConstraints

from app.domain.search import KnowledgeDocument
from app.services.knowledge_ingestion import knowledge_ingestion_service
from app.services.knowledge_search import knowledge_search_service


router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class IngestDocumentRequest(BaseModel):
    id: NonEmptyString
    text: NonEmptyString

class IngestDocumentResponse(BaseModel):
    id: str
    chunks: int

class HybridSearchRequest(BaseModel):
     query: NonEmptyString
     limit: int = Field(default=5, ge=1, le=20)

class HybridSearchResultResponse(BaseModel):
     source_id: str
     chunk_index: int
     text: str
     score: float

class RerankedSearchResultReponse(BaseModel):
     source_id: str
     chunk_index: int
     text: str
     relevance_score: float

@router.post("/documents")
async def ingest_document(request: IngestDocumentRequest) -> IngestDocumentResponse:
        document = KnowledgeDocument(id=request.id, text=request.text)

        chunk_count = await knowledge_ingestion_service.ingest(document)

        return IngestDocumentResponse(
             id=document.id,
             chunks=chunk_count
        )

@router.post("/search/hybrid")
async def search_hybrid(request: HybridSearchRequest) -> list[HybridSearchResultResponse]:
     results = await knowledge_search_service.search_hybrid(query=request.query, limit=request.limit)

     return [
          HybridSearchResultResponse(
               source_id=result.chunk.source_id,
               chunk_index=result.chunk.index,
               text=result.chunk.text,
               score=result.score
          )
          for result in results
     ]

@router.post("/search/reranked")
async def search_reranked(request: HybridSearchRequest) -> list[RerankedSearchResultReponse]:
     results = await knowledge_search_service.search_reranked(query=request.query, limit=request.limit)

     return [
          RerankedSearchResultReponse(
               source_id=result.chunk.source_id,
               chunk_index=result.chunk.index,
               text=result.chunk.text,
               relevance_score=result.relevance_score
          )
          for result in results
     ]