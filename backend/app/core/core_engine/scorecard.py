def generate_scorecard(
    price,
    followers,
    engagement_rate,
):
    """
    Generate creator business scorecard.
    """

    tier = (
        "micro"
        if followers < 10000
        else "mid"
        if followers < 100000
        else "macro"
    )

    quality_score = min(
        100,
        (
            engagement_rate * 10
        ) + (
            followers / 10000
        ),
    )

    confidence = min(
        0.99,
        max(
            0.3,
            engagement_rate / 10,
        ),
    )

    market_position = (
        "premium"
        if quality_score > 70
        else "average"
        if quality_score > 40
        else "low"
    )

    recommendation = (
        "strong for brand deals"
        if quality_score > 70
        else "good potential"
        if quality_score > 40
        else "needs growth"
    )

    return {
        "price": price,
        "tier": tier,
        "quality_score": round(
            quality_score,
            2,
        ),
        "confidence": round(
            confidence,
            2,
        ),
        "market_position": market_position,
        "recommendation": recommendation,
    }