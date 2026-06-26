from datetime import (
    datetime,
    timedelta,
    timezone,
)

import uuid
from typing import Any

from jose import (
    JWTError,
    ExpiredSignatureError,
    jwt,
)

from passlib.context import CryptContext

from app.config.settings import settings


# =====================================
# JWT CONFIG
# =====================================

JWT_SECRET = settings.JWT_SECRET

JWT_ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

REFRESH_TOKEN_EXPIRE_DAYS = (
    settings.REFRESH_TOKEN_EXPIRE_DAYS
)

ACCESS_TOKEN_TYPE = "access"

REFRESH_TOKEN_TYPE = "refresh"


# =====================================
# PASSWORD HASHING
# =====================================

pwd_context = CryptContext(
    schemes=["bcrypt_sha256"],
    deprecated="auto",
)


# =====================================
# PASSWORD HELPERS
# =====================================

def hash_password(
    password: str,
) -> str:
    return pwd_context.hash(
        password.strip()
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password.strip(),
        hashed_password,
    )


# =====================================
# TIME HELPERS
# =====================================

def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


def utc_timestamp() -> int:
    return int(
        utc_now().timestamp()
    )


# =====================================
# BASE PAYLOAD FACTORY
# =====================================

def _create_base_payload(
    user_id: int | str,
    token_type: str,
    session_id: str,
) -> dict[str, Any]:

    if not user_id:
        raise ValueError(
            "user_id is required"
        )

    if not session_id:
        raise ValueError(
            "session_id is required"
        )

    if token_type not in (
        ACCESS_TOKEN_TYPE,
        REFRESH_TOKEN_TYPE,
    ):
        raise ValueError(
            "invalid token type"
        )

    return {
        "sub": str(user_id),
        "type": token_type,
        "sid": session_id,
        "jti": str(uuid.uuid4()),
        "iat": utc_timestamp(),
    }


# =====================================
# ACCESS TOKEN
# =====================================

def create_access_token(
    user_id: int | str,
    session_id: str,
) -> str:

    expire = utc_now() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = _create_base_payload(
        user_id=user_id,
        token_type=ACCESS_TOKEN_TYPE,
        session_id=session_id,
    )

    payload["exp"] = int(
        expire.timestamp()
    )

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


# =====================================
# REFRESH TOKEN
# =====================================

def create_refresh_token(
    user_id: int | str,
    session_id: str,
) -> str:

    expire = utc_now() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = _create_base_payload(
        user_id=user_id,
        token_type=REFRESH_TOKEN_TYPE,
        session_id=session_id,
    )

    payload["exp"] = int(
        expire.timestamp()
    )

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )


# =====================================
# TOKEN DECODING
# =====================================

def decode_token(
    token: str,
) -> dict[str, Any] | None:

    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

    except ExpiredSignatureError:
        return None

    except JWTError:
        return None

    except Exception:
        return None


# =====================================
# PAYLOAD VALIDATION
# =====================================

def _validate_payload(
    payload: dict[str, Any] | None,
    expected_type: str,
) -> dict[str, Any] | None:

    if payload is None:
        return None

    required_fields = (
        "sub",
        "type",
        "sid",
        "jti",
        "iat",
        "exp",
    )

    for field in required_fields:
        if payload.get(field) is None:
            return None

    if payload["type"] != expected_type:
        return None

    if not str(payload["sub"]).strip():
        return None

    if not str(payload["sid"]).strip():
        return None

    if not str(payload["jti"]).strip():
        return None

    try:
        exp = int(payload["exp"])

    except (
        TypeError,
        ValueError,
    ):
        return None

    if exp < utc_timestamp():
        return None

    return payload


# =====================================
# ACCESS TOKEN VERIFY
# =====================================

def verify_access_token(
    token: str,
) -> dict[str, Any] | None:

    payload = decode_token(
        token
    )

    return _validate_payload(
        payload=payload,
        expected_type=ACCESS_TOKEN_TYPE,
    )


# =====================================
# REFRESH TOKEN VERIFY
# =====================================

def verify_refresh_token(
    token: str,
) -> dict[str, Any] | None:

    payload = decode_token(
        token
    )

    return _validate_payload(
        payload=payload,
        expected_type=REFRESH_TOKEN_TYPE,
    )