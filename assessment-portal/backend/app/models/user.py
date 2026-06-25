from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"


class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

    email: EmailStr

    password: str

    role: UserRole = UserRole.STUDENT

    created_at: datetime = Field(default_factory=datetime.utcnow)