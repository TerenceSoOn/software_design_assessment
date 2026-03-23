"""
Profile schemas for API requests and responses.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProfileBase(BaseModel):
    """Base profile schema."""
    display_name: Optional[str] = None
    bio: Optional[str] = None
    interests: List[str] = []
    age: Optional[int] = None
    gender: Optional[str] = None
    preferred_gender: Optional[str] = None  # "male", "female", "any"
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    photo_wall: List[str] = []


class ProfileCreate(ProfileBase):
    """Schema for creating a profile."""
    pass


class ProfileUpdate(ProfileBase):
    """Schema for updating a profile (all fields optional)."""
    pass


class ProfileResponse(ProfileBase):
    """Schema for profile in API responses."""
    id: int
    user_id: int
    updated_at: datetime
    
    class Config:
        from_attributes = True
