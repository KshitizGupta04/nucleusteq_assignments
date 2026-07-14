from typing import (
    List,
    Optional
)

from pydantic import (
    BaseModel,
    Field
)


AnswerType = str | List[str]


class QuestionBreakdownResponse(
    BaseModel
):

    question_id: str

    question: str

    selected_answer: Optional[
        AnswerType
    ] = None

    correct_answer: AnswerType

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


class QuizStatisticsResponse(
    BaseModel
):

    quiz_id: str

    total_attempts: int

    average_score: float

    pass_count: int

    fail_count: int

    pass_rate: float


class LeaderboardResponse(
    BaseModel
):

    rank: int

    student_id: str

    score_obtained: float

    total_marks: float

    percentage: float


class ResultMessageResponse(
    BaseModel
):

    message: str