from pydantic import BaseModel


# =========================================================
# CREATOR INPUT SCHEMA
# =========================================================

class CreatorCreate(BaseModel):
    name: str
    niche: str
    platform: str
    followers: int
    engagement_rate: float


# =========================================================
# CREATOR RESPONSE SCHEMA
# =========================================================

class CreatorOut(BaseModel):
    id: int
    name: str
    niche: str
    platform: str
    followers: int
    engagement_rate: float
    estimated_price: float | None = None

    model_config = {
        "from_attributes": True
    }


# =========================================================
# PRICING REPORT SCHEMA
# =========================================================

class PricingReport(BaseModel):
    estimated_price: float
    confidence_score: float
    market_label: str
    reasoning: str