from typing import Optional, Literal, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


# =========================================================
# SUPPORTED VALUES
# =========================================================

SUPPORTED_PLATFORMS = {
    "instagram",
    "tiktok",
    "youtube",
}


SUPPORTED_NICHES = {
    "finance",
    "tech",
    "fitness",
    "fashion",
    "general",
}


# =========================================================
# CREATE REQUEST
# =========================================================

class CreatorCreate(BaseModel):
    """
    Incoming creator payload.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        examples=["Sarah Chen"],
    )

    niche: Literal[
        "finance",
        "tech",
        "fitness",
        "fashion",
        "general",
    ] = Field(
        ...,
        examples=["fitness"],
    )

    platform: Literal[
        "instagram",
        "tiktok",
        "youtube",
    ] = Field(
        ...,
        examples=["instagram"],
    )

    followers: int = Field(
        ...,
        gt=0,
        examples=[125000],
    )

    engagement_rate: float = Field(
        ...,
        ge=0,
        le=100,
        examples=[4.8],
    )

    # =====================================================
    # STRING CLEANUP
    # =====================================================

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.strip()


    @field_validator("niche", "platform")
    @classmethod
    def normalize_fields(cls, value: str) -> str:
        return value.strip().lower()


# =========================================================
# PRICING REPORT
# =========================================================

class PricingReportResponse(BaseModel):
    """
    AI pricing intelligence layer.
    """

    confidence_score: float = Field(
        examples=[0.82],
    )

    market_label: str = Field(
        examples=["high-value creator"],
    )

    reasoning: str = Field(
        examples=[
            (
                "Strong engagement and niche "
                "alignment increase pricing."
            )
        ],
    )


# =========================================================
# SCORECARD
# =========================================================

class ScorecardResponse(BaseModel):
    """
    AI creator scorecard.
    """

    price: float = Field(
        examples=[93.6],
    )

    tier: str = Field(
        examples=["micro"],
    )

    quality_score: float = Field(
        examples=[78.5],
    )

    confidence: float = Field(
        examples=[0.82],
    )

    market_position: str = Field(
        examples=["strong"],
    )

    recommendation: str = Field(
        examples=[
            "Strong creator for brand partnerships."
        ],
    )


# =========================================================
# CREATOR DTO
# =========================================================

class CreatorDTO(BaseModel):
    """
    Base creator database DTO.
    """

    id: int

    name: str

    niche: str

    platform: str

    followers: int

    engagement_rate: float

    estimated_price: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# FULL CREATOR RESPONSE
# =========================================================

class CreatorResponse(BaseModel):
    """
    Full creator API response.
    """

    id: int

    name: str

    niche: str

    platform: str

    followers: int

    engagement_rate: float

    estimated_price: float

    pricing_report: PricingReportResponse

    scorecard: ScorecardResponse

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# PRICING RESPONSE
# =========================================================

class CreatorPricingResponse(BaseModel):
    """
    Creator pricing endpoint response.
    """

    creator: CreatorDTO

    pricing: dict[str, Any]