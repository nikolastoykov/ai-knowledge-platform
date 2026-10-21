from fastapi import APIRouter
from pydantic import BaseModel
from app.ai import embedding_provider
from app.search.similarity import cosine_similarity


router = APIRouter(prefix="/ai", tags=["AI"])


class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    dimensions: int
    preview: list[float]

class SimilarityRequest(BaseModel):
    text_a: str
    text_b: str

class SimilarityResponse(BaseModel):
    similarity: float


@router.post("/embed", response_model=EmbeddingResponse)
async def embed(request: EmbeddingRequest) -> EmbeddingResponse:
    vector = await embedding_provider.embed(request.text)

    return EmbeddingResponse(dimensions=len(vector), preview=vector[:10])


@router.post("/similarity", response_model=SimilarityResponse)
async def similarity(request: SimilarityRequest) -> SimilarityResponse:
    vector_a = await embedding_provider.embed(request.text_a)
    vector_b = await embedding_provider.embed(request.text_b)

    score = cosine_similarity(vector_a, vector_b)

    return SimilarityResponse(similarity=score)