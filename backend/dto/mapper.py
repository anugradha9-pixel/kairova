from backend.dto.pricing import CreatorPricingResponse


def to_pricing_response(report) -> CreatorPricingResponse:
    return CreatorPricingResponse(
        creator_id=report.creator_id,
        estimated_rate=report.estimated_rate,
        confidence_score=report.confidence_score,
        market_label=report.market_label,
        reasoning=report.reasoning,
    )