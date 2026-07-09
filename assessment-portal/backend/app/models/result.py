from datetime import (
    datetime
)

from pydantic import (
    BaseModel,
    Field
)


class Result(
    BaseModel
):

    attempt_id: str

    quiz_id: str

    student_id: str

    attempt_number: int

    score_obtained: float

    total_marks: float

    percentage: float

    status: str

    question_breakdown: list = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )