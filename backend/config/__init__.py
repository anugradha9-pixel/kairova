from backend.config.settings import settings


# =========================
# JWT / AUTH EXPORTS
# =========================

JWT_SECRET = settings.JWT_SECRET

JWT_ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

REFRESH_TOKEN_EXPIRE_DAYS = (
    settings.REFRESH_TOKEN_EXPIRE_DAYS
)

SESSION_EXPIRE_DAYS = (
    settings.SESSION_EXPIRE_DAYS
)


# =========================
# APP EXPORTS
# =========================

APP_NAME = settings.APP_NAME

APP_ENV = settings.APP_ENV

DEBUG = settings.DEBUG

LOG_LEVEL = settings.LOG_LEVEL

API_PREFIX = settings.API_PREFIX


# =========================
# DATABASE / CACHE EXPORTS
# =========================

DATABASE_URL = settings.DATABASE_URL

REDIS_URL = settings.REDIS_URL


# =========================
# EXPORT CONTROL
# =========================

__all__ = [
    "settings",
    # JWT
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    "SESSION_EXPIRE_DAYS",
    # App
    "APP_NAME",
    "APP_ENV",
    "DEBUG",
    "LOG_LEVEL",
    "API_PREFIX",
    # Infra
    "DATABASE_URL",
    "REDIS_URL",
]