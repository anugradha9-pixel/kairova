from typing import Any

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


# =========================================================
# STANDARD API RESPONSE
# =========================================================

class APIResponse(BaseModel):
    """
    Standard API response wrapper.

    Example:

    {
        "success": true,
        "message": "Request successful",
        "data": {},
        "error": null
    }
    """

    success: bool = Field(
        default=True,
        description="Indicates whether request succeeded.",
    )

    message: str = Field(
        default="Request successful",
        description="Human-readable response message.",
    )

    data: Any | None = Field(
        default=None,
        description="Response payload.",
    )

    error: str | None = Field(
        default=None,
        description="Error details if request failed.",
    )

    # =====================================================
    # PYDANTIC CONFIG
    # =====================================================

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )