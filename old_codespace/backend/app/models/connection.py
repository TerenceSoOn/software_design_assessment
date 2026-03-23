"""
Connection model - for datemate connections.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class DatemateConnection(Base):
    """
    Datemate connection model.
    
    Represents a connection request between two users.
    After a good random chat, one user can send a datemate request.
    
    Attributes:
        id: Primary key
        requester_id: User who sent the request
        receiver_id: User who received the request
        status: Request status (pending/accepted/rejected)
        requested_at: When request was sent
        responded_at: When request was responded to
    """
    __tablename__ = "datemate_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")  # pending, accepted, rejected
    requested_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    
    # Relationships
    requester = relationship("User", foreign_keys=[requester_id], backref="sent_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_requests")
    
    def __repr__(self):
        return f"<DatemateConnection {self.requester_id} -> {self.receiver_id} ({self.status})>"
