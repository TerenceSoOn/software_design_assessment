from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.utils.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.profile import Profile
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
    user_profile: Optional[Dict[str, Any]] = None # For dynamic persona
    preferences: Optional[Dict[str, Any]] = None # For dynamic persona

class SafetyCheckRequest(BaseModel):
    message: str

class WingmanRequest(BaseModel):
    partner_profile: str
    chat_history: Optional[List[Dict[str, str]]] = []

class AtmosphereRequest(BaseModel):
    chat_history: List[Dict[str, str]]

class ProfileOptimizeRequest(BaseModel):
    current_bio: str

class MissExRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None
    ex_chat_history: Optional[str] = None
    target_user_id: Optional[int] = None # New: Target user to imitate

# --- Endpoints ---

@router.post("/companion")
async def ai_companion_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """
    FR-16 & FR-22: Chat with AI Companion or Practice Mode.
    """
    if request.scenario:
        # Practice mode logic handles fetching profile if not provided
        # But here we can inject it if needed, or let practice_chat_endpoint handle it
        # For now, we'll just pass through
        response = await practice_chat_response(request.message, request.history, request.scenario)
    else:
        # Companion mode
        response = await get_ai_companion_response(request.message, request.history)
    
    return {"response": response}

@router.post("/practice")
async def practice_chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    """FR-22: Practice dating conversation (alias for companion with scenario)."""
    
    # Fetch user profile and preferences from DB if not provided in request
    user_profile_data = request.user_profile
    preferences_data = request.preferences
    
    if not user_profile_data or not preferences_data:
        # Access profile via relationship (assuming backref 'profile' returns a list or object)
        # Since we don't have easy access to relationship loading strategy here without session, 
        # we rely on lazy loading or explicit query if needed. 
        # But wait, current_user is detached? No, usually attached if from dependency.
        # Let's assume current_user.profile works.
        
        profile = current_user.profile
        if isinstance(profile, list) and profile:
            profile = profile[0]
        
        if profile:
            if not user_profile_data:
                user_profile_data = {
                    "gender": profile.gender,
                    "age": profile.age,
                    "interests": profile.interests
                }
            if not preferences_data:
                preferences_data = {
                    "preferred_gender": profile.preferred_gender
                }
    
    response = await practice_chat_response(
        request.message, 
        request.history, 
        request.scenario or "random_persona",
        user_profile_data,
        preferences_data
    )
    return {"response": response}

@router.post("/safety-check")
async def safety_check(request: SafetyCheckRequest, current_user: User = Depends(get_current_user)):
    """FR-23: Check content safety for abuse/harassment."""
    result = await check_content_safety(request.message)
    return result

@router.post("/wingman")
async def wingman_suggestions(
    request: WingmanRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """FR-19: Get conversation analysis and suggestions based on profiles and chat history."""
    
    # Get current user's profile (User A)
    user_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    user_profile_str = None
    if user_profile:
        user_profile_str = f"Name: {user_profile.display_name}, Bio: {user_profile.bio or 'No bio'}, Interests: {user_profile.interests or []}"
    
    result = await get_wingman_suggestion(
        partner_profile=request.partner_profile,  # User B profile (already stringified from frontend)
        chat_history=request.chat_history,
        user_profile=user_profile_str  # User A profile
    )
    # Result is already a dict with 'analysis' and 'suggestions'
    return result

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
async def miss_ex_chat(
    request: MissExRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """FR-17: Chat with AI that imitates ex's communication style."""
    
    partner_profile_str = None
    
    if request.target_user_id:
        # Fetch target user's profile
        target_profile = db.query(Profile).filter(Profile.user_id == request.target_user_id).first()
        if target_profile:
            partner_profile_str = (
                f"Name: {target_profile.display_name}, "
                f"Age: {target_profile.age}, "
                f"Gender: {target_profile.gender}, "
                f"Bio: {target_profile.bio}, "
                f"Interests: {', '.join(target_profile.interests) if target_profile.interests else 'None'}"
            )
    
    response = await imitate_ex(
        request.message, 
        request.history, 
        request.ex_chat_history,
        partner_profile_str
    )
    return {"response": response}
