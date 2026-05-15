from pydantic import BaseModel


class CreatorPricingResponse(BaseModel):
    creator_id: int
    estimated_rate: float
    confidence_score: float
    market_label: str
    reasoning: str