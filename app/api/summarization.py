from fastapi import APIRouter
from pydantic import BaseModel

from app.services.summarization import summarization_service


router = APIRouter(prefix="/ai", tags=["AI"])

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest) -> SummarizeResponse:
    summary = await summarization_service.summarize(request.text)

    return SummarizeResponse(summary=summary)