import logging

from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import (
    JWTError,
    jwt
)

from passlib.context import (
    CryptContext
)

from app.core.config import (
    settings
)


logger = logging.getLogger(__name__)


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
) -> str:

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    data: dict
) -> str:

    payload = data.copy()

    expire = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update(
        {
            "exp": expire,
            "type": "access"
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(
    data: dict
) -> str:

    payload = data.copy()

    expire = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    payload.update(
        {
            "exp": expire,
            "type": "refresh"
        }
    )

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(
    token: str
):

    payload = None

    try:

        decoded_payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        if decoded_payload.get(
            "type"
        ) == "access":

            payload = decoded_payload

    except JWTError as exception:

        logger.exception(
            "Failed to decode access token: %s",
            exception
        )

    return payload


def decode_refresh_token(
    token: str
):

    payload = None

    try:

        decoded_payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        if decoded_payload.get(
            "type"
        ) == "refresh":

            payload = decoded_payload

    except JWTError as exception:

        logger.exception(
            "Failed to decode refresh token: %s",
            exception
        )

    return payload