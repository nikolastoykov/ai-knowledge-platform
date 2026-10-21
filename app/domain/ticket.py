from enum import StrEnum

from pydantic import BaseModel, Field


class TicketCategory(StrEnum):
    BILLING = "billing"
    SHIPPING = "shipping"
    RETURN = "return"
    PRODUCT = "product"
    OTHER = "other"


class TicketPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TicketAnalysis(BaseModel):
    category: TicketCategory
    priority: TicketPriority
    requires_human: bool

    confidence: float = Field(ge=0, le=1)