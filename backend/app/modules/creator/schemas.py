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

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("niche", "platform")
    @classmethod
    def normalize_fields(cls, value: str) -> str:
        return value.strip().lower()


# =========================================================
# UPDATE REQUEST
# =========================================================

class CreatorUpdateRequest(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    niche: Optional[
        Literal[
            "finance",
            "tech",
            "fitness",
            "fashion",
            "general",
        ]
    ] = None

    platform: Optional[
        Literal[
            "instagram",
            "tiktok",
            "youtube",
        ]
    ] = None

    followers: Optional[int] = Field(
        default=None,
        gt=0,
    )

    engagement_rate: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
    )

    model_config = ConfigDict(
        extra="forbid",
    )

    @field_validator("name")
    @classmethod
    def validate_name(
        cls,
        value: str | None,
    ) -> str | None:
    
        if value is None:
            return value

        return value.strip()

    @field_validator("niche", "platform")
    @classmethod
    def normalize_fields(
        cls,
        value: str | None,
    ) -> str | None:

        if value is None:
            return value

        return value.strip().lower()

# =========================================================
# PRICING REPORT
# =========================================================

class PricingReportResponse(BaseModel):

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

    id: int

    user_id: int

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
# CREATOR LIST RESPONSE
# =========================================================

class CreatorListResponse(BaseModel):

    creators: list[CreatorDTO]

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# FULL CREATOR RESPONSE
# =========================================================

class CreatorResponse(BaseModel):

    id: int

    user_id: int

    name: str

    niche: str

    platform: str

    followers: int

    engagement_rate: float

    estimated_price: Optional[float] = None

    pricing_report: PricingReportResponse

    scorecard: ScorecardResponse

    model_config = ConfigDict(
        from_attributes=True,
    )


# =========================================================
# PRICING RESPONSE
# =========================================================

class CreatorPricingResponse(BaseModel):

    creator: CreatorDTO

    pricing: dict[str, Any]