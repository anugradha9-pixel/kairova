from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.models import User
from app.auth.permissions import (
    require_authenticated,
    require_admin,
)

from app.schemas.response import APIResponse

from app.modules.user.repository import UserRepository

from app.modules.user.schemas import (
    UserProfileResponse,
    UserUpdateRequest,
)

from app.modules.user.service import (
    get_user_by_id_service,
    get_all_users_service,
    update_user_service,
    delete_user_service,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# =====================================
# CURRENT USER
# =====================================

@router.get(
    "/me",
    response_model=UserProfileResponse,
)
def current_user_profile(
    current_user: User = Depends(
        require_authenticated
    ),
):
    return current_user


# =====================================
# LIST USERS (ADMIN)
# =====================================

@router.get("")
def list_users(
    admin: User = Depends(
        require_admin
    ),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    users = get_all_users_service(
        repo
    )

    return APIResponse(
        message="Users retrieved",
        data=users,
    )


# =====================================
# GET USER (ADMIN)
# =====================================

@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
)
def get_user(
    user_id: int,
    admin: User = Depends(
        require_admin
    ),
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)

    return get_user_by_id_service(
        repo,
        user_id,
    )


# =====================================
# UPDATE USER
# =====================================

@router.patch(
    "/{user_id}",
    response_model=UserProfileResponse,
)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    current_user: User = Depends(
        require_authenticated
    ),
    db: Session = Depends(get_db),
):

    if (
        current_user.id != user_id
        and
        not current_user.is_admin
    ):
        raise HTTPException(
            status_code=403,
            detail="Not allowed",
        )

    repo = UserRepository(db)

    return update_user_service(
        repo=repo,
        user_id=user_id,
        email=payload.email,
        is_active=payload.is_active,
    )


# =====================================
# DELETE USER
# =====================================

@router.delete(
    "/{user_id}",
)
def delete_user(
    user_id: int,
    admin: User = Depends(
        require_admin
    ),
    db: Session = Depends(get_db),
):

    repo = UserRepository(db)

    result = delete_user_service(
        repo,
        user_id,
    )

    return APIResponse(
        message=result["message"],
        data={},
    )