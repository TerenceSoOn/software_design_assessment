"""
Profile model - stores user profile information.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Profile(Base):
    """
    User profile model.
    
    Each user has one profile with personal information.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to User
        display_name: Name shown to other users
        bio: About me / bio text
        interests: JSON list of interests
        age: User's age
        gender: User's gender
        location: User's location
        avatar_url: URL to avatar image
        photo_wall: JSON array of photo URLs
        updated_at: Last update timestamp
    """
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    display_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    interests = Column(JSON, default=list)  # List of interests
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    preferred_gender = Column(String, nullable=True)  # "male", "female", "any"
    location = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    photo_wall = Column(JSON, default=list)  # List of photo URLs
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to user
    user = relationship("User", backref="profile")
    
    def __repr__(self):
        return f"<Profile for user_id={self.user_id}>"
