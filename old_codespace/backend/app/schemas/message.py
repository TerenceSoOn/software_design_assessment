"""
Message schemas for private messaging.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    """Schema for creating a priva message."""
    receiver_id: int
    message_text: str


class MessageResponse(BaseModel):
    """Schema for message in API responses."""
    id: int
    connection_id: int
    sender_id: int
    receiver_id: int
    message_text: str
    sent_at: datetime
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
