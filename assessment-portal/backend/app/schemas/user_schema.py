from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str

    username: str

    email: EmailStr

    role: str

    created_at: datetime