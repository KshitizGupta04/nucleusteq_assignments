from typing import Optional

from pydantic import (
    BaseModel,
    Field
)


class CategoryRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=200
    )


class UpdateCategoryRequest(BaseModel):

    name: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    description: str = Field(
        ...,
        min_length=5,
        max_length=200
    )


class CategoryCreateResponse(BaseModel):

    message: str
    category_id: str


class CategoryMessageResponse(BaseModel):

    message: str