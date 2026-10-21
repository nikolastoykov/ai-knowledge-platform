from fastapi import APIRouter
from pydantic import BaseModel

from app.domain.ticket import TicketAnalysis
from app.services.ticket_classifier import ticket_classifier_service


router = APIRouter(prefix="/ai", tags=["AI"])


class TicketRequest(BaseModel):
    text: str


@router.post("/classify-ticket", response_model=TicketAnalysis)
async def classify_ticket(request: TicketRequest) -> TicketAnalysis:

    return await ticket_classifier_service.classify(request.text)