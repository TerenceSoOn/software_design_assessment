from pydantic import BaseModel
from typing import Optional

class ReportRequest(BaseModel):
    reported_user_id: int
    chat_type: str  # "random" or "private"
    session_id: Optional[str] = None # For random chat
    partner_id: Optional[int] = None # For private chat, to identify the conversation
    reason: Optional[str] = None

class ReportResponse(BaseModel):
    success: bool
    message: str
    action_taken: str # "none", "deleted"
