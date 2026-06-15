from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


# =========================================================
# BASE SCHEMA
# =========================================================

class BaseSchema(BaseModel):
    """
    Shared base schema configuration.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )


# =========================================================
# EMAIL MIXIN
# =========================================================

class EmailSchema(BaseSchema):
    """
    Shared email normalization schema.
    """

    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(
        cls,
        value: str,
    ) -> str:
        return value.lower().strip()


# =========================================================
# USER SIGNUP
# =========================================================

class UserSignup(EmailSchema):
    """
    User registration schema.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User account password",
    )


# =========================================================
# USER LOGIN
# =========================================================

class UserLogin(EmailSchema):
    """
    User login schema.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User account password",
    )