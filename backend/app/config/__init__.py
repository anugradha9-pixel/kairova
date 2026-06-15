from app.config.settings import settings


# =========================
# APP CORE
# =========================

APP_NAME = settings.APP_NAME
APP_ENV = settings.APP_ENV
DEBUG = settings.DEBUG
LOG_LEVEL = settings.LOG_LEVEL
API_PREFIX = settings.API_PREFIX


# =========================
# DATABASE / CACHE
# =========================

DATABASE_URL = settings.DATABASE_URL
REDIS_URL = settings.REDIS_URL


# =========================
# JWT / AUTH
# =========================

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
SESSION_EXPIRE_DAYS = settings.SESSION_EXPIRE_DAYS


# =========================
# PRICING ENGINE CONFIG
# =========================

DEFAULT_TARGET_MARGIN_PERCENT = getattr(
    settings,
    "DEFAULT_TARGET_MARGIN_PERCENT",
    30.0,
)


# =========================
# EXPORT CONTROL
# =========================

__all__ = [
    "settings",

    # App
    "APP_NAME",
    "APP_ENV",
    "DEBUG",
    "LOG_LEVEL",
    "API_PREFIX",

    # Database
    "DATABASE_URL",
    "REDIS_URL",

    # JWT
    "JWT_SECRET",
    "JWT_ALGORITHM",
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS",
    "SESSION_EXPIRE_DAYS",

    # Pricing
    "DEFAULT_TARGET_MARGIN_PERCENT",
]