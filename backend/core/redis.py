from redis import Redis
from redis.exceptions import (
    ConnectionError,
    RedisError,
    TimeoutError,
)

from backend.config import settings


# =========================
# REDIS CLIENT
# =========================

redis_client = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    health_check_interval=30,
    retry_on_timeout=True,
)


# =========================
# REDIS HEALTH CHECK
# =========================

def check_redis_connection() -> bool:
    """
    Lightweight Redis health check.
    Used for startup validation
    and monitoring endpoints.
    """

    try:
        return redis_client.ping() is True

    except (
        ConnectionError,
        TimeoutError,
        RedisError,
    ):
        return False