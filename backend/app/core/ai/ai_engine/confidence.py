def calculate_confidence_score(
    followers: int,
    engagement_rate: float,
) -> float:
    """
    Calculate pricing confidence score.

    Returns:
        float: Confidence score between 0.0 and 1.0
    """

    # =====================================
    # INPUT SAFETY (STRICT CASTING)
    # =====================================

    try:
        followers = int(followers or 0)
    except Exception:
        followers = 0

    try:
        engagement_rate = float(engagement_rate or 0)
    except Exception:
        engagement_rate = 0.0

    followers = max(0, followers)
    engagement_rate = max(0.0, engagement_rate)

    # =====================================
    # BASE SCORE
    # =====================================

    score = 0.40

    # =====================================
    # FOLLOWER CONFIDENCE
    # =====================================

    if followers >= 1_000_000:
        score += 0.30

    elif followers >= 100_000:
        score += 0.25

    elif followers >= 50_000:
        score += 0.18

    elif followers >= 10_000:
        score += 0.12

    elif followers >= 1_000:
        score += 0.06

    # =====================================
    # ENGAGEMENT CONFIDENCE
    # =====================================

    if engagement_rate >= 8:
        score += 0.30

    elif engagement_rate >= 5:
        score += 0.25

    elif engagement_rate >= 3:
        score += 0.18

    elif engagement_rate >= 1:
        score += 0.10

    # =====================================
    # FINAL NORMALIZATION
    # =====================================

    score = min(score, 1.0)

    return round(score, 2)