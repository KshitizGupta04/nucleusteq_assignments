from typing import (
    List,
    Optional
)

from pydantic import (
    BaseModel,
    Field
)


class QuestionBreakdownResponse(
    BaseModel
):

    question_id: str

    question: str

    selected_answer: Optional[str] = None

    correct_answer: str

    is_correct: bool

    marks_obtained: float


class ResultResponse(
    BaseModel
):

    result_id: str

    attempt_id: str

    quiz_id: str

    student_id: str

    attempt_number: int

    score_obtained: float

    total_marks: float

    percentage: float

    status: str

    question_breakdown: List[
        QuestionBreakdownResponse
    ] = Field(
        default_factory=list
    )


class ResultHistoryResponse(
    BaseModel
):

    result_id: str

    attempt_id: str

    quiz_id: str

    attempt_number: int

    score_obtained: float

    total_marks: float

    percentage: float

    status: str


class AdminResultResponse(
    BaseModel
):

    result_id: str

    attempt_id: str

    quiz_id: str

    student_id: str

    attempt_number: int

    score_obtained: float

    total_marks: float

    percentage: float

    status: str


class ResultMessageResponse(
    BaseModel
):

    message: str