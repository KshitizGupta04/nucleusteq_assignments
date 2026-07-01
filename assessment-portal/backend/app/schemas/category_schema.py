from pydantic import (
    BaseModel,
    Field
)


class CategoryRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=255
    )


class CategoryResponse(BaseModel):

    id: str

    name: str

    description: str


class UpdateCategoryRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=255
    )