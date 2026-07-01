from datetime import datetime

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from app.enums.user_role import (
    UserRole
)


class User(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    email: EmailStr

    password: str

    role: UserRole = (
        UserRole.STUDENT
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )