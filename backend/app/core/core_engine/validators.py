from typing import Any


# =====================================
# SUPPORTED PLATFORMS
# =====================================

SUPPORTED_PLATFORMS = {
    "instagram",
    "tiktok",
    "youtube",
}


# =====================================
# INPUT VALIDATION
# =====================================

def validate_creator_input(
    followers: Any,
    engagement_rate: Any,
    platform: Any,
) -> dict[str, Any]:
    """
    Central validation layer for creator pricing inputs.

    Returns:
        dict:
            Cleaned and validated creator input payload
    """

    # =====================================
    # FOLLOWERS
    # =====================================

    try:
        followers = float(followers or 0)
    except (TypeError, ValueError):
        followers = 0.0

    followers = max(0.0, followers)

    # =====================================
    # ENGAGEMENT RATE
    # =====================================

    try:
        engagement_rate = float(engagement_rate or 0)
    except (TypeError, ValueError):
        engagement_rate = 0.0

    engagement_rate = max(0.0, min(engagement_rate, 100.0))

    # =====================================
    # PLATFORM NORMALIZATION
    # =====================================

    platform = str(platform or "").strip().lower()

    if not platform:
        platform = "instagram"

    # =====================================
    # PLATFORM VALIDATION FLAG
    # =====================================

    is_supported_platform = platform in SUPPORTED_PLATFORMS

    # =====================================
    # RESPONSE
    # =====================================

    return {
        "followers": followers,
        "engagement_rate": engagement_rate,
        "platform": platform,
        "is_supported_platform": is_supported_platform,
    }