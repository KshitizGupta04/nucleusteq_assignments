from datetime import (
    datetime,
    timezone
)

from pydantic import (
    BaseModel,
    Field
)


def get_utc_now():

    return datetime.now(
        timezone.utc
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

    score: float = 0.0

    status: str = "in_progress"

    started_at: datetime = Field(
        default_factory=get_utc_now
    )

    submitted_at: datetime | None = None

    created_at: datetime = Field(
        default_factory=get_utc_now
    )

    updated_at: datetime = Field(
        default_factory=get_utc_now
    )