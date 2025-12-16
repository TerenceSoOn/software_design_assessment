"""
Messages router - Private messaging between datemates.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.message import PrivateMessage
from app.models.connection import DatemateConnection
from app.utils.dependencies import get_current_user
from pydantic import BaseModel


router = APIRouter(prefix="/messages", tags=["Messages"])


class MessageCreate(BaseModel):
    """Schema for creating a message."""
    content: Optional[str] = ""  # 允许为空（纯图片消息）
    image_url: Optional[str] = None  # 图片 URL


class MessageResponse(BaseModel):
    """Schema for message in responses."""
    id: int
    sender_id: int
    receiver_id: int
    content: Optional[str] = ""
    image_url: Optional[str] = None  # 图片 URL
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[MessageResponse])
def get_all_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages for current user (all conversations)."""
    messages = db.query(PrivateMessage).filter(
        (PrivateMessage.sender_id == current_user.id) | (PrivateMessage.receiver_id == current_user.id)
    ).order_by(PrivateMessage.sent_at.desc()).all()
    
    # Convert to response format
    result = []
    for msg in messages:
        result.append(MessageResponse(
            id=msg.id,
            sender_id=msg.sender_id,
            receiver_id=msg.receiver_id,
            content=msg.message_text or "",
            image_url=msg.image_url,
            is_read=msg.read_at is not None,
            created_at=msg.sent_at
        ))
    
    return result


@router.get("/{user_id}", response_model=List[MessageResponse])
def get_messages_with_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages between current user and specified user."""
    # Check if users are connected (datemates)
    connection = db.query(DatemateConnection).filter(
        ((DatemateConnection.requester_id == current_user.id) & (DatemateConnection.receiver_id == user_id)) |
        ((DatemateConnection.requester_id == user_id) & (DatemateConnection.receiver_id == current_user.id)),
        DatemateConnection.status == "accepted"
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=403, 
            detail="You can only message users who are your datemates"
        )
    
    # Get messages
    messages = db.query(PrivateMessage).filter(
        ((PrivateMessage.sender_id == current_user.id) & (PrivateMessage.receiver_id == user_id)) |
        ((PrivateMessage.sender_id == user_id) & (PrivateMessage.receiver_id == current_user.id))
    ).order_by(PrivateMessage.sent_at).all()
    
    # Convert to response format
    result = []
    for msg in messages:
        result.append(MessageResponse(
            id=msg.id,
            sender_id=msg.sender_id,
            receiver_id=msg.receiver_id,
            content=msg.message_text or "",
            image_url=msg.image_url,
            is_read=msg.read_at is not None,
            created_at=msg.sent_at
        ))
    
    return result


@router.post("/{user_id}", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    user_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to a datemate."""
    # Check if users are connected (datemates)
    connection = db.query(DatemateConnection).filter(
        ((DatemateConnection.requester_id == current_user.id) & (DatemateConnection.receiver_id == user_id)) |
        ((DatemateConnection.requester_id == user_id) & (DatemateConnection.receiver_id == current_user.id)),
        DatemateConnection.status == "accepted"
    ).first()
    
    if not connection:
        raise HTTPException(
            status_code=403,
            detail="You can only message users who are your datemates"
        )
    
    # 验证：至少要有文本或图片
    if not message_data.content and not message_data.image_url:
        raise HTTPException(
            status_code=400,
            detail="Message must have content or image"
        )
    
    # Create message
    new_message = PrivateMessage(
        connection_id=connection.id,
        sender_id=current_user.id,
        receiver_id=user_id,
        message_text=message_data.content or "",
        image_url=message_data.image_url
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return MessageResponse(
        id=new_message.id,
        sender_id=new_message.sender_id,
        receiver_id=new_message.receiver_id,
        content=new_message.message_text or "",
        image_url=new_message.image_url,
        is_read=new_message.read_at is not None,
        created_at=new_message.sent_at
    )


@router.put("/{message_id}/read", response_model=MessageResponse)
def mark_message_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a message as read."""
    message = db.query(PrivateMessage).filter(
        PrivateMessage.id == message_id,
        PrivateMessage.receiver_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.read_at = datetime.utcnow()
    db.commit()
    db.refresh(message)
    
    return MessageResponse(
        id=message.id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.message_text or "",
        image_url=message.image_url,
        is_read=message.read_at is not None,
        created_at=message.sent_at
    )
