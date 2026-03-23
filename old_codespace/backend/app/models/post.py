"""
Post models - for the Public Square feature.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Post(Base):
    """
    Post model for Public Square.
    
    Users can create posts with text and images.
    
    Attributes:
        id: Primary key
        user_id: User who created the post
        content_text: Post text content
        image_urls: JSON array of image URLs
        tags: JSON array of tags
        created_at: When post was created
        updated_at: Last update timestamp
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_text = Column(Text, nullable=False)
    image_urls = Column(JSON, default=list)  # List of image URLs
    tags = Column(JSON, default=list)  # List of tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", backref="posts")
    
    def __repr__(self):
        return f"<Post {self.id} by user {self.user_id}>"


class PostLike(Base):
    """
    Post like model.
    
    Represents a like on a post.
    
    Attributes:
        id: Primary key
        post_id: Post that was liked
        user_id: User who liked the post
        created_at: When like was created
    """
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", backref="likes")
    user = relationship("User")
    
    def __repr__(self):
        return f"<PostLike post={self.post_id} by user={self.user_id}>"


class PostComment(Base):
    """
    Post comment model.
    
    Represents a comment on a post.
    
    Attributes:
        id: Primary key
        post_id: Post being commented on
        user_id: User who made the comment
        comment_text: Comment content
        created_at: When comment was created
    """
    __tablename__ = "post_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    post = relationship("Post", backref="comments")
    author = relationship("User")
    
    def __repr__(self):
        return f"<PostComment {self.id} on post {self.post_id}>"
