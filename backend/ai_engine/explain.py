def generate_explanation(
    niche: str,
    platform: str,
    followers: int,
    engagement_rate: float,
    estimated_price: float,
) -> str:

    reasons = []

    if engagement_rate > 5:
        reasons.append(
            "High engagement rate improves sponsorship value"
        )

    if platform.lower() == "youtube":
        reasons.append(
            "YouTube creators typically command premium CPM rates"
        )

    if followers > 10000:
        reasons.append(
            "Audience scale supports mid-tier sponsorship pricing"
        )

    reasons.append(
        f"Estimated price computed at ${estimated_price}"
    )

    return " | ".join(reasons)