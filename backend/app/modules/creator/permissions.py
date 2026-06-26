from fastapi import HTTPException

def require_creator_owner_or_admin(
    creator,
    current_user,
):
    if current_user.is_admin:
        return

    if creator.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )