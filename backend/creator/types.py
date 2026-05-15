from pydantic import BaseModel


class PricingReport(BaseModel):
    estimated_price: float
    confidence_score: float
    market_label: str
    reasoning: str