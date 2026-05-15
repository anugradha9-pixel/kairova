from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):

    APP_NAME: str = "Kairova"

    DEBUG: bool = True

    DATABASE_URL: str

    REDIS_URL: str = "redis://localhost:6379"

    API_PREFIX: str = "/api"

    LOG_LEVEL: str = "INFO"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()