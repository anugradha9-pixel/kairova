def calculate_confidence_score(
    followers: int,
    engagement_rate: float,
) -> float:
    """
    Calculate confidence score for creator pricing.
    """

    score = 0.5

    # Follower confidence
    if followers >= 100000:
        score += 0.25
    elif followers >= 50000:
        score += 0.15
    elif followers >= 10000:
        score += 0.10

    # Engagement confidence
    if engagement_rate >= 5:
        score += 0.25
    elif engagement_rate >= 3:
        score += 0.15
    elif engagement_rate >= 1:
        score += 0.10

    return round(min(score, 1.0), 2)