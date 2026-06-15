from pydantic import BaseModel, ConfigDict


# =========================================================
# PRICING DOMAIN MODEL (INTERNAL AI LAYER)
# =========================================================

class PricingReport(BaseModel):
    """
    Internal AI pricing output model.

    This is NOT an API DTO.
    Used only inside service / AI pipeline.
    """

    estimated_price: float
    confidence_score: float
    market_label: str
    reasoning: str

    # =====================================================
    # PYDANTIC CONFIG
    # =====================================================

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        from_attributes=True,
    )