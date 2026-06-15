from typing import Optional
from sqlalchemy.orm import Session

from app.modules.creator.domain import PricingReport
from app.modules.creator.models import Creator
from app.modules.creator.repository import CreatorRepository
from app.modules.creator.schemas import CreatorCreate

from app.core.core_engine.pricing import estimate_price
from app.core.core_engine.scorecard import generate_scorecard

from app.core.ai.ai_engine.confidence import (
    calculate_confidence_score,
)

from app.core.ai.ai_engine.labeling import (
    generate_market_label,
)

from app.core.ai.ai_engine.explain import (
    generate_explanation,
)


# =========================================================
# INTERNAL: PRICING PIPELINE
# =========================================================

def _build_pricing_report(
    followers: int,
    engagement_rate: float,
    platform: str,
    niche: str,
):
    """
    Internal AI pricing orchestration pipeline.
    """

    # =====================================================
    # ESTIMATED PRICE
    # =====================================================

    estimated_price = estimate_price(
        followers=followers,
        engagement_rate=engagement_rate,
        platform=platform,
        niche=niche,
    )

    # =====================================================
    # CONFIDENCE SCORE
    # =====================================================

    confidence_score = calculate_confidence_score(
        followers=followers,
        engagement_rate=engagement_rate,
    )

    # =====================================================
    # MARKET LABEL
    # =====================================================

    market_label = generate_market_label(
        price=estimated_price,
        followers=followers,
    )

    # =====================================================
    # AI REASONING
    # =====================================================

    reasoning = generate_explanation(
        niche=niche,
        platform=platform,
        followers=followers,
        engagement_rate=engagement_rate,
        estimated_price=estimated_price,
    )

    # =====================================================
    # SCORECARD
    # =====================================================

    scorecard = generate_scorecard(
        price=estimated_price,
        followers=followers,
        engagement_rate=engagement_rate,
    )

    # =====================================================
    # PRICING REPORT MODEL
    # =====================================================

    report = PricingReport(
        estimated_price=estimated_price,
        confidence_score=confidence_score,
        market_label=market_label,
        reasoning=reasoning,
    )

    return report, scorecard


# =========================================================
# CREATE CREATOR SERVICE
# =========================================================

def create_creator_service(
    db: Session,
    payload: CreatorCreate,
):
    """
    Create creator and compute pricing.
    """

    repo = CreatorRepository(db)

    # =====================================================
    # CREATE ENTITY
    # =====================================================

    creator = Creator(
        name=payload.name,
        niche=payload.niche,
        platform=payload.platform,
        followers=payload.followers,
        engagement_rate=payload.engagement_rate,
    )

    creator = repo.create(creator)

    # =====================================================
    # BUILD REPORT
    # =====================================================

    report, scorecard = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    # =====================================================
    # UPDATE PRICE
    # =====================================================

    creator = repo.update_price(
        creator=creator,
        estimated_price=report.estimated_price,
    )

    # =====================================================
    # COMMIT
    # =====================================================

    db.commit()
    db.refresh(creator)

    # =====================================================
    # ATTACH RESPONSE DATA
    # =====================================================

    creator.pricing_report = {
        "confidence_score": report.confidence_score,
        "market_label": report.market_label,
        "reasoning": report.reasoning,
    }

    creator.scorecard = scorecard

    return creator


# =========================================================
# GET CREATOR PRICING SERVICE
# =========================================================

def get_creator_pricing_service(
    db: Session,
    creator_id: int,
):
    """
    Fetch creator + pricing report.
    """

    repo = CreatorRepository(db)

    creator = repo.get_by_id(creator_id)

    if not creator:
        return None, None

    report, scorecard = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    pricing_data = {
        "estimated_price": report.estimated_price,
        "confidence_score": report.confidence_score,
        "market_label": report.market_label,
        "reasoning": report.reasoning,
        "scorecard": scorecard,
    }

    return creator, pricing_data