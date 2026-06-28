from app.constants.messages import (
    ErrorMessages
)


class UserAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.EMAIL_ALREADY_EXISTS
    ):

        super().__init__(message)


class UsernameAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.USERNAME_ALREADY_EXISTS
    ):

        super().__init__(message)


class UserNotFoundException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.USER_NOT_FOUND
    ):

        super().__init__(message)


class InvalidPasswordException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.INVALID_PASSWORD
    ):

        super().__init__(message)


class AdminAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.ADMIN_ALREADY_EXISTS
    ):

        super().__init__(message)


class InvalidTokenException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.INVALID_TOKEN
    ):

        super().__init__(message)


class UnauthorizedException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.INVALID_TOKEN
    ):

        super().__init__(message)


class ForbiddenException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.ADMIN_ACCESS_REQUIRED
    ):

        super().__init__(message)