from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # =====================================
    # APP CORE
    # =====================================

    APP_NAME: str = "MakerMint"
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
        min_length=20,
        description="Secret key for JWT signing",
    )

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=15,
        ge=1,
        le=60 * 24,
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        ge=1,
        le=30,
    )

    # =====================================
    # SESSION STORAGE
    # =====================================

    SESSION_EXPIRE_DAYS: int = Field(
        default=7,
        ge=1,
        le=30,
    )

    # =====================================
    # OPTIONAL SERVICES
    # =====================================

    STRIPE_SECRET: str | None = None

    # =====================================
    # PRICING ENGINE
    # =====================================

    DEFAULT_TARGET_MARGIN_PERCENT: float = Field(
        default=30.0,
        ge=0,
        le=100,
    )

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