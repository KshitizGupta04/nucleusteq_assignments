from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_admin,
    get_current_user
)

from app.schemas.question_schema import (
    QuestionRequest,
    UpdateQuestionRequest
)

from app.services.question_service import (
    QuestionService
)


router = APIRouter(
    prefix="/api/v1/questions",
    tags=["Question"]
)


@router.post("/")
def create_question(
    request: QuestionRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    return QuestionService.create_question(
        request
    )


@router.get("/quiz/{quiz_id}")
def get_questions_by_quiz(
    quiz_id: str,
    current_user=Depends(
        get_current_user
    )
):

    return QuestionService.get_questions_by_quiz(
        quiz_id
    )


@router.put("/{question_id}")
def update_question(
    question_id: str,
    request: UpdateQuestionRequest,
    current_admin=Depends(
        get_current_admin
    )
):

    return QuestionService.update_question(
        question_id,
        request
    )


@router.delete("/{question_id}")
def delete_question(
    question_id: str,
    current_admin=Depends(
        get_current_admin
    )
):

    return QuestionService.delete_question(
        question_id
    )