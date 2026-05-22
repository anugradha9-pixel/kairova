from datetime import (
    datetime,
    timedelta,
    timezone,
)

import uuid
from typing import Any

from jose import (
    JWTError,
    jwt,
)

from passlib.context import CryptContext

from backend.config import settings


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


# =====================================
# PASSWORD HASHING
# =====================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# =====================================
# PASSWORD HELPERS
# =====================================

def hash_password(
    password: str,
) -> str:

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# =====================================
# TIME HELPERS
# =====================================

def utc_now() -> datetime:

    return datetime.now(
        timezone.utc
    )


# =====================================
# BASE PAYLOAD FACTORY
# =====================================

def _create_base_payload(
    user_id: int | str,
    token_type: str,
    session_id: str,
) -> dict[str, Any]:

    return {
        "sub": str(user_id),
        "type": token_type,
        "sid": session_id,
        "jti": str(uuid.uuid4()),
        "iat": int(
            utc_now().timestamp()
        ),
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
        token_type="access",
        session_id=session_id,
    )

    payload.update({
        "exp": expire,
    })

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
        token_type="refresh",
        session_id=session_id,
    )

    payload.update({
        "exp": expire,
    })

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

        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        return payload

    except JWTError:
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

    required_fields = [
        "sub",
        "type",
        "sid",
        "jti",
        "iat",
        "exp",
    ]

    for field in required_fields:

        if payload.get(field) is None:
            return None

    if payload.get("type") != expected_type:
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
        expected_type="access",
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
        expected_type="refresh",
    )