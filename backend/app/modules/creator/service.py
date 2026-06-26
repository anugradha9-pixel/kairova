from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User

from app.modules.creator.domain import PricingReport
from app.modules.creator.models import Creator
from app.modules.creator.repository import CreatorRepository
from app.modules.creator.schemas import (
    CreatorCreate,
    CreatorUpdateRequest,
)

from app.core.core_engine.pricing import estimate_price
from app.core.core_engine.scorecard import generate_scorecard

from app.core.ai.ai_engine.confidence import calculate_confidence_score
from app.core.ai.ai_engine.labeling import generate_market_label
from app.core.ai.ai_engine.explain import generate_explanation


# =========================================================
# INTERNAL: PRICING PIPELINE
# =========================================================

def _build_pricing_report(
    followers: int,
    engagement_rate: float,
    platform: str,
    niche: str,
):

    estimated_price = estimate_price(
        followers=followers,
        engagement_rate=engagement_rate,
        platform=platform,
        niche=niche,
    )

    confidence_score = calculate_confidence_score(
        followers=followers,
        engagement_rate=engagement_rate,
    )

    market_label = generate_market_label(
        price=estimated_price,
        followers=followers,
    )

    reasoning = generate_explanation(
        niche=niche,
        platform=platform,
        followers=followers,
        engagement_rate=engagement_rate,
        estimated_price=estimated_price,
    )

    scorecard = generate_scorecard(
        price=estimated_price,
        followers=followers,
        engagement_rate=engagement_rate,
    )

    report = PricingReport(
        estimated_price=estimated_price,
        confidence_score=confidence_score,
        market_label=market_label,
        reasoning=reasoning,
    )

    return report, scorecard


# =========================================================
# PERMISSIONS
# =========================================================

def verify_creator_access(
    creator: Creator,
    current_user: User,
):

    if current_user.is_admin:
        return

    if creator.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )


# =========================================================
# CREATE CREATOR
# =========================================================

def create_creator_service(
    db: Session,
    payload: CreatorCreate,
    current_user: User,
):

    repo = CreatorRepository(db)

    creator = Creator(
        user_id=current_user.id,
        name=payload.name,
        niche=payload.niche,
        platform=payload.platform,
        followers=payload.followers,
        engagement_rate=payload.engagement_rate,
    )

    creator = repo.create(creator)

    report, scorecard = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    creator = repo.update_price(
        creator=creator,
        estimated_price=report.estimated_price,
    )

    db.commit()
    db.refresh(creator)

    creator.pricing_report = {
        "confidence_score": report.confidence_score,
        "market_label": report.market_label,
        "reasoning": report.reasoning,
    }

    creator.scorecard = scorecard

    return creator


# =========================================================
# GET CREATOR
# =========================================================

def get_creator_by_id_service(
    db: Session,
    creator_id: int,
):

    repo = CreatorRepository(db)

    return repo.get_by_id(
        creator_id,
    )


# =========================================================
# GET MY CREATORS
# =========================================================

def get_my_creators_service(
    db: Session,
    current_user: User,
):

    repo = CreatorRepository(db)

    return repo.get_by_user(
        current_user.id,
    )


# =========================================================
# UPDATE CREATOR
# =========================================================

def update_creator_service(
    db: Session,
    creator_id: int,
    payload: CreatorUpdateRequest,
    current_user: User,
):

    repo = CreatorRepository(db)

    creator = repo.get_by_id(
        creator_id,
    )

    if not creator:
        raise HTTPException(
            status_code=404,
            detail="Creator not found",
        )

    verify_creator_access(
        creator,
        current_user,
    )

    update_data = payload.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(
            creator,
            field,
            value,
        )

    report, _ = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    creator.estimated_price = (
        report.estimated_price
    )

    creator = repo.update_creator(
        creator,
    )

    db.commit()
    db.refresh(creator)

    return creator


# =========================================================
# DELETE CREATOR
# =========================================================

def delete_creator_service(
    db: Session,
    creator_id: int,
    current_user: User,
):

    repo = CreatorRepository(db)

    creator = repo.get_by_id(
        creator_id,
    )

    if not creator:
        raise HTTPException(
            status_code=404,
            detail="Creator not found",
        )

    verify_creator_access(
        creator,
        current_user,
    )

    repo.delete_creator(
        creator,
    )

    db.commit()

    return {
        "message": "Creator deleted successfully",
    }


# =========================================================
# GET CREATOR PRICING
# =========================================================

def get_creator_pricing_service(
    db: Session,
    creator_id: int,
):

    repo = CreatorRepository(db)

    creator = repo.get_by_id(
        creator_id,
    )

    if not creator:
        return None

    report, scorecard = _build_pricing_report(
        followers=creator.followers,
        engagement_rate=creator.engagement_rate,
        platform=creator.platform,
        niche=creator.niche,
    )

    return {
        "estimated_price": report.estimated_price,
        "confidence_score": report.confidence_score,
        "market_label": report.market_label,
        "reasoning": report.reasoning,
        "scorecard": scorecard,
    }