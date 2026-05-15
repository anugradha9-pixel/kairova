from sqlalchemy.ext.asyncio import AsyncSession

from backend.creator.models import Creator
from backend.creator.schemas import CreatorCreate, PricingReport
from backend.creator.repository import CreatorRepository

from backend.core_engine.pricing import estimate_price
from backend.ai_engine.explain import generate_explanation
from backend.ai_engine.confidence import calculate_confidence_score
from backend.ai_engine.labeling import generate_market_label


def _build_pricing_report(
    followers: int,
    engagement_rate: float,
    platform: str,
    niche: str,
) -> PricingReport:

    estimated_price = estimate_price(
        followers=followers,
        engagement_rate=engagement_rate,
        platform=platform,
    )

    confidence_score = calculate_confidence_score(
        followers=followers,
        engagement_rate=engagement_rate,
    )

    market_label = generate_market_label(price=estimated_price)

    reasoning = generate_explanation(
        niche=niche,
        platform=platform,
        followers=followers,
        engagement_rate=engagement_rate,
        estimated_price=estimated_price,
    )

    return PricingReport(
        estimated_price=estimated_price,
        confidence_score=confidence_score,
        market_label=market_label,
        reasoning=reasoning,
    )


# =========================================================
# CREATE CREATOR (ASYNC READY)
# =========================================================

async def create_creator_service(
    db: AsyncSession,
    payload: CreatorCreate,
):

    repo = CreatorRepository(db)

    creator = Creator(
        name=payload.name,
        niche=payload.niche,
        platform=payload.platform,
        followers=payload.followers,
        engagement_rate=payload.engagement_rate,
    )

    creator = await repo.create_creator(creator)

    report = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    creator.estimated_price = report.estimated_price
    creator = await repo.update_creator(creator)

    return creator, report


# =========================================================
# GET CREATOR PRICING (ASYNC)
# =========================================================

async def get_creator_pricing_service(
    db: AsyncSession,
    creator_id: int,
):

    repo = CreatorRepository(db)

    creator = await repo.get_by_id(creator_id)

    if not creator:
        return None, None

    report = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    return creator, report