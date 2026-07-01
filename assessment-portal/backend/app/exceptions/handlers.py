from fastapi import (
    FastAPI,
    Request,
    status
)

from fastapi.responses import (
    JSONResponse
)

from app.exceptions.customexceptions import (
    AdminAlreadyExistsException,
    ForbiddenException,
    InvalidPasswordException,
    InvalidTokenException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
)


def register_exception_handlers(
    app: FastAPI
):

    @app.exception_handler(
        UserAlreadyExistsException
    )
    async def user_exists_exception_handler(
        request: Request,
        exc: UserAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        UsernameAlreadyExistsException
    )
    async def username_exists_exception_handler(
        request: Request,
        exc: UsernameAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        UserNotFoundException
    )
    async def user_not_found_exception_handler(
        request: Request,
        exc: UserNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        InvalidPasswordException
    )
    async def invalid_password_exception_handler(
        request: Request,
        exc: InvalidPasswordException
    ):

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        AdminAlreadyExistsException
    )
    async def admin_exists_exception_handler(
        request: Request,
        exc: AdminAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        InvalidTokenException
    )
    async def invalid_token_exception_handler(
        request: Request,
        exc: InvalidTokenException
    ):

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        UnauthorizedException
    )
    async def unauthorized_exception_handler(
        request: Request,
        exc: UnauthorizedException
    ):

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc)
            }
        )

    @app.exception_handler(
        ForbiddenException
    )
    async def forbidden_exception_handler(
        request: Request,
        exc: ForbiddenException
    ):

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc)
            }
        )