from redis.exceptions import RedisError

from app.config.settings import settings
from app.core.redis import redis_client


# =====================================
# SESSION CONFIG
# =====================================

SESSION_EXPIRE_SECONDS = (
    settings.REFRESH_TOKEN_EXPIRE_DAYS
    * 24
    * 60
    * 60
)


# =====================================
# INTERNAL SESSION KEY
# =====================================

def _session_key(session_id: str) -> str:
    return f"session:{session_id}"


# =====================================
# STORE SESSION
# =====================================

def store_session(sid: str, jti: str) -> bool:

    if not sid or not jti:
        return False

    try:
        redis_client.set(
            name=_session_key(sid),
            value=jti,
            ex=SESSION_EXPIRE_SECONDS,
        )
        return True

    except RedisError:
        return False


# =====================================
# GET SESSION JTI
# =====================================

def get_session_jti(sid: str) -> str | None:

    if not sid:
        return None

    try:
        value = redis_client.get(_session_key(sid))

        if value is None:
            return None

        if isinstance(value, bytes):
            return value.decode("utf-8")

        return str(value)

    except RedisError:
        return None


# =====================================
# DELETE SESSION
# =====================================

def delete_session(sid: str) -> bool:

    if not sid:
        return False

    try:
        deleted = redis_client.delete(_session_key(sid))
        return bool(deleted)

    except RedisError:
        return False


# =====================================
# SESSION EXISTS
# =====================================

def session_exists(sid: str) -> bool:

    if not sid:
        return False

    try:
        exists = redis_client.exists(_session_key(sid))
        return bool(exists)

    except RedisError:
        return False