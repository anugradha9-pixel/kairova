from typing import Any

from app.core.core_engine.pricing import estimate_price
from app.core.ai.ai_engine.confidence import calculate_confidence_score
from app.core.ai.ai_engine.explain import generate_explanation
from app.core.ai.ai_engine.labeling import generate_market_label


# =====================================
# PRICING SIMULATION ENGINE
# =====================================

def simulate_pricing_scenarios(
    followers: int | float,
    engagement_rate: int | float,
    platform: str | None,
    niche: str = "general",
) -> dict[str, Any]:
    """
    Simulate pricing outcome using full AI pricing pipeline.

    Useful for:
    - Pricing engine debugging
    - Product analytics
    - A/B testing
    - Internal QA validation
    """

    # =====================================
    # INPUT NORMALIZATION
    # =====================================

    try:
        followers = int(float(followers or 0))
    except (TypeError, ValueError):
        followers = 0

    try:
        engagement_rate = float(engagement_rate or 0)
    except (TypeError, ValueError):
        engagement_rate = 0.0

    followers = max(0, followers)
    engagement_rate = max(0.0, min(engagement_rate, 100.0))

    platform = (platform or "").strip().lower()
    niche = (niche or "general").strip().lower()

    # =====================================
    # PRICE ESTIMATION
    # =====================================

    estimated_price = estimate_price(
        followers=followers,
        engagement_rate=engagement_rate,
        platform=platform,
    )

    # =====================================
    # CONFIDENCE SCORE
    # =====================================

    confidence_score = calculate_confidence_score(
        followers=followers,
        engagement_rate=engagement_rate,
    )

    # =====================================
    # MARKET LABEL
    # =====================================

    market_label = generate_market_label(
        price=estimated_price
    )

    # =====================================
    # AI EXPLANATION
    # =====================================

    explanation = generate_explanation(
        niche=niche,
        platform=platform,
        followers=followers,
        engagement_rate=engagement_rate,
        estimated_price=estimated_price,
    )

    # =====================================
    # RESPONSE
    # =====================================

    return {
        "estimated_price": estimated_price,
        "confidence_score": confidence_score,
        "market_label": market_label,
        "reasoning": explanation,
        "inputs": {
            "followers": followers,
            "engagement_rate": engagement_rate,
            "platform": platform,
            "niche": niche,
        },
    }