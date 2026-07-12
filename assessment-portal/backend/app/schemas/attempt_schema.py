from datetime import (
    datetime
)

from typing import (
    Dict,
    List
)

from pydantic import (
    BaseModel,
    Field
)


class StartAttemptRequest(
    BaseModel
):

    quiz_id: str


class SaveAnswerRequest(
    BaseModel
):

    question_id: str

    answer: str = Field(
        ...,
        min_length=1
    )


class SubmitAttemptRequest(
    BaseModel
):

    answers: Dict[
        str,
        str
    ]


class AttemptQuestionResponse(
    BaseModel
):

    id: str

    quiz_id: str

    question: str

    options: List[str]

    question_type: str

    difficulty: str


class AttemptResponse(
    BaseModel
):

    attempt_id: str

    quiz_id: str

    student_id: str

    attempt_number: int

    question_snapshot: List[
        AttemptQuestionResponse
    ]

    answers: Dict[
        str,
        str
    ]

    score: float

    status: str

    started_at: datetime

    expires_at: datetime


class AttemptCreateResponse(
    BaseModel
):

    message: str

    attempt_id: str

    resumed: bool

    started_at: datetime

    expires_at: datetime


class AttemptMessageResponse(
    BaseModel
):

    message: str


class ResumeAttemptResponse(
    BaseModel
):

    attempt_id: str

    quiz_id: str

    question_snapshot: List[
        AttemptQuestionResponse
    ]

    answers: Dict[
        str,
        str
    ]

    status: str

    started_at: datetime

    expires_at: datetime