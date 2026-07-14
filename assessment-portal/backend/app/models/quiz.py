from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class Quiz(BaseModel):

    title: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=255
    )

    category_id: str

    duration: int = Field(
        ...,
        gt=0
    )

    total_marks: int = Field(
        ...,
        gt=0
    )

    question_count: int | None = Field(
        default=None,
        gt=0
    )

    negative_marks: float = Field(
        default=0.0,
        ge=0
    )

    available_from: datetime | None = None

    available_until: datetime | None = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )