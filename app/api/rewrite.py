from fastapi import APIRouter
from pydantic import BaseModel

from app.domain.rewrite import Tone
from app.services.rewrite import rewrite_service


router = APIRouter(prefix="/ai", tags=["AI"])


class RewriteRequest(BaseModel):
    text: str
    tone: Tone

class RewriteResponse(BaseModel):
    text: str

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite(request: RewriteRequest) -> RewriteResponse:
    rewriten_text = await rewrite_service.rewrite(request.text, request.tone)

    return RewriteResponse(text=rewriten_text)