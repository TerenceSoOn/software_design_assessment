"""
AI Router - Endpoints for AI-powered features.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.utils.deepseek import (
    get_ai_companion_response,
    check_content_safety,
    get_wingman_suggestion,
    optimize_profile,
    analyze_atmosphere,
    practice_chat_response,
    imitate_ex
)

router = APIRouter(prefix="/ai", tags=["AI Features"])

# --- Request Schemas ---

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None
    scenario: Optional[str] = None  # For practice mode

class SafetyCheckRequest(BaseModel):
    message: str  # Changed from 'text' to match test

class WingmanRequest(BaseModel):
    partner_profile: str
    chat_history: Optional[List[Dict[str, str]]] = []  # Added for context

class AtmosphereRequest(BaseModel):
    chat_history: List[Dict[str, str]]  # Changed from conversation_text

class ProfileOptimizeRequest(BaseModel):
    current_bio: str  # Changed from profile_text to match test

class MissExRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None
    ex_chat_history: Optional[str] = None  # Changed from ex_style_samples

# --- Endpoints ---

@router.post("/companion")
async def ai_companion_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """
    FR-16 & FR-22: Chat with AI Companion or Practice Mode.
    
    If scenario is provided, it's practice mode.
    Otherwise, it's companion mode for dating advice.
    """
    if request.scenario:
        # Practice mode
        response = await practice_chat_response(request.message, request.history, request.scenario)
    else:
        # Companion mode
        response = await get_ai_companion_response(request.message, request.history)
    
    return {"response": response}

@router.post("/practice")
async def practice_chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """FR-22: Practice dating conversation (alias for companion with scenario)."""
    response = await practice_chat_response(
        request.message, 
        request.history, 
        request.scenario or "first_date"
    )
    return {"response": response}

@router.post("/safety-check")
async def safety_check(request: SafetyCheckRequest, current_user: User = Depends(get_current_user)):
    """FR-23: Check content safety for abuse/harassment."""
    result = await check_content_safety(request.message)
    return result

@router.post("/wingman")
async def wingman_suggestions(request: WingmanRequest, current_user: User = Depends(get_current_user)):
    """FR-19: Get conversation starters and suggestions based on partner's profile."""
    suggestions = await get_wingman_suggestion(
        request.partner_profile,
        request.chat_history
    )
    return {"suggestions": suggestions}

@router.post("/atmosphere")
async def atmosphere_analyze(request: AtmosphereRequest, current_user: User = Depends(get_current_user)):
    """FR-20: Analyze conversation atmosphere and mood."""
    analysis = await analyze_atmosphere(request.chat_history)
    return {"analysis": analysis}

@router.post("/optimize-profile")
async def profile_optimize(request: ProfileOptimizeRequest, current_user: User = Depends(get_current_user)):
    """FR-21: Get AI suggestions to optimize profile bio."""
    suggestions = await optimize_profile(request.current_bio)
    return {"suggestions": suggestions}

@router.post("/miss-ex")
async def miss_ex_chat(request: MissExRequest, current_user: User = Depends(get_current_user)):
    """FR-17: Chat with AI that imitates ex's communication style."""
    response = await imitate_ex(
        request.message, 
        request.history, 
        request.ex_chat_history
    )
    return {"response": response}
