from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


# =========================================================
# GLOBAL EXCEPTION HANDLER
# =========================================================

async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Global exception handler for all AppException errors.

    Ensures consistent API error format across the entire backend.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "code": exc.error_code,
                "details": exc.details,
            },
            "path": str(request.url),
        },
    )