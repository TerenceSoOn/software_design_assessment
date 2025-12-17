"""
DeepSeek AI client for FlirtNet.
Handles interaction with DeepSeek API for AI features.
"""
import httpx
from typing import List, Dict, Any, Optional
from app.config import settings

async def chat_completion(
    messages: List[Dict[str, str]], 
    model: str = "deepseek-chat",
    temperature: float = 0.7,
    max_tokens: int = 500
) -> Dict[str, Any]:
    """
    Call DeepSeek chat completions API (OpenAI-compatible).
    POST https://api.deepseek.com/v1/chat/completions
    """
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.DEEPSEEK_API_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"DeepSeek API Error: {e}")
            return {"error": str(e)}

# --- AI Feature Implementations ---

async def get_ai_companion_response(message: str, history: List[Dict[str, str]] = None) -> str:
    """FR-16: AI Companion Chat"""
    system_prompt = (
        "You are a friendly, empathetic AI companion on FlirtNet, a dating app. "
        "Your goal is to provide emotional support and engaging conversation to users "
        "who haven't found a match yet. Be encouraging, warm, and a good listener."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = await chat_completion(messages)
    if "error" in response:
        return "I'm having trouble connecting right now. Please try again later."
        
    return response["choices"][0]["message"]["content"]

async def check_content_safety(text: str) -> Dict[str, Any]:
    """FR-23: AI Abuse & Harassment Detector"""
    system_prompt = (
        "You are a content safety moderator for a dating app. Analyze the following message "
        "for abusive, harassing, aggressive, or inappropriate content. "
        "Focus on context, tone, and repeated patterns, not just keywords. "
        "Return a JSON object with: "
        "{'is_safe': bool, 'reason': str, 'severity': 'low'|'medium'|'high'|'none'}"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    
    response = await chat_completion(messages, temperature=0.1) # Low temp for consistency
    if "error" in response:
        return {"is_safe": True, "reason": "Check failed", "severity": "none"}
        
    content = response["choices"][0]["message"]["content"]
    # In a real implementation, we'd parse the JSON from the content
    # For now, simple heuristic based on text analysis
    is_safe = "safe" in content.lower() and "unsafe" not in content.lower()
    return {
        "is_safe": is_safe,
        "analysis": content
    }

async def get_wingman_suggestion(
    partner_profile: str, 
    chat_history: List[Dict[str, str]] = None,
    user_profile: str = None
) -> Dict[str, Any]:
    """FR-19: AI Wingman - Analyze situation and provide suggestions"""
    
    # Build context
    context_parts = []
    if user_profile:
        context_parts.append(f"User A (the person asking for help):\n{user_profile}")
    if partner_profile:
        context_parts.append(f"User B (the person they're chatting with):\n{partner_profile}")
    
    chat_context = ""
    if chat_history:
        # Explicitly map roles to User A (User) and User B (Partner/Assistant) to avoid confusion
        role_map = {"user": "User A", "assistant": "User B", "system": "System"}
        chat_context = "\n".join([
            f"{role_map.get(msg.get('role', 'user'), 'User')}: {msg.get('content', '')}" 
            for msg in chat_history
        ])
    
    system_prompt = (
        "You are a dating coach helping User A continue their conversation with User B.\n\n"
        "RULES:\n"
        "1. Analyze the situation briefly\n"
        "2. Provide EXACTLY 3 message suggestions\n"
        "3. Each suggestion must be ONLY the message text - NO explanations, NO 'Why it works', NO numbering\n\n"
        "RESPOND IN THIS EXACT JSON FORMAT:\n"
        '{"analysis": "One sentence describing the current vibe", "suggestions": ["First message to send", "Second message to send", "Third message to send"]}\n\n'
        "CRITICAL: suggestions array must contain ONLY the actual messages User A should send. Nothing else."
    )
    
    user_content = ""
    if context_parts:
        user_content += "\n\n".join(context_parts) + "\n\n"
    if chat_context:
        user_content += f"Chat History:\n{chat_context}\n\n"
    user_content += "Please analyze and provide suggestions."
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    
    response = await chat_completion(messages, temperature=0.7)
    if "error" in response:
        return {
            "analysis": "Unable to analyze at this time.",
            "suggestions": ["How's your day going?", "Tell me more about yourself!", "What do you enjoy doing for fun?"]
        }
    
    content = response["choices"][0]["message"]["content"]
    
    # Try to parse JSON response
    import json
    try:
        # Clean up potential markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        return {
            "analysis": result.get("analysis", "Analysis not available."),
            "suggestions": result.get("suggestions", [])
        }
    except (json.JSONDecodeError, IndexError):
        # Fallback: try to extract suggestions from text
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        suggestions = [line for line in lines if line.startswith(('1.', '2.', '3.', '-', '*'))][:3]
        if not suggestions:
            suggestions = lines[:3] if len(lines) >= 3 else ["Say something nice!", "Ask about their interests!", "Share something about yourself!"]
        return {
            "analysis": content[:200] if len(content) > 200 else content,
            "suggestions": [s.lstrip('0123456789.-* ') for s in suggestions]
        }


async def optimize_profile(profile_text: str) -> str:
    """FR-21: AI Profile Optimizer"""
    system_prompt = (
        "You are an expert dating profile consultant. Review the following profile bio "
        "and provide specific, actionable tips to make it more attractive and authentic. "
        "Suggest improvements for clarity, tone, and engagement."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": profile_text}
    ]
    
    response = await chat_completion(messages)
    if "error" in response:
        return "Could not analyze profile at this time."
        
    return response["choices"][0]["message"]["content"]

async def analyze_atmosphere(chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """FR-20: Atmosphere Analyzer"""
    system_prompt = (
        "Analyze the following conversation from a dating app. "
        "Provide feedback on the atmosphere/mood. "
        "Return a JSON object with: "
        "{'mood_score': int (1-10), 'feedback': str, 'suggestions': str}"
    )
    
    # Convert chat history to readable format
    conversation_text = "\n".join([f"{msg.get('role', 'user')}: {msg.get('content', '')}" for msg in chat_history])
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": conversation_text}
    ]
    
    response = await chat_completion(messages)
    if "error" in response:
        return {"mood_score": 5, "feedback": "Analysis failed", "suggestions": ""}
        
    return {"analysis": response["choices"][0]["message"]["content"]}

async def practice_chat_response(
    message: str, 
    history: List[Dict[str, str]] = None, 
    scenario: str = "first_date",
    user_profile: Dict[str, Any] = None,
    preferences: Dict[str, Any] = None
) -> str:
    """FR-22: AI Practice Mode with Dynamic Persona"""
    
    system_prompt = ""
    
    if scenario == "random_persona":
        # Generate a dynamic persona based on user preferences
        preferred_gender = preferences.get("preferred_gender", "Any") if preferences else "Any"
        user_gender = user_profile.get("gender", "User") if user_profile else "User"
        
        system_prompt = (
            f"You are a potential match for a {user_gender} user on a dating app. "
            f"Your gender is {preferred_gender}. "
            "Create a unique, random personality for yourself (e.g., shy bookworm, adventurous traveler, witty comedian). "
            "IMPORTANT: Act like a 100% real person. Do NOT be overly polite or customer-service like. "
            "You can be slightly awkward, blunt, or use slang if it fits your persona. "
            "Do not reveal you are an AI unless explicitly asked. Keep responses concise and natural."
        )
    else:
        scenario_prompts = {
            "first_date": "Act as someone on a first date. Be friendly but realistic. Don't be too perfect.",
            "casual_chat": "Act as a casual match. You can be relaxed, maybe a bit dry or playful. Avoid formal language.",
            "flirty": "Act as someone who's interested. Be bold but realistic.",
        }
        system_prompt = (
            f"You are practicing dating conversation. {scenario_prompts.get(scenario, scenario_prompts['first_date'])} "
            "Respond naturally. Do NOT sound like a helpful assistant. Be a real human with flaws."
        )
    
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = await chat_completion(messages)
    if "error" in response:
        return "..."
        
    return response["choices"][0]["message"]["content"]

async def judge_chat_behavior(
    reported_user_id: int,
    chat_history: List[Dict[str, str]]
) -> Dict[str, Any]:
    """
    Judge if the reported user is guilty based on chat history.
    """
    system_prompt = (
        "You are a strict moderator for a dating app. Review the chat history and determine if "
        f"the user with ID {reported_user_id} has violated community guidelines "
        "(harassment, hate speech, explicit content without consent, scams, etc.). "
        "Return a JSON object with: "
        "{'guilty': bool, 'reason': str}"
    )

    # Convert chat history to readable format
    conversation_text = "\n".join([
        f"User {msg.get('sender_id', 'Unknown')}: {msg.get('content', '')}" 
        for msg in chat_history
    ])

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Chat History:\n{conversation_text}"}
    ]

    response = await chat_completion(messages, temperature=0.0)
    
    if "error" in response:
        # Fail safe: return not guilty if AI fails
        return {"guilty": False, "reason": "AI analysis failed"}

    content = response["choices"][0]["message"]["content"]
    
    import json
    try:
        # Clean up potential markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        result = json.loads(content)
        return {
            "guilty": result.get("guilty", False),
            "reason": result.get("reason", "No reason provided")
        }
    except json.JSONDecodeError:
        # Fallback heuristic
        guilty = "guilty" in content.lower() and "not guilty" not in content.lower()
        return {"guilty": guilty, "reason": content}

async def imitate_ex(
    message: str, 
    history: List[Dict[str, str]] = None, 
    chat_history_context: str = None,
    partner_profile: str = None
) -> str:
    """FR-17: Miss Ex / Simulate Reply"""
    
    context_instruction = ""
    if chat_history_context:
        context_instruction += f"STRICTLY imitate the communication style found in this chat history: '{chat_history_context}'. "
    
    if partner_profile:
        context_instruction += f"Act as the person described in this profile: '{partner_profile}'. "
        
    system_prompt = (
        f"{context_instruction}"
        "Respond to the user's message in that EXACT style and character. "
        "If the history shows short, rude, or dry replies, mimic that. "
        "Do NOT be polite if the context isn't. Do NOT act like an AI assistant. "
        "If no specific style is provided, act as a distant ex-partner."
    )
    
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = await chat_completion(messages)
    if "error" in response:
        return "..."
        
    return response["choices"][0]["message"]["content"]
