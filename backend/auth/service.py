from datetime import datetime, timezone
import uuid

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from backend.auth.jwt import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)

from backend.auth.models import User

from backend.auth.schemas import TokenPair

from backend.auth.utils import (
    delete_session,
    get_session_jti,
    store_session,
)


# =====================================
# COMMON AUTH EXCEPTION
# =====================================

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
)

INVALID_REFRESH_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid refresh token",
)


# =====================================
# CREATE USER
# =====================================

def create_user(
    db: Session,
    email: str,
    password: str,
) -> User:

    email = email.lower().strip()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    user = User(
        email=email,
        password_hash=hash_password(password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )


# =====================================
# AUTHENTICATE USER
# =====================================

def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:

    email = email.lower().strip()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise INVALID_CREDENTIALS_EXCEPTION

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise INVALID_CREDENTIALS_EXCEPTION

    return user


# =====================================
# CREATE TOKEN PAIR
# =====================================

def create_user_tokens(
    user_id: int,
) -> TokenPair:

    session_id = str(uuid.uuid4())

    access_token = create_access_token(
        user_id=user_id,
        session_id=session_id,
    )

    refresh_token = create_refresh_token(
        user_id=user_id,
        session_id=session_id,
    )

    refresh_payload = verify_refresh_token(
        refresh_token
    )

    if refresh_payload is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate refresh token",
        )

    token_jti = refresh_payload.get("jti")

    if token_jti is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid refresh token payload",
        )

    store_session(
        sid=session_id,
        jti=token_jti,
    )

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


# =====================================
# LOGIN FLOW
# =====================================

def login_user(
    db: Session,
    email: str,
    password: str,
) -> TokenPair:

    user = authenticate_user(
        db=db,
        email=email,
        password=password,
    )

    try:
        user.last_login_at = datetime.now(
            timezone.utc
        )

        db.commit()

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update login timestamp",
        )

    return create_user_tokens(
        user_id=user.id,
    )


# =====================================
# REFRESH FLOW
# ROTATION + REPLAY PROTECTION
# =====================================

def refresh_user_tokens(
    refresh_token: str,
) -> TokenPair:

    payload = verify_refresh_token(
        refresh_token
    )

    if payload is None:
        raise INVALID_REFRESH_EXCEPTION

    user_id = payload.get("sub")
    session_id = payload.get("sid")
    token_jti = payload.get("jti")

    if not all([
        user_id,
        session_id,
        token_jti,
    ]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    stored_jti = get_session_jti(
        session_id
    )

    # Session expired or revoked
    if stored_jti is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
        )

    # Replay attack protection
    if stored_jti != token_jti:

        # Kill entire session immediately
        delete_session(session_id)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reuse detected",
        )

    # Rotate tokens
    new_access_token = create_access_token(
        user_id=user_id,
        session_id=session_id,
    )

    new_refresh_token = create_refresh_token(
        user_id=user_id,
        session_id=session_id,
    )

    new_payload = verify_refresh_token(
        new_refresh_token
    )

    if new_payload is None:

        delete_session(session_id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token rotation failed",
        )

    new_jti = new_payload.get("jti")

    if new_jti is None:

        delete_session(session_id)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid rotated token payload",
        )

    # Replace stored JTI
    store_session(
        sid=session_id,
        jti=new_jti,
    )

    return TokenPair(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


# =====================================
# LOGOUT FLOW
# =====================================

def logout_user(
    refresh_token: str,
) -> None:

    payload = verify_refresh_token(
        refresh_token
    )

    if payload is None:
        raise INVALID_REFRESH_EXCEPTION

    session_id = payload.get("sid")

    if session_id:
        delete_session(session_id)