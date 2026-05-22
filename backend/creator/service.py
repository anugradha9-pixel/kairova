from sqlalchemy.ext.asyncio import AsyncSession

from backend.creator.models import Creator
from backend.creator.schemas import (
    CreatorCreate,
    PricingReport,
)
from backend.creator.repository import CreatorRepository

from backend.core_engine.pricing import estimate_price

from backend.ai_engine.explain import generate_explanation
from backend.ai_engine.confidence import calculate_confidence_score
from backend.ai_engine.labeling import generate_market_label


# =========================================================
# INTERNAL: BUILD PRICING REPORT
# =========================================================

def _build_pricing_report(
    followers: int,
    engagement_rate: float,
    platform: str,
    niche: str,
) -> PricingReport:

    # -----------------------------------------------------
    # Pricing Engine
    # -----------------------------------------------------

    estimated_price = estimate_price(
        followers=followers,
        engagement_rate=engagement_rate,
        platform=platform,
    )

    # -----------------------------------------------------
    # AI Confidence
    # -----------------------------------------------------

    confidence_score = calculate_confidence_score(
        followers=followers,
        engagement_rate=engagement_rate,
    )

    # -----------------------------------------------------
    # Market Tier Label
    # -----------------------------------------------------

    market_label = generate_market_label(
        price=estimated_price
    )

    # -----------------------------------------------------
    # AI Explanation
    # -----------------------------------------------------

    reasoning = generate_explanation(
        niche=niche,
        platform=platform,
        followers=followers,
        engagement_rate=engagement_rate,
        estimated_price=estimated_price,
    )

    # -----------------------------------------------------
    # Typed Response
    # -----------------------------------------------------

    return PricingReport(
        estimated_price=estimated_price,
        confidence_score=confidence_score,
        market_label=market_label,
        reasoning=reasoning,
    )


# =========================================================
# CREATE CREATOR
# =========================================================

async def create_creator_service(
    db: AsyncSession,
    payload: CreatorCreate,
):

    repo = CreatorRepository(db)

    # -----------------------------------------------------
    # Create ORM Object
    # -----------------------------------------------------

    creator = Creator(
        name=payload.name,
        niche=payload.niche,
        platform=payload.platform,
        followers=payload.followers,
        engagement_rate=payload.engagement_rate,
    )

    # -----------------------------------------------------
    # Persist Creator
    # -----------------------------------------------------

    creator = await repo.create(creator)

    # -----------------------------------------------------
    # Generate Pricing Report
    # -----------------------------------------------------

    report = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    # -----------------------------------------------------
    # Save Estimated Price
    # -----------------------------------------------------

    creator = await repo.update_price(
        creator=creator,
        estimated_price=report.estimated_price,
    )

    # -----------------------------------------------------
    # Return Typed Objects
    # -----------------------------------------------------

    return creator, report


# =========================================================
# GET CREATOR PRICING
# =========================================================

async def get_creator_pricing_service(
    db: AsyncSession,
    creator_id: int,
):

    repo = CreatorRepository(db)

    # -----------------------------------------------------
    # Fetch Creator
    # -----------------------------------------------------

    creator = await repo.get_by_id(creator_id)

    # -----------------------------------------------------
    # Handle Missing Creator
    # -----------------------------------------------------

    if not creator:
        return None, None

    # -----------------------------------------------------
    # Recompute Pricing
    # -----------------------------------------------------

    report = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    # -----------------------------------------------------
    # Return Typed Objects
    # -----------------------------------------------------

    return creator, report