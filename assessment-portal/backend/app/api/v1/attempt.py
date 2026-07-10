from fastapi import (
    APIRouter,
    Depends
)

from app.core.dependencies import (
    get_current_student
)

from app.schemas.attempt_schema import (
    ResumeAttemptResponse,
    SaveAnswerRequest,
    StartAttemptRequest,
    SubmitAttemptRequest
)

from app.services.attempt_service import (
    AttemptService
)


router = APIRouter(
    prefix="/api/v1/attempts",
    tags=["Attempt"]
)


@router.post("/start")
def start_attempt(
    request: StartAttemptRequest,
    current_user=Depends(
        get_current_student
    )
):

    response = AttemptService.start_attempt(
        request,
        current_user
    )

    return response


@router.put("/{attempt_id}/answer")
def save_answer(
    attempt_id: str,
    request: SaveAnswerRequest,
    current_user=Depends(
        get_current_student
    )
):

    response = AttemptService.save_answer(
        attempt_id,
        request
    )

    return response


@router.get(
    "/{attempt_id}",
    response_model=ResumeAttemptResponse
)
def resume_attempt(
    attempt_id: str,
    current_user=Depends(
        get_current_student
    )
):

    response = AttemptService.resume_attempt(
        attempt_id
    )

    return response


@router.post("/{attempt_id}/submit")
def submit_attempt(
    attempt_id: str,
    request: SubmitAttemptRequest,
    current_user=Depends(
        get_current_student
    )
):

    response = AttemptService.submit_attempt(
        attempt_id,
        request
    )

    return response