from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    model_validator
)


QuestionType = Literal[
    "mcq",
    "true_false",
    "short_answer",
    "multiple_select"
]

DifficultyType = Literal[
    "easy",
    "medium",
    "hard"
]


class QuestionBase(BaseModel):

    question: str = Field(
        ...,
        min_length=5,
        max_length=500
    )

    options: list[str]

    correct_answer: str | list[str]

    question_type: QuestionType

    difficulty: DifficultyType


    @model_validator(
        mode="after"
    )
    def validate_question_data(
        self
    ):

        if (
            self.question_type == "mcq"
            and len(self.options) != 4
        ):

            raise ValueError(
                "MCQ question must contain "
                "exactly 4 options."
            )


        if (
            self.question_type == "true_false"
            and len(self.options) != 2
        ):

            raise ValueError(
                "True/False question must contain "
                "exactly 2 options."
            )


        if (
            self.question_type == "short_answer"
        ):

            if self.options:

                raise ValueError(
                    "Short answer question must "
                    "not contain options."
                )

            if not isinstance(
                self.correct_answer,
                str
            ):

                raise ValueError(
                    "Short answer question must "
                    "have a single correct answer."
                )

            if not self.correct_answer.strip():

                raise ValueError(
                    "Correct answer cannot be empty."
                )

            return self


        cleaned_options = [
            option.strip()
            for option in self.options
        ]


        if any(
            not option
            for option in cleaned_options
        ):

            raise ValueError(
                "Options cannot be empty."
            )


        if (
            len(set(cleaned_options))
            != len(cleaned_options)
        ):

            raise ValueError(
                "All options must be unique."
            )


        if (
            self.question_type ==
            "multiple_select"
        ):

            if len(self.options) < 2:

                raise ValueError(
                    "Multiple-select question must "
                    "contain at least 2 options."
                )

            if not isinstance(
                self.correct_answer,
                list
            ):

                raise ValueError(
                    "Multiple-select question must "
                    "have multiple correct answers."
                )

            if len(
                self.correct_answer
            ) < 2:

                raise ValueError(
                    "Multiple-select question must "
                    "have at least 2 correct answers."
                )

            if (
                len(
                    set(
                        self.correct_answer
                    )
                )
                !=
                len(
                    self.correct_answer
                )
            ):

                raise ValueError(
                    "Correct answers must be unique."
                )

            if any(
                answer not in self.options
                for answer in
                self.correct_answer
            ):

                raise ValueError(
                    "Every correct answer must be "
                    "one of the options."
                )

            return self


        if not isinstance(
            self.correct_answer,
            str
        ):

            raise ValueError(
                "Correct answer must be a string "
                "for this question type."
            )


        if (
            self.correct_answer
            not in self.options
        ):

            raise ValueError(
                "Correct answer must be "
                "one of the options."
            )


        return self


class QuestionRequest(
    QuestionBase
):

    quiz_id: str


class UpdateQuestionRequest(
    QuestionBase
):

    pass


class QuestionResponse(BaseModel):

    id: str

    quiz_id: str

    question: str

    options: list[str]

    correct_answer: str | list[str]

    question_type: QuestionType

    difficulty: DifficultyType


class StudentQuestionResponse(BaseModel):

    id: str

    quiz_id: str

    question: str

    options: list[str]

    question_type: QuestionType

    difficulty: DifficultyType