from typing import Any

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from backend.auth.jwt import verify_access_token
from backend.auth.models import User
from backend.db.session import get_db


# =====================================
# SECURITY SCHEME
# =====================================

security = HTTPBearer(
    auto_error=True,
)


# =====================================
# COMMON AUTH EXCEPTION
# =====================================

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token",
    headers={
        "WWW-Authenticate": "Bearer",
    },
)


# =====================================
# TOKEN PAYLOAD
# =====================================

def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
) -> dict[str, Any]:

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise credentials_exception

    return payload


# =====================================
# CURRENT AUTHENTICATED USER
# =====================================

def get_current_user(
    payload: dict[str, Any] = Depends(
        get_token_payload
    ),
    db: Session = Depends(get_db),
) -> User:

    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)

    except (TypeError, ValueError):
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user