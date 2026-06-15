from typing import Any


def normalize_float(value: Any, default: float = 0.0) -> float:
    """
    Safely converts input to float.
    """

    try:
        return float(value)
    except Exception:
        return default


def normalize_int(value: Any, default: int = 0) -> int:
    """
    Safely converts input to int.
    """

    try:
        return int(value)
    except Exception:
        return default


def normalize_str(value: Any, default: str = "") -> str:
    """
    Safely converts input to cleaned lowercase string.
    """

    if value is None:
        return default

    return str(value).strip().lower()