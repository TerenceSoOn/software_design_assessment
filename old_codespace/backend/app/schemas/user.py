"""
User schemas for API requests and responses.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user (includes password)."""
    password: str


class UserResponse(UserBase):
    """Schema for user in API responses (no password)."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allow ORM model conversion
