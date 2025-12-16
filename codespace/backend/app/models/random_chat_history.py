"""
Random Chat History model - Temporary storage for random chat messages.

Messages are stored here during random chat sessions and transferred to
PrivateMessage when users become datemates.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class RandomChatHistory(Base):
    """Random chat message history (temporary storage)."""
    __tablename__ = "random_chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, nullable=False)  # UUID to group conversation
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=True)  # 允许为空（纯图片消息）
    image_url = Column(String(500), nullable=True)  # 图片 URL
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
