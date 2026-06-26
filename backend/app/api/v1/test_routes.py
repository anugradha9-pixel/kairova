from fastapi import APIRouter, Depends
from app.auth.permissions import (
    require_authenticated,
    require_creator,
    require_admin,
)
from app.auth.models import User

router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


# =========================================================
# AUTH TEST
# =========================================================

@router.get("/auth")
def test_auth(user: User = Depends(require_authenticated)):
    return {
        "message": "authenticated access granted",
        "user_id": getattr(user, "id", None),
    }


# =========================================================
# CREATOR TEST
# =========================================================

@router.post("/creator")
def test_creator(user: User = Depends(require_creator)):
    return {
        "message": "creator access granted",
        "user_id": getattr(user, "id", None),
        "role": getattr(user, "role", None),
    }


# =========================================================
# ADMIN TEST
# =========================================================

@router.get("/admin")
def test_admin(user: User = Depends(require_admin)):
    return {
        "message": "admin access granted",
        "user_id": getattr(user, "id", None),
        "is_admin": getattr(user, "is_admin", False),
    }