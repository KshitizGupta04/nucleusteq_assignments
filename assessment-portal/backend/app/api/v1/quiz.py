from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user
)

from app.schemas.quiz_schema import (
    QuizRequest,
    UpdateQuizRequest
)

from app.services.quiz_service import (
    QuizService
)


router = APIRouter(
    prefix="/api/v1/quizzes",
    tags=["Quiz"]
)


@router.post("/")
def create_quiz(
    request: QuizRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    response = QuizService.create_quiz(
        request
    )

    return response


@router.get("/")
def get_all_quizzes(
    current_user=Depends(
        get_current_user
    )
):

    response = QuizService.get_all_quizzes(
        current_user
    )

    return response


@router.put("/{quiz_id}")
def update_quiz(
    quiz_id: str,
    request: UpdateQuizRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    response = QuizService.update_quiz(
        quiz_id,
        request
    )

    return response


@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: str,
    current_admin=Depends(
        get_current_admin
    )
):

    response = QuizService.delete_quiz(
        quiz_id
    )

    return response