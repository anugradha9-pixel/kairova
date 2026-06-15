def generate_explanation(
    niche: str,
    platform: str,
    followers: int | float,
    engagement_rate: int | float,
    estimated_price: float,
) -> str:
    """
    Generate human-readable pricing explanation for creator valuation.
    """

    reasons = []

    # =====================================
    # INPUT SANITIZATION (STANDARDIZED)
    # =====================================

    try:
        followers = float(followers or 0)
        engagement_rate = float(engagement_rate or 0)
        estimated_price = float(estimated_price or 0)
    except Exception:
        followers = 0.0
        engagement_rate = 0.0
        estimated_price = 0.0

    niche = (niche or "").strip().lower()
    platform = (platform or "").strip().lower()

    followers = max(0.0, followers)
    engagement_rate = max(0.0, min(engagement_rate, 100.0))

    # =====================================
    # ENGAGEMENT SIGNAL
    # =====================================

    if engagement_rate >= 8:
        reasons.append("Exceptional engagement rate significantly increases brand value")
    elif engagement_rate >= 5:
        reasons.append("High engagement rate improves sponsorship conversion potential")
    elif engagement_rate >= 2:
        reasons.append("Moderate engagement rate supports stable monetization potential")
    else:
        reasons.append("Low engagement rate reduces sponsorship efficiency")

    # =====================================
    # PLATFORM FACTOR
    # =====================================

    if platform == "youtube":
        reasons.append("YouTube creators benefit from premium CPM-based monetization")

    elif platform == "instagram":
        reasons.append("Instagram creators perform well in brand sponsorship campaigns")

    elif platform == "tiktok":
        reasons.append("TikTok creators gain value from viral reach and discovery algorithm")

    elif platform:
        reasons.append(f"{platform.title()} platform pricing modeled using general benchmarks")

    else:
        reasons.append("Platform not specified, using generic pricing model")

    # =====================================
    # AUDIENCE SCALE FACTOR
    # =====================================

    if followers >= 1_000_000:
        reasons.append("Massive audience scale qualifies for top-tier brand deals")

    elif followers >= 100_000:
        reasons.append("Large audience supports high-value sponsorship opportunities")

    elif followers >= 10_000:
        reasons.append("Mid-tier audience suitable for consistent brand collaborations")

    elif followers >= 1_000:
        reasons.append("Small but engaged audience suitable for niche partnerships")

    else:
        reasons.append("Early-stage creator with limited monetization power")

    # =====================================
    # NICHE CONTEXT
    # =====================================

    if niche:
        reasons.append(f"Niche specialization in {niche} improves targeting efficiency")

    # =====================================
    # PRICE OUTPUT
    # =====================================

    reasons.append(f"Final estimated valuation: ${estimated_price:,.2f}")

    return " | ".join(reasons)