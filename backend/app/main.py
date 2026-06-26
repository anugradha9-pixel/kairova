from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings

from app.core.exceptions import AppException
from app.core.handlers import app_exception_handler

from app.schemas.response import APIResponse


# =========================================================
# ROUTERS
# =========================================================

from app.api.v1.creator_routes import router as creator_router
from app.api.v1.user_routes import router as user_router

from app.auth.routes import router as auth_router

from app.api.v1.test_routes import router as test_router


# =========================================================
# IMPORT ORM MODELS
# IMPORTANT:
# Must be imported before metadata initialization
# =========================================================

import app.auth.models
import app.auth.session_models
import app.modules.creator.models


# =========================================================
# APP INITIALIZATION
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="MakerMint Backend API",
    docs_url="/docs",
    redoc_url="/redoc",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# EXCEPTION HANDLERS
# =========================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# =========================================================
# API ROUTES
# =========================================================

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    creator_router,
    prefix="/api/v1",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)

app.include_router(
    test_router,
    prefix="/api/v1",
)


# =========================================================
# DEBUG ROUTES
# =========================================================

if settings.APP_ENV.lower() != "production":

    @app.get("/debug/routes")
    def list_routes():
        """
        Development-only route inspection.
        """

        routes = []

        for route in app.routes:
            if hasattr(route, "path"):

                routes.append(
                    {
                        "path": route.path,
                        "name": route.name,
                        "methods": (
                            list(route.methods)
                            if hasattr(route, "methods")
                            else None
                        ),
                    }
                )

        return APIResponse(
            message="Registered routes",
            data=routes,
        )


# =========================================================
# ROOT
# =========================================================

@app.get(
    "/",
    response_model=APIResponse,
)
def root():

    return APIResponse(
        message="Backend is running",
        data={
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
        },
    )


# =========================================================
# HEALTH
# =========================================================

@app.get(
    "/health",
    response_model=APIResponse,
)
def health():

    return APIResponse(
        message="Healthy",
        data={
            "status": "ok",
        },
    )