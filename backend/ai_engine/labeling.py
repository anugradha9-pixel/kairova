def generate_market_label(
    price: float
) -> str:

    if price < 500:
        return "Nano Creator"

    elif price < 5000:
        return "Mid-tier Creator"

    return "Premium Creator"