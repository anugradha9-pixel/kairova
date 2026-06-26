from datetime import (
    datetime,
    timezone,
    timedelta,
)

import uuid

from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import TokenPair
from app.auth.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)
from app.auth.repository import AuthRepository
from app.config.settings import settings


# =====================================
# COMMON EXCEPTIONS
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
    repo = AuthRepository(db)

    email = email.lower().strip()

    existing_user = repo.get_user_by_email(email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    try:
        return repo.create_user(
            {
                "email": email,
                "hashed_password": hash_password(password),
            }
        )

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
    repo = AuthRepository(db)

    email = email.lower().strip()

    user = repo.get_user_by_email(email)

    if not user:
        raise INVALID_CREDENTIALS_EXCEPTION

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise INVALID_CREDENTIALS_EXCEPTION

    return user


# =====================================
# CREATE TOKEN PAIR
# =====================================

def create_user_tokens(
    db: Session,
    user_id: int,
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> TokenPair:
    repo = AuthRepository(db)

    max_sessions = getattr(
        settings,
        "MAX_ACTIVE_SESSIONS",
        None,
    )

    if max_sessions:
        active_count = repo.count_user_active_sessions(
            user_id
        )

        if active_count >= max_sessions:
            repo.revoke_oldest_active_session(
                user_id
            )

    session_id = str(uuid.uuid4())

    access_token = create_access_token(
        user_id=user_id,
        session_id=session_id,
    )

    refresh_token = create_refresh_token(
        user_id=user_id,
        session_id=session_id,
    )

    payload = verify_refresh_token(
        refresh_token
    )

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate refresh token",
        )

    refresh_jti = payload.get("jti")

    if not refresh_jti:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid refresh token payload",
        )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.SESSION_EXPIRE_DAYS
        )
    )

    try:
        repo.create_session(
            user_id=user_id,
            session_id=session_id,
            refresh_jti=refresh_jti,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create session",
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
    ip_address: str | None = None,
    user_agent: str | None = None,
) -> TokenPair:
    user = authenticate_user(
        db=db,
        email=email,
        password=password,
    )

    return create_user_tokens(
        db=db,
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )


# =====================================
# REFRESH FLOW
# =====================================

def refresh_user_tokens(
    db: Session,
    refresh_token: str,
) -> TokenPair:
    repo = AuthRepository(db)

    payload = verify_refresh_token(
        refresh_token
    )

    if not payload:
        raise INVALID_REFRESH_EXCEPTION

    user_id = payload.get("sub")
    session_id = payload.get("sid")
    refresh_jti = payload.get("jti")

    if not all(
        [
            user_id,
            session_id,
            refresh_jti,
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    try:
        user_id = int(user_id)

    except (
        TypeError,
        ValueError,
    ):
        raise INVALID_REFRESH_EXCEPTION

    user = repo.get_user_by_id(
        user_id
    )

    if not user:
        raise INVALID_REFRESH_EXCEPTION

    session = repo.get_session_by_session_id(
        session_id
    )

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
        )

    if session.refresh_jti != refresh_jti:
        repo.revoke_session(
            session.id
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token reuse detected",
        )

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

    if not new_payload:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token rotation failed",
        )

    new_jti = new_payload.get("jti")

    if not new_jti:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid rotated token payload",
        )

    repo.rotate_session_jti(
        session=session,
        new_jti=new_jti,
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
    db: Session,
    refresh_token: str,
) -> None:
    repo = AuthRepository(db)

    payload = verify_refresh_token(
        refresh_token
    )

    if not payload:
        raise INVALID_REFRESH_EXCEPTION

    session_id = payload.get("sid")

    if not session_id:
        return

    session = repo.get_session_by_session_id(
        session_id
    )

    if session:
        repo.revoke_session(
            session.id
        )

# =====================================
# GET ACTIVE SESSIONS
# =====================================

def get_user_sessions(
    db: Session,
    user_id: int,
):

    repo = AuthRepository(db)

    return repo.get_user_active_sessions(
        user_id=user_id,
    )


# =====================================
# REVOKE SESSION BY ID
# =====================================

def revoke_user_session(
    db: Session,
    user_id: int,
    session_id: str,
) -> None:

    repo = AuthRepository(db)

    session = repo.get_session_by_session_id(
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    if session.user_id != user_id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    repo.revoke_session(session)


# =====================================
# REVOKE ALL SESSIONS
# =====================================

def revoke_all_sessions(
    db: Session,
    user_id: int,
) -> None:

    repo = AuthRepository(db)

    repo.revoke_all_user_sessions(
        user_id=user_id,
    )