from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)

import re


class RegisterRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z][A-Za-z0-9_]*$"
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=32
    )

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str
    ):

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*()_\-+=]", value):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value


class LoginRequest(BaseModel):

    username: str

    password: str


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"