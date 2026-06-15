from typing import List


def explain_price(
    followers: int,
    engagement_rate: float,
    platform: str,
    price: float,
) -> List[str]:
    """
    Generate structured pricing reasoning
    for creator valuation engine.

    Returns:
        List[str]: Ordered explanation factors
    """

    reasons: List[str] = []

    # =====================================
    # INPUT SAFETY (STANDARDIZED CASTING)
    # =====================================

    try:
        followers = int(followers or 0)
    except Exception:
        followers = 0

    try:
        engagement_rate = float(engagement_rate or 0)
    except Exception:
        engagement_rate = 0.0

    try:
        price = float(price or 0)
    except Exception:
        price = 0.0

    platform = (platform or "").strip().lower()

    followers = max(0, followers)
    engagement_rate = max(0.0, engagement_rate)
    price = max(0.0, price)

    # =====================================
    # ENGAGEMENT FACTOR
    # =====================================

    if engagement_rate >= 8:
        reasons.append(
            "Exceptional engagement rate strongly increases brand value"
        )

    elif engagement_rate >= 5:
        reasons.append(
            "High engagement rate improves sponsorship conversion"
        )

    elif engagement_rate >= 2:
        reasons.append(
            "Moderate engagement supports stable monetization"
        )

    else:
        reasons.append(
            "Low engagement reduces advertising efficiency"
        )

    # =====================================
    # AUDIENCE SIZE FACTOR
    # =====================================

    if followers >= 1_000_000:
        reasons.append(
            "Massive audience scale qualifies for top-tier brand deals"
        )

    elif followers >= 100_000:
        reasons.append(
            "Large audience increases CPM and sponsorship demand"
        )

    elif followers >= 10_000:
        reasons.append(
            "Mid-tier audience suitable for brand collaborations"
        )

    elif followers >= 1_000:
        reasons.append(
            "Small audience with niche targeting potential"
        )

    else:
        reasons.append(
            "Early-stage creator with limited monetization history"
        )

    # =====================================
    # PLATFORM FACTOR
    # =====================================

    if platform == "tiktok":
        reasons.append(
            "TikTok virality multiplier increases exposure potential"
        )

    elif platform == "youtube":
        reasons.append(
            "YouTube supports high CPM long-form monetization"
        )

    elif platform == "instagram":
        reasons.append(
            "Instagram optimized for brand sponsorship campaigns"
        )

    elif platform:
        reasons.append(
            f"{platform.title()} platform evaluated using benchmark pricing model"
        )

    else:
        reasons.append(
            "Platform not specified, using general benchmark model"
        )

    # =====================================
    # PRICE SIGNAL FACTOR
    # =====================================

    if price >= 100_000:
        reasons.append(
            "Ultra-premium creator pricing tier detected"
        )

    elif price >= 10_000:
        reasons.append(
            "High-value creator category identified"
        )

    elif price >= 1_000:
        reasons.append(
            "Premium creator category detected"
        )

    else:
        reasons.append(
            "Entry-level or emerging creator pricing range"
        )

    # =====================================
    # REMOVE DUPLICATES (SAFEGUARD)
    # =====================================

    unique_reasons = list(dict.fromkeys(reasons))

    return unique_reasons