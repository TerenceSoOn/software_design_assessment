"""
Chat models - for random chat matching and messages.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class RandomChat(Base):
    """
    Random chat session model.
    
    Represents a matched chat between two users.
    
    Attributes:
        id: Primary key
        user1_id: First user in chat
        user2_id: Second user in chat (or AI)
        status: Chat status (waiting/matched/ended)
        started_at: When chat started
        ended_at: When chat ended
    """
    __tablename__ = "random_chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Can be AI (null)
    status = Column(String, default="waiting")  # waiting, matched, ended
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    
    def __repr__(self):
        return f"<RandomChat {self.id} status={self.status}>"


class ChatMessage(Base):
    """
    Messages sent in random chats.
    
    Attributes:
        id: Primary key
        chat_id: Foreign key to RandomChat
        sender_id: User who sent message
        message_text: Message content
        sent_at: When message was sent
    """
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("random_chats.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    chat = relationship("RandomChat", backref="messages")
    sender = relationship("User")
    
    def __repr__(self):
        return f"<ChatMessage {self.id} in chat {self.chat_id}>"
