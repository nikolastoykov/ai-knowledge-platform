from fastapi import APIRouter
from pydantic import BaseModel

from app.ai import llm_provider
from app.ai.models import AIRequest


router = APIRouter(prefix="/ai", tags=["AI"])

class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    text: str


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    result = await llm_provider.generate(AIRequest(input=request.prompt))

    return GenerateResponse(text=result.text)
