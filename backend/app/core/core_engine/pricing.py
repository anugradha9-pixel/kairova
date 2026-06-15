from typing import Final


# =====================================
# PRICING CONSTANTS
# =====================================

BASE_CPM: Final[float] = 12.0

PLATFORM_MULTIPLIER = {
    "instagram": 1.2,
    "tiktok": 1.1,
    "youtube": 1.5,
}

NICHE_MULTIPLIER = {
    "finance": 2.0,
    "tech": 1.6,
    "fitness": 1.3,
    "fashion": 1.4,
    "general": 1.0,
}


# =====================================
# PRICE ESTIMATION ENGINE
# =====================================

def estimate_price(
    followers: int | float,
    engagement_rate: int | float,
    platform: str = "instagram",
    niche: str = "general",
) -> float:

    try:
        followers = float(followers or 0)
        engagement_rate = float(engagement_rate or 0)
    except (TypeError, ValueError):
        return 0.0

    followers = max(0.0, followers)
    engagement_rate = max(0.0, min(engagement_rate, 100.0))

    platform = str(platform or "instagram").strip().lower()
    niche = str(niche or "general").strip().lower()

    if followers <= 0:
        return 0.0

    impressions = followers * (engagement_rate / 100.0)

    base_price = (impressions / 1000.0) * BASE_CPM

    platform_mult = PLATFORM_MULTIPLIER.get(platform, 1.0)
    niche_mult = NICHE_MULTIPLIER.get(niche, 1.0)

    estimated_price = base_price * platform_mult * niche_mult

    return round(max(0.0, estimated_price), 2)