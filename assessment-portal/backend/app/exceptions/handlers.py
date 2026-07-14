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
    AttemptAlreadyInProgressException,
    AttemptAlreadySubmittedException,
    AttemptNotFoundException,
    CategoryAlreadyExistsException,
    CategoryNotFoundException,
    ForbiddenException,
    InvalidAnswerException,
    InvalidPasswordException,
    InvalidTokenException,
    MaxAttemptReachedException,
    QuestionNotFoundException,
    QuizAlreadyExistsException,
    QuizExpiredException,
    QuizNotFoundException,
    QuizNotStartedException,
    ResultAlreadyExistsException,
    ResultNotFoundException,
    StudentAccessRequiredException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UsernameAlreadyExistsException
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


    @app.exception_handler(
        CategoryAlreadyExistsException
    )
    async def category_exists_exception_handler(
        request: Request,
        exc: CategoryAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        CategoryNotFoundException
    )
    async def category_not_found_exception_handler(
        request: Request,
        exc: CategoryNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        QuizAlreadyExistsException
    )
    async def quiz_exists_exception_handler(
        request: Request,
        exc: QuizAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        QuizNotFoundException
    )
    async def quiz_not_found_exception_handler(
        request: Request,
        exc: QuizNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )


    # EXT-008:
    # Quiz exists, but its availability window
    # has not started yet.
    @app.exception_handler(
        QuizNotStartedException
    )
    async def quiz_not_started_exception_handler(
        request: Request,
        exc: QuizNotStartedException
    ):

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc)
            }
        )


    # EXT-008:
    # Quiz exists, but its availability window
    # has already ended.
    @app.exception_handler(
        QuizExpiredException
    )
    async def quiz_expired_exception_handler(
        request: Request,
        exc: QuizExpiredException
    ):

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        QuestionNotFoundException
    )
    async def question_not_found_exception_handler(
        request: Request,
        exc: QuestionNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        AttemptNotFoundException
    )
    async def attempt_not_found_exception_handler(
        request: Request,
        exc: AttemptNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        MaxAttemptReachedException
    )
    async def max_attempt_reached_exception_handler(
        request: Request,
        exc: MaxAttemptReachedException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        StudentAccessRequiredException
    )
    async def student_access_required_exception_handler(
        request: Request,
        exc: StudentAccessRequiredException
    ):

        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        AttemptAlreadySubmittedException
    )
    async def attempt_already_submitted_exception_handler(
        request: Request,
        exc: AttemptAlreadySubmittedException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        InvalidAnswerException
    )
    async def invalid_answer_exception_handler(
        request: Request,
        exc: InvalidAnswerException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        AttemptAlreadyInProgressException
    )
    async def attempt_already_in_progress_exception_handler(
        request: Request,
        exc: AttemptAlreadyInProgressException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        ResultNotFoundException
    )
    async def result_not_found_exception_handler(
        request: Request,
        exc: ResultNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc)
            }
        )


    @app.exception_handler(
        ResultAlreadyExistsException
    )
    async def result_already_exists_exception_handler(
        request: Request,
        exc: ResultAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": str(exc)
            }
        )