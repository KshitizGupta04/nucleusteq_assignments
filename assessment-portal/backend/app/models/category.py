from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class Category(BaseModel):

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

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )