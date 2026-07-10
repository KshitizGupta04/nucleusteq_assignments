from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


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
        min_length=1,
        max_length=512
    )


class LoginRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=30
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=512
    )


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"