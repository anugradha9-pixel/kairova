from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.auth.dependencies import get_current_user
from app.auth.models import User


# =====================================
# INTERNAL USER VALIDATION
# =====================================

def _validate_user(
    current_user: User | None,
) -> User:
    """
    Shared authentication validation.
    """

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive",
        )

    return current_user


# =====================================
# AUTHENTICATED USER
# =====================================

def require_authenticated(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Any authenticated active user.
    """

    return _validate_user(
        current_user,
    )


# =====================================
# CREATOR ROLE
# =====================================

def require_creator(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Creator role required.
    Admins bypass creator restriction.
    """

    current_user = _validate_user(
        current_user,
    )

    # Admin override
    if current_user.is_admin:
        return current_user

    if current_user.role != "creator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Creator access required",
        )

    return current_user


# =====================================
# ADMIN ROLE
# =====================================

def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Admin role required.
    """

    current_user = _validate_user(
        current_user,
    )

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user