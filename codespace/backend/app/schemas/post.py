"""
Post schemas for Public Square feature.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PostCreate(BaseModel):
    """Schema for creating a post."""
    content_text: str
    image_urls: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    
    class Config:
        # Allow 'content' as alias for 'content_text'
        populate_by_name = True
        
    @classmethod
    def model_validate(cls, obj):
        # Handle 'content' field if provided instead of 'content_text'
        if isinstance(obj, dict):
            if 'content' in obj and 'content_text' not in obj:
                obj['content_text'] = obj.pop('content')
            # Handle singular 'image_url' if provided
            if 'image_url' in obj and 'image_urls' not in obj:
                url = obj.pop('image_url')
                obj['image_urls'] = [url] if url else []
        return super().model_validate(obj)


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    content_text: Optional[str] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None


class PostResponse(BaseModel):
    """Schema for post in API responses."""
    id: int
    user_id: int
    content_text: str
    image_urls: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    like_count: int = 0
    comment_count: int = 0
    author_name: Optional[str] = None
    author_avatar_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    """Schema for creating a comment."""
    comment_text: str
    
    @classmethod
    def model_validate(cls, obj):
        # Handle 'content' field if provided instead of 'comment_text'
        if isinstance(obj, dict) and 'content' in obj and 'comment_text' not in obj:
            obj['comment_text'] = obj.pop('content')
        return super().model_validate(obj)


class CommentResponse(BaseModel):
    """Schema for comment in API responses."""
    id: int
    post_id: int
    user_id: int
    comment_text: str
    created_at: datetime
    
    class Config:
        from_attributes = True
