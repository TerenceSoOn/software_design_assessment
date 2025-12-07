"""
Datemates router - datemate connection management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.connection import DatemateConnection
from app.utils.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/datemates", tags=["Datemates"])


class ConnectionRequest(BaseModel):
    """Schema for creating a connection request."""
    receiver_id: int


class ConnectionResponse(BaseModel):
    """Schema for connection in responses."""
    id: int
    requester_id: int
    receiver_id: int
    status: str
    requested_at: datetime
    responded_at: datetime | None
    
    class Config:
        from_attributes = True


@router.post("/", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
def send_connection_request(
    request_data: ConnectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a datemate connection request to another user."""
    # Can't request yourself
    if request_data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send request to yourself")
    
    # Check if connection already exists (any status)
    existing = db.query(DatemateConnection).filter(
        ((DatemateConnection.requester_id == current_user.id) & (DatemateConnection.receiver_id == request_data.receiver_id)) |
        ((DatemateConnection.requester_id == request_data.receiver_id) & (DatemateConnection.receiver_id == current_user.id))
    ).first()
    
    if existing:
        if existing.status in ["pending", "accepted"]:
            raise HTTPException(status_code=400, detail="Connection request already exists")
        elif existing.status == "rejected":
            # If previously rejected, update to new pending request
            existing.status = "pending"
            existing.requester_id = current_user.id # Ensure current user is the requester
            existing.receiver_id = request_data.receiver_id
            existing.requested_at = datetime.utcnow()
            existing.responded_at = None
            db.commit()
            db.refresh(existing)
            return existing
    
    # Create request
    new_request = DatemateConnection(
        requester_id=current_user.id,
        receiver_id=request_data.receiver_id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return new_request


@router.post("/request/{user_id}", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
def send_connection_request_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a datemate connection request to another user (alternate endpoint)."""
    # Can't request yourself
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send request to yourself")
    
    # Check if connection already exists with pending or accepted status
    existing = db.query(DatemateConnection).filter(
        ((DatemateConnection.requester_id == current_user.id) & (DatemateConnection.receiver_id == user_id)) |
        ((DatemateConnection.requester_id == user_id) & (DatemateConnection.receiver_id == current_user.id)),
        DatemateConnection.status.in_(["pending", "accepted"])
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Connection request already exists")
    
    # Create request
    new_request = DatemateConnection(
        requester_id=current_user.id,
        receiver_id=user_id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return new_request


@router.get("/", response_model=List[ConnectionResponse])
def get_my_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all connections (accepted datemates) for current user."""
    connections = db.query(DatemateConnection).filter(
        ((DatemateConnection.requester_id == current_user.id) | 
         (DatemateConnection.receiver_id == current_user.id)) &
        (DatemateConnection.status == "accepted")
    ).all()
    
    return connections


@router.get("/pending", response_model=List[ConnectionResponse])
def get_pending_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending connection requests received by current user."""
    requests = db.query(DatemateConnection).filter(
        DatemateConnection.receiver_id == current_user.id,
        DatemateConnection.status == "pending"
    ).all()
    
    return requests


@router.get("/sent", response_model=List[ConnectionResponse])
def get_sent_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending connection requests sent by current user."""
    requests = db.query(DatemateConnection).filter(
        DatemateConnection.requester_id == current_user.id,
        DatemateConnection.status == "pending"
    ).all()
    
    return requests


@router.post("/accept/{connection_id}", response_model=ConnectionResponse)
def accept_connection(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a connection request and transfer random chat history."""
    from app.models.random_chat_history import RandomChatHistory
    from app.models.message import PrivateMessage
    
    connection = db.query(DatemateConnection).filter(
        DatemateConnection.id == connection_id,
        DatemateConnection.receiver_id == current_user.id,
        DatemateConnection.status == "pending"
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection request not found")
    
    # Accept the connection
    connection.status = "accepted"
    connection.responded_at = datetime.utcnow()
    
    # Find any random chat history between these two users
    requester_id = connection.requester_id
    receiver_id = connection.receiver_id
    
    # Query for messages between these users (in either direction)
    random_chat_messages = db.query(RandomChatHistory).filter(
        ((RandomChatHistory.sender_id == requester_id) & (RandomChatHistory.receiver_id == receiver_id)) |
        ((RandomChatHistory.sender_id == receiver_id) & (RandomChatHistory.receiver_id == requester_id))
    ).order_by(RandomChatHistory.sent_at).all()
    
    # Transfer messages to PrivateMessage table
    for msg in random_chat_messages:
        private_msg = PrivateMessage(
            connection_id=connection.id,
            sender_id=msg.sender_id,
            receiver_id=msg.receiver_id,
            message_text=msg.message_text,
            sent_at=msg.sent_at
        )
        db.add(private_msg)
    
    # Delete the temporary random chat history
    for msg in random_chat_messages:
        db.delete(msg)
    
    db.commit()
    db.refresh(connection)
    
    return connection


@router.put("/{connection_id}/reject", response_model=ConnectionResponse)
def reject_connection(
    connection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a connection request."""
    connection = db.query(DatemateConnection).filter(
        DatemateConnection.id == connection_id,
        DatemateConnection.receiver_id == current_user.id,
        DatemateConnection.status == "pending"
    ).first()
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection request not found")
    
    connection.status = "rejected"
    connection.responded_at = datetime.utcnow()
    db.commit()
    db.refresh(connection)
    
    return connection
