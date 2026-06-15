from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base

from app.config.settings import settings
from app.core.exceptions import AppException
from app.core.handlers import app_exception_handler

from app.schemas.response import APIResponse

from app.api.v1.creator_routes import router as creator_router
from app.api.v1.auth_routes import router as auth_router

# =========================================================
# IMPORTANT:
# IMPORT ORM MODELS BEFORE create_all()
# =========================================================

import app.modules.creator.models

# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


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
# EXCEPTION HANDLER
# =========================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    creator_router,
    prefix="/api/v1",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return APIResponse(
        message="Backend is running",
        data={
            "service": settings.APP_NAME,
            "environment": settings.APP_ENV,
        },
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return APIResponse(
        message="Healthy",
        data={
            "status": "ok",
        },
    )