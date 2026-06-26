from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.dependencies import get_current_user
from app.auth.permissions import require_admin

from app.auth.models import User

from app.auth.schemas import (
    UserSignup,
    UserLogin,
    TokenPair,
    RefreshRequest,
    LogoutRequest,
    UserResponse,
    MessageResponse,
    SessionListResponse,
)

from app.auth.service import (
    create_user,
    login_user,
    refresh_user_tokens,
    logout_user,
    get_user_sessions,
    revoke_user_session,
    revoke_all_sessions,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# =====================================
# SIGNUP
# =====================================

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    payload: UserSignup,
    db: Session = Depends(get_db),
):
    return create_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# =====================================
# LOGIN
# =====================================

@router.post(
    "/login",
    response_model=TokenPair,
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# =====================================
# REFRESH
# =====================================

@router.post(
    "/refresh",
    response_model=TokenPair,
)
def refresh(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    return refresh_user_tokens(
        db=db,
        refresh_token=payload.refresh_token,
    )


# =====================================
# LOGOUT
# =====================================

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    payload: LogoutRequest,
    db: Session = Depends(get_db),
):
    logout_user(
        db=db,
        refresh_token=payload.refresh_token,
    )

    return MessageResponse(
        message="Logged out successfully",
    )


# =====================================
# CURRENT USER
# =====================================

@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user


# =====================================
# ACTIVE SESSIONS
# =====================================

@router.get(
    "/sessions",
    response_model=SessionListResponse,
)
def active_sessions(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    sessions = get_user_sessions(
        db=db,
        user_id=current_user.id,
    )

    return SessionListResponse(
        sessions=sessions,
    )


# =====================================
# REVOKE ONE SESSION
# =====================================

@router.delete(
    "/sessions/{session_id}",
    response_model=MessageResponse,
)
def revoke_session_route(
    session_id: str,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    revoke_user_session(
        db=db,
        user_id=current_user.id,
        session_id=session_id,
    )

    return MessageResponse(
        message="Session revoked",
    )


# =====================================
# REVOKE ALL SESSIONS
# =====================================

@router.delete(
    "/sessions",
    response_model=MessageResponse,
)
def revoke_all_sessions_route(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    revoke_all_sessions(
        db=db,
        user_id=current_user.id,
    )

    return MessageResponse(
        message="All sessions revoked",
    )


# =====================================
# ADMIN TEST
# =====================================

@router.get(
    "/admin-test",
)
def admin_test(
    current_user: User = Depends(
        require_admin
    ),
):
    return {
        "message": "Admin access granted",
    }