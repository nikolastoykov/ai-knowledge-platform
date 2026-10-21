from pydantic import BaseModel, Field


class RerankItm(BaseModel):
    candidate_id: int
    relevance_score: float = Field(ge=0, le=1)

class RerankResponse(BaseModel):
    results: list[RerankItm]