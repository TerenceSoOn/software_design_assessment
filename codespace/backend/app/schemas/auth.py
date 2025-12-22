"""
Authentication schemas for login/register requests and responses.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration request."""
    username: str
    email: Optional[str] = None  # Email is now optional
    password: str
    gender: str  # "male", "female", "other"
    preferred_gender: str  # "male", "female", "any"


class UserLogin(BaseModel):
    """Schema for user login request."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    user_id: int
