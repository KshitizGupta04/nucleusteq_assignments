"""
Pydantic schemas for user authentication.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for user registration.
    """

    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = "student"


class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user details.
    """

    id: str
    name: str
    email: EmailStr
    role: str
    created_at: datetime


class Token(BaseModel):
    """
    Schema for JWT token response.
    """

    access_token: str
    token_type: str = "bearer"