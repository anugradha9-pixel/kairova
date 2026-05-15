from pydantic import BaseModel
from typing import Optional


# ---------------------------
# REQUEST SCHEMA
# ---------------------------
class CreatorCreate(BaseModel):
    name: str
    niche: str
    platform: str
    followers: int
    engagement_rate: float


# ---------------------------
# RESPONSE SCHEMA (DB OUTPUT)
# ---------------------------
class CreatorOut(BaseModel):
    id: int
    name: str
    niche: str
    platform: str
    followers: int
    engagement_rate: float
    estimated_price: Optional[float]

    class Config:
        from_attributes = True