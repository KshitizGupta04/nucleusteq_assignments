from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class QuestionRequest(BaseModel):

    quiz_id: str

    question: str = Field(
        ...,
        min_length=5,
        max_length=500
    )

    options: list[str]

    correct_answer: str

    question_type: Literal[
        "mcq",
        "true_false"
    ]

    difficulty: Literal[
        "easy",
        "medium",
        "hard"
    ]

    @field_validator("options")
    @classmethod
    def validate_options(
        cls,
        value: list[str]
    ):

        if len(value) != 4:
            raise ValueError(
                "Question must contain exactly 4 options."
            )

        return value

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(
        cls,
        value: str,
        info
    ):

        options = info.data.get(
            "options",
            []
        )

        if value not in options:
            raise ValueError(
                "Correct answer must be one of the options."
            )

        return value


class UpdateQuestionRequest(
    BaseModel
):

    question: str = Field(
        ...,
        min_length=5,
        max_length=500
    )

    options: list[str]

    correct_answer: str

    question_type: Literal[
        "mcq",
        "true_false"
    ]

    difficulty: Literal[
        "easy",
        "medium",
        "hard"
    ]

    @field_validator("options")
    @classmethod
    def validate_options(
        cls,
        value: list[str]
    ):

        if len(value) != 4:
            raise ValueError(
                "Question must contain exactly 4 options."
            )

        return value

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(
        cls,
        value: str,
        info
    ):

        options = info.data.get(
            "options",
            []
        )

        if value not in options:
            raise ValueError(
                "Correct answer must be one of the options."
            )

        return value