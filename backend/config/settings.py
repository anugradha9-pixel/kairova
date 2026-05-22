from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # =====================================
    # APP CORE
    # =====================================

    APP_NAME: str = "Kairova"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    API_PREFIX: str = "/api"

    # =====================================
    # DATABASE
    # =====================================

    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL connection URL",
    )

    # =====================================
    # REDIS
    # =====================================

    REDIS_URL: str = Field(
        default="redis://redis:6379/0",
        description="Redis connection URL",
    )

    # =====================================
    # JWT / AUTH
    # =====================================

    JWT_SECRET: str = Field(
        ...,
        description="Secret key for JWT signing",
    )

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # =====================================
    # SESSION STORAGE
    # =====================================

    SESSION_EXPIRE_DAYS: int = 7

    # =====================================
    # OPTIONAL SERVICES
    # =====================================

    STRIPE_SECRET: str | None = None

    # =====================================
    # PYDANTIC CONFIG
    # =====================================

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
        env_ignore_empty=True,
    )


# =====================================
# GLOBAL SETTINGS INSTANCE
# =====================================

settings = Settings()