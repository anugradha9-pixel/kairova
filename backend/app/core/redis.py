from redis import Redis
from redis.exceptions import (
    ConnectionError,
    RedisError,
    TimeoutError,
)

from app.config import settings


# =========================================================
# REDIS CLIENT
# =========================================================

redis_client: Redis = Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    health_check_interval=30,
    retry_on_timeout=True,
)


# =========================================================
# REDIS HEALTH CHECK
# =========================================================

def check_redis_connection() -> bool:
    """
    Lightweight Redis health check.

    Used for:
    - startup validation
    - health endpoints
    - monitoring
    """

    try:
        return redis_client.ping() is True

    except (ConnectionError, TimeoutError, RedisError):
        return False