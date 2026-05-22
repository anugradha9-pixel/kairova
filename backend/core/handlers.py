from fastapi import Request
from fastapi.responses import JSONResponse

from backend.core.exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException):
    """
    Global exception handler for all AppException errors.
    Ensures consistent API error format across backend.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "code": getattr(exc, "error_code", "app_error"),
                "details": getattr(exc, "details", None),
            },
            "path": str(request.url),
        },
    )