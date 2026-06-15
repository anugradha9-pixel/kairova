def detect_pattern(data: list[float]) -> str:
    """
    Placeholder for behavioral / pricing pattern detection.
    """
    if not data:
        return "no_data"

    if sum(data) / len(data) > 1000:
        return "high_value_pattern"

    return "normal_pattern"