from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.auth.models import User

from app.auth.schemas import (
    BaseSchema,
    TokenPair,
    UserLogin,
    UserSignup,
    UserResponse,
    MessageResponse,
    RefreshRequest,
    LogoutRequest,
)

from app.auth.service import (
    create_user,
    login_user,
    logout_user,
    refresh_user_tokens,
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
# REFRESH TOKEN
# =====================================

@router.post(
    "/refresh",
    response_model=TokenPair,
)
def refresh(
    payload: RefreshRequest,
):

    return refresh_user_tokens(
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
):

    logout_user(
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