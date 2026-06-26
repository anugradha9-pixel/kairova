from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.auth.repository import AuthRepository
from app.auth.security import verify_password

from app.auth.schemas import (
    BaseSchema,
    TokenPair,
    UserLogin,
    UserSignup,
    UserResponse,
    MessageResponse,
    RefreshRequest,
    LogoutRequest,
    SessionResponse,
    SessionListResponse,
)

from app.auth.service import (
    create_user,
    login_user,
    logout_user,
    refresh_user_tokens,
    get_user_sessions,
    revoke_user_session,
    revoke_all_sessions,
)

from app.auth.permissions import (
    require_admin,
)

from app.db.session import get_db


# =====================================
# ROUTER
# =====================================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================
# RESPONSE SCHEMA (SIGNUP)
# =====================================

class SignupResponse(BaseSchema):
    message: str
    user_id: int


# =====================================
# SIGNUP
# =====================================

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    payload: UserSignup,
    db: Session = Depends(get_db),
):
    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )

    return SignupResponse(
        message="User created successfully",
        user_id=user.id,
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
# OAUTH2 LOGIN (SWAGGER AUTHORIZE)
# =====================================

@router.post(
    "/token",
)
def token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2-compatible login endpoint.

    Swagger's Authorize button submits:
        username
        password

    as application/x-www-form-urlencoded.

    We map username -> email and then
    reuse the existing login service.
    """

    try:
        return login_user(
            db=db,
            email=form_data.username,
            password=form_data.password,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


# =====================================
# REFRESH TOKEN
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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
# ADMIN ACCESS
# =====================================

@router.get(
    "/admin-test",
)
def admin_test(
    current_user: User = Depends(require_admin),
):
    return {
        "message": "Admin access granted",
    }