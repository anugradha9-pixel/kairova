def estimate_price(followers, engagement_rate, platform):

    try:
        followers = float(followers)
        engagement_rate = float(engagement_rate)
    except Exception as e:
        print("❌ Pricing input error:", e)
        return 0

    if followers <= 0:
        return 0

    base_cpm = 12

    platform_multiplier = {
        "instagram": 1.0,
        "tiktok": 1.3,
        "youtube": 2.0
    }

    multiplier = platform_multiplier.get(
        platform.lower() if platform else "",
        1.0
    )

    # normalized engagement (0–100 → 0–1 logic safe)
    engagement_factor = 1 + (engagement_rate / 100)

    estimated_price = (
        (followers / 1000)
        * base_cpm
        * engagement_factor
        * multiplier
    )

    return round(estimated_price, 2)