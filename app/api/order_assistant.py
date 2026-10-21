from fastapi import APIRouter
from pydantic import BaseModel

from app.services.order_assistant import order_assistant_service


router = APIRouter(prefix="/ai", tags=["AI"])


class OrderQuestionRequest(BaseModel):
    question: str

class OrderQuestionResponse(BaseModel):
    answer: str


@router.post("/order-assistant", response_model=OrderQuestionResponse)
async def order_assistant(request: OrderQuestionRequest) -> OrderQuestionResponse:
    answer = await order_assistant_service.answer(request.question)

    return OrderQuestionResponse(answer=answer)