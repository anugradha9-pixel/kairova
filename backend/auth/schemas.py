from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


# =====================================
# BASE SCHEMA
# =====================================

class BaseSchema(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )


# =====================================
# SHARED FIELDS
# =====================================

PasswordField = Field(
    min_length=8,
    max_length=128,
    description="User account password",
)


# =====================================
# AUTH REQUEST SCHEMAS
# =====================================

class UserSignup(BaseSchema):

    email: EmailStr

    password: str = PasswordField

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str,
    ) -> str:
        return value.lower().strip()


class UserLogin(BaseSchema):

    email: EmailStr

    password: str = PasswordField

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str,
    ) -> str:
        return value.lower().strip()


# =====================================
# TOKEN SCHEMAS
# =====================================

class TokenPair(BaseSchema):

    access_token: str

    refresh_token: str

    token_type: Literal["bearer"] = "bearer"


class RefreshRequest(BaseSchema):

    refresh_token: str


class LogoutRequest(BaseSchema):

    refresh_token: str


# =====================================
# USER RESPONSE SCHEMAS
# =====================================

class UserResponse(BaseSchema):

    id: int

    email: EmailStr

    created_at: datetime

    updated_at: datetime | None = None

    last_login_at: datetime | None = None


# =====================================
# GENERIC RESPONSE SCHEMAS
# =====================================

class MessageResponse(BaseSchema):

    message: str