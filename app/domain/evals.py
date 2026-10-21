from pydantic import BaseModel, Field


class RAGAnswerEvaluation(BaseModel):
    correct: bool
    grounded: bool
    score: float = Field(ge=0, le=1)
    reason: str