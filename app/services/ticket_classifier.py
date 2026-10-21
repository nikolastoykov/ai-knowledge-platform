from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.models import AIRequest
from app.domain.ticket import TicketAnalysis


class TicketClassifierService:

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def classify(self, text: str) -> TicketAnalysis:
        result = await self.llm_provider.generate_structured(
            AIRequest(
                instructions="""
                Analyze the customer support ticket.
                
                Determine:
                - the category
                - the priority
                - whether human intervention is required
                - your confidence
                
                Do not invent infomation that is not present in the ticket.
                """,
                input=text,
            ),
            TicketAnalysis
        )

        return result

ticket_classifier_service = TicketClassifierService(llm_provider)