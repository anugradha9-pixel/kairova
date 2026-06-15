from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)


# =========================================================
# STANDARD API RESPONSE
# =========================================================

class APIResponse(BaseModel):
    """
    Standardized API response wrapper.

    Example:
    {
        "success": true,
        "message": "Request successful",
        "data": {},
        "error": null
    }
    """

    success: bool = True

    message: str = "Request successful"

    data: Any | None = None

    error: str | None = None

    # =====================================================
    # PYDANTIC CONFIG
    # =====================================================

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )