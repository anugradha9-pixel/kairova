def explain_price(followers, engagement_rate, platform, price):

    reasons = []

    if engagement_rate > 5:
        reasons.append("High engagement increases brand value")

    if followers > 100000:
        reasons.append("Large audience scale increases CPM")

    if platform.lower() == "tiktok":
        reasons.append("TikTok virality multiplier applied")

    if price > 1000:
        reasons.append("Premium creator category detected")

    return reasons