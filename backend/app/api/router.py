from fastapi import APIRouter

from app.api.v1.creator_routes import (
    router as creator_router,
)


# =====================================
# MAIN API ROUTER
# =====================================

api_router = APIRouter()


# =====================================
# VERSION 1 ROUTES
# =====================================

api_router.include_router(
    creator_router,
    prefix="/v1/creators",
    tags=["Creators"],
)