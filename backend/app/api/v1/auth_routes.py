from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.schemas import (
    UserSignup,
    UserLogin,
    TokenPair,
    RefreshRequest,
    LogoutRequest,
    UserResponse,
)

from app.auth.service import (
    create_user,
    login_user,
    refresh_user_tokens,
    logout_user,
)

from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


# =====================================
# SIGNUP
# =====================================

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    user = create_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )
    return user


# =====================================
# LOGIN
# =====================================

@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    return login_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )


# =====================================
# REFRESH TOKEN
# =====================================

@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest):
    tokens = refresh_user_tokens(
        refresh_token=payload.refresh_token
    )
    return tokens


# =====================================
# LOGOUT
# =====================================

@router.post("/logout")
def logout(payload: LogoutRequest):
    logout_user(refresh_token=payload.refresh_token)
    return {"message": "Logged out successfully"}


# =====================================
# CURRENT USER
# =====================================

@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user