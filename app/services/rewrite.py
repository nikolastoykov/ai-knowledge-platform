from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.openai_provider import AIRequest
from app.domain.rewrite import Tone


class RewriteService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def rewrite(self, text: str, tone: Tone) -> str:
        response = await self.llm_provider.generate(
            AIRequest(
                instructions=f"""
                Rewrite the probided text.
                Required tone: {tone.value}
                Preserve the original meaning.
                Do not add information that is not present.
                """,
                input=text,
            )
        )

        return response.text

rewrite_service = RewriteService(llm_provider)