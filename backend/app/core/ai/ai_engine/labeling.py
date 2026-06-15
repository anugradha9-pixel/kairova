def generate_market_label(
    price: float,
    followers: int,
) -> str:
    """
    Classify creator based on audience size.
    """

    try:
        followers = int(followers or 0)
    except (TypeError, ValueError):
        followers = 0

    followers = max(0, followers)

    if followers < 10_000:
        return "Nano Creator"

    if followers < 100_000:
        return "Micro Creator"

    if followers < 1_000_000:
        return "Macro Creator"

    return "Mega Creator"