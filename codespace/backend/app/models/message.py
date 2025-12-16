"""
Message model - for private messaging between datemates.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PrivateMessage(Base):
    """
    Private message model.
    
    Messages sent between connected datemates.
    
    Attributes:
        id: Primary key
        connection_id: Datemate connection this message belongs to
        sender_id: User who sent the message
        receiver_id: User who receives the message
        message_text: Message content
        image_url: Optional image URL
        sent_at: When message was sent
        read_at: When message was read (null if unread)
    """
    __tablename__ = "private_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("datemate_connections.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(Text, nullable=True)  # 允许为空（纯图片消息）
    image_url = Column(String(500), nullable=True)  # 图片 URL
    sent_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    connection = relationship("DatemateConnection", backref="messages")
    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    
    def __repr__(self):
        return f"<PrivateMessage {self.id} from {self.sender_id} to {self.receiver_id}>"
