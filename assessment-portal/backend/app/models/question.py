from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class Question(BaseModel):

    quiz_id: str

    question: str

    options: list[str]

    correct_answer: str

    question_type: str

    difficulty: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime | None = None