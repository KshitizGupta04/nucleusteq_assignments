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


class CategoryAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.CATEGORY_ALREADY_EXISTS
    ):

        super().__init__(message)


class CategoryNotFoundException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.CATEGORY_NOT_FOUND
    ):

        super().__init__(message)


class QuizAlreadyExistsException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.QUIZ_ALREADY_EXISTS
    ):

        super().__init__(message)


class QuizNotFoundException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.QUIZ_NOT_FOUND
    ):

        super().__init__(message)

class QuestionNotFoundException(Exception):

    def __init__(
        self,
        message: str = ErrorMessages.QUESTION_NOT_FOUND
    ):

        super().__init__(message)

class AttemptNotFoundException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.ATTEMPT_NOT_FOUND
    ):

        super().__init__(
            message
        )


class MaxAttemptReachedException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.MAX_ATTEMPT_REACHED
    ):

        super().__init__(
            message
        )

class StudentAccessRequiredException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.STUDENT_ACCESS_REQUIRED
    ):

        super().__init__(
            message
        )

class AttemptAlreadySubmittedException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.ATTEMPT_ALREADY_SUBMITTED
    ):

        super().__init__(
            message
        )

class InvalidAnswerException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.INVALID_ANSWER
    ):

        super().__init__(
            message
        )

class AttemptAlreadyInProgressException(
    Exception
):

    def __init__(
        self,
        message: str = ErrorMessages.ATTEMPT_ALREADY_IN_PROGRESS
    ):

        super().__init__(
            message
        )