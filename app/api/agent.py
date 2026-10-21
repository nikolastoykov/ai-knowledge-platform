from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agent import agent_service
from app.tools.orders import GET_ORDER_TOOL
from app.tools.customers import GET_CUSTOMER_TOOL


router = APIRouter(prefix="/agent", tags=["Agent"])


class AgentRequest(BaseModel):
    task: str

@router.post("/run")
async def run_agent(request: AgentRequest) -> dict:
    answer = await agent_service.run(
        task=request.task,
        tools=[
            GET_ORDER_TOOL,
            GET_CUSTOMER_TOOL
        ]
    )

    return {
        "answer": answer
    }