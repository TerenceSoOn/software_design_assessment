from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.random_chat_history import RandomChatHistory
from app.models.message import PrivateMessage
from app.schemas.report import ReportRequest, ReportResponse
from app.utils.dependencies import get_current_user
from app.utils.deepseek import judge_chat_behavior

from app.models.profile import Profile
from app.models.connection import DatemateConnection

router = APIRouter(prefix="/report", tags=["Report"])

@router.post("/", response_model=ReportResponse)
async def report_user(
    request: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Report a user for inappropriate behavior.
    Chat history is analyzed by AI. If guilty, the user is deleted.
    """
    
    # 1. Fetch Chat History
    chat_history = []
    
    if request.chat_type == "random":
        if not request.session_id:
            raise HTTPException(status_code=400, detail="session_id required for random chat report")
            
        messages = db.query(RandomChatHistory).filter(
            RandomChatHistory.session_id == request.session_id
        ).order_by(RandomChatHistory.sent_at).all()
        
        chat_history = [
            {"sender_id": msg.sender_id, "content": msg.message_text} 
            for msg in messages
        ]
        
    elif request.chat_type == "private":
        if not request.partner_id:
             raise HTTPException(status_code=400, detail="partner_id required for private chat report")
             
        # Verify partner_id matches reported_user_id (or just use reported_user_id as the filter)
        # The reported user MUST be the partner in the chat
        if request.reported_user_id != request.partner_id:
             raise HTTPException(status_code=400, detail="reported_user_id must match partner_id for private chat")

        messages = db.query(PrivateMessage).filter(
            or_(
                (PrivateMessage.sender_id == current_user.id) & (PrivateMessage.receiver_id == request.reported_user_id),
                (PrivateMessage.sender_id == request.reported_user_id) & (PrivateMessage.receiver_id == current_user.id)
            )
        ).order_by(PrivateMessage.sent_at).all()
        
        chat_history = [
            {"sender_id": msg.sender_id, "content": msg.message_text}
            for msg in messages
        ]
    else:
        raise HTTPException(status_code=400, detail="Invalid chat_type")

    if not chat_history:
        return ReportResponse(
            success=False,
            message="No chat history found to analyze.",
            action_taken="none"
        )

    # 2. AI Judgment
    judgment = await judge_chat_behavior(request.reported_user_id, chat_history)
    
    if judgment["guilty"]:
        # 3. Take Action (Delete User)
        user_to_delete = db.query(User).filter(User.id == request.reported_user_id).first()
        if user_to_delete:
            # We might want to notify the user via socket before deleting, but account deletion is immediate here.
            # Ideally, we should soft delete or just deactivate, but requirement says "delete from db".
            
            # Note: Deleting user might fail due to foreign key constraints if not set to CASCADE.
            # For this assessment, we'll try to delete. If it fails, we might need to clean up related data.
            # Assuming basic CASCADE or manual cleanup isn't strictly required unless it crashes.
            # Let's check dependencies. User has Profile, Messages, etc.
            # We'll wrap in try/except.
            
            try:
                # Manual cleanup might be needed if cascade isn't configured in models
                # Delete related profile first (1:1 relationship)
                db.query(Profile).filter(Profile.user_id == request.reported_user_id).delete()
                
                # Delete messages (sender or receiver) - Optional, depending on policy, but needed for FK constraints
                db.query(PrivateMessage).filter(or_(
                    PrivateMessage.sender_id == request.reported_user_id,
                    PrivateMessage.receiver_id == request.reported_user_id
                )).delete()
                
                # Delete connections
                db.query(DatemateConnection).filter(or_(
                    DatemateConnection.requester_id == request.reported_user_id,
                    DatemateConnection.receiver_id == request.reported_user_id
                )).delete()

                # Delete random chat history
                db.query(RandomChatHistory).filter(or_(
                    RandomChatHistory.sender_id == request.reported_user_id,
                    RandomChatHistory.receiver_id == request.reported_user_id
                )).delete()
                
                # Finally delete user
                db.delete(user_to_delete)
                db.commit()
                
                return ReportResponse(
                    success=True,
                    message=f"Report accepted. User found guilty of: {judgment['reason']}. Account deleted.",
                    action_taken="deleted"
                )
            except Exception as e:
                db.rollback()
                print(f"Failed to delete user: {e}")
                return ReportResponse(
                    success=True,
                    message=f"Report accepted. User found guilty but deletion failed: {str(e)}",
                    action_taken="error_deleting"
                )
    
    return ReportResponse(
        success=True,
        message=f"Report analyzed. User found NOT guilty. Reason: {judgment['reason']}",
        action_taken="none"
    )
