from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.orm import Session

from backend.auth.dependencies import (
    get_current_user,
)

from backend.auth.models import User

from backend.auth.schemas import (
    TokenPair,
    UserLogin,
    UserSignup,
    UserResponse,
    MessageResponse,
)

from backend.auth.service import (
    create_user,
    login_user,
    logout_user,
    refresh_user_tokens,
)

from backend.db.session import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =====================================
# SIGNUP
# =====================================

class SignupResponse(BaseSchema):
    message: str
    user_id: int

@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
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
# CURRENT AUTHENTICATED USER
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