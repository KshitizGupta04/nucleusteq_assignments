from datetime import (
    datetime
)

from pydantic import (
    BaseModel,
    Field
)


class Attempt(
    BaseModel
):

    quiz_id: str

    student_id: str

    attempt_number: int

    question_snapshot: list = Field(
        default_factory=list
    )

    answers: dict = Field(
        default_factory=dict
    )

    score: int = 0

    status: str = "in_progress"

    started_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    submitted_at: datetime | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )