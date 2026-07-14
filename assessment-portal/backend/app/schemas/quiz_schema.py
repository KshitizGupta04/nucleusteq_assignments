from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    model_validator
)


class QuizBase(BaseModel):

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


    @model_validator(
        mode="after"
    )
    def validate_availability_window(
        self
    ):

        if (
            self.available_from is not None
            and self.available_until is not None
            and self.available_until
            <= self.available_from
        ):

            raise ValueError(
                "Quiz availability end time must "
                "be after the start time."
            )

        return self


class QuizRequest(
    QuizBase
):

    pass


class QuizResponse(BaseModel):

    id: str

    title: str

    description: str

    category_id: str

    duration: int

    total_marks: int

    question_count: int | None = None

    negative_marks: float = 0.0

    available_from: datetime | None = None

    available_until: datetime | None = None


class UpdateQuizRequest(
    QuizBase
):

    pass


class QuizCreateResponse(BaseModel):

    message: str

    quiz_id: str


class QuizMessageResponse(BaseModel):

    message: str