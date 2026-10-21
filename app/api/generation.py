from fastapi import APIRouter
from pydantic import BaseModel

from app.ai import llm_provider


router = APIRouter(prefix="/ai", tags=["AI"])

class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    text: str


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    result = await llm_provider.generate(request.prompt)

    return GenerateResponse(text=result)