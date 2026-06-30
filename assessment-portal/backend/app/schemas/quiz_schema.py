from pydantic import (
    BaseModel,
    Field
)


class QuizRequest(BaseModel):

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


class QuizResponse(BaseModel):

    id: str

    title: str

    description: str

    category_id: str

    duration: int

    total_marks: int


class UpdateQuizRequest(BaseModel):

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