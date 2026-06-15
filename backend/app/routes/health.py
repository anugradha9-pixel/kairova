from fastapi import APIRouter

from app.config.settings import settings

from app.schemas.response import APIResponse


router = APIRouter(
    tags=["Health"],
)


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get(
    "/health",
    response_model=APIResponse,
)
async def healthcheck():
    """
    Basic health check endpoint.

    Used for:
    - Docker health checks
    - uptime monitoring
    - load balancer checks
    """

    return APIResponse(
        message="Health check successful",
        data={
            "status": "ok",
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "version": "1.0.0",
        },
    )