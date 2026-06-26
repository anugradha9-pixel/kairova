from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from app.auth.schemas import BaseSchema


# =====================================
# USER PROFILE RESPONSE
# =====================================

class UserProfileResponse(BaseSchema):
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


# =====================================
# USER LIST RESPONSE
# =====================================

class UserListResponse(BaseSchema):
    users: list[UserProfileResponse]


# =====================================
# UPDATE USER
# =====================================

class UserUpdateRequest(BaseSchema):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


# =====================================
# DELETE RESPONSE
# =====================================

class UserDeleteResponse(BaseSchema):
    message: str