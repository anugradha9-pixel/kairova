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
# AUTH REQUEST SCHEMAS
# =====================================

class UserSignup(BaseSchema):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User account password",
    )

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str
    ) -> str:

        return value.lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str
    ) -> str:

        if " " in value:
            raise ValueError(
                "Password cannot contain spaces"
            )

        return value


class UserLogin(BaseSchema):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User account password",
    )

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str
    ) -> str:

        return value.lower().strip()


# =====================================
# TOKEN SCHEMAS
# =====================================

class TokenPair(BaseSchema):

    access_token: str
    refresh_token: str

    token_type: Literal["bearer"] = "bearer"


class TokenResponse(BaseSchema):

    access_token: str

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

    is_active: bool
    is_admin: bool

    created_at: datetime
    updated_at: datetime


# =====================================
# GENERIC RESPONSE SCHEMAS
# =====================================

class MessageResponse(BaseSchema):

    message: str


# =====================================
# INTERNAL USER SCHEMA
# =====================================

class UserOut(BaseSchema):

    id: int

    email: EmailStr

    is_active: bool
    is_admin: bool


# =====================================
# SESSION RESPONSE
# =====================================

class SessionResponse(BaseSchema):

    session_id: str

    refresh_jti: str

    is_active: bool

    expires_at: datetime


# =====================================
# SESSION LIST RESPONSE
# =====================================

class SessionListResponse(BaseSchema):

    sessions: list[SessionResponse]