from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.openai_provider import AIRequest


class SummarizationService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def summarize(self, text: str) -> str:
        response = await self.llm_provider.generate(
            AIRequest(
                instructions="""
                Summarize the provided text clearly and concisely.
                Preserve the important information.
                """,
                input=text
            )
        )

        return response.text

summarization_service = SummarizationService(llm_provider)