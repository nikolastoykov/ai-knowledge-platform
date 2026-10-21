from app.ai import llm_provider
from app.ai.llm_provider import LLMProvider
from app.ai.models import AIRequest
from app.domain.evals import RAGAnswerEvaluation


class RAGAnswerJudge:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def evaluate(self, question: str, answer: str, context: str) -> RAGAnswerEvaluation:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        if not answer.strip():
            raise ValueError("Answer cannot be empty.")

        return await self.llm_provider.generate_structured(
            AIRequest(
                instructions="Evaluate the answer against the question and provided context. " \
                "Mark correct=true only if the answer correctly answers the user's question. " \
                "Mark grounded=true only if the answer is supported by the context and does not invent unsupported facts. " \
                "Give an overall score from 0 to 1 and a short reason.",
                input=f"Question:\n{question}\n\nAnswer:\n{answer}\n\nContext:\n{context}",
            ),
            RAGAnswerEvaluation,
        )

rag_answer_judge = RAGAnswerJudge(llm_provider=llm_provider)