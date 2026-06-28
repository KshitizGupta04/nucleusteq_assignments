from fastapi import (
    Depends
)

from fastapi.security import (
    OAuth2PasswordBearer
)

from app.exceptions.customexceptions import (
    ForbiddenException,
    InvalidTokenException
)

from app.core.security import (
    decode_access_token
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):

    payload = decode_access_token(
        token
    )

    if not payload:

        raise InvalidTokenException()

    return payload


def get_current_admin(
    current_user=Depends(
        get_current_user
    )
):

    if current_user["role"] != "admin":

        raise ForbiddenException()

    return current_user