from fastapi import HTTPException, status

from app.auth.models import User

from app.modules.user.repository import UserRepository


# =====================================
# GET USER
# =====================================

def get_user_by_id_service(
    repo: UserRepository,
    user_id: int,
):

    user = repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# =====================================
# LIST USERS
# =====================================

def get_all_users_service(
    repo: UserRepository,
):

    return repo.get_all()


# =====================================
# UPDATE USER
# =====================================

def update_user_service(
    repo: UserRepository,
    user_id: int,
    email: str | None = None,
    is_active: bool | None = None,
):

    user = get_user_by_id_service(
        repo,
        user_id,
    )

    if email is not None:
        user.email = email

    if is_active is not None:
        user.is_active = is_active

    return repo.save(user)


# =====================================
# DELETE USER
# =====================================

def delete_user_service(
    repo: UserRepository,
    user_id: int,
):

    user = get_user_by_id_service(
        repo,
        user_id,
    )

    repo.delete(user)

    return {
        "message": "User deleted",
    }