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

async def get_wingman_suggestion(partner_profile: str, chat_history: List[Dict[str, str]] = None) -> List[str]:
    """FR-19: AI Wingman"""
    system_prompt = (
        "You are a professional dating coach and 'wingman'. "
        "Based on the following user profile, suggest 3 creative, personalized "
        "opening lines or conversation starters that are respectful and engaging."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Partner profile: {partner_profile}"}
    ]
    
    if chat_history:
        messages[1]["content"] += f"\n\nCurrent conversation context: {chat_history}"
    
    response = await chat_completion(messages)
    if "error" in response:
        return ["Hi there!", "How's your day going?", "I like your profile!"]
        
    return response["choices"][0]["message"]["content"].split('\n')

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

async def practice_chat_response(message: str, history: List[Dict[str, str]] = None, scenario: str = "first_date") -> str:
    """FR-22: AI Practice Mode"""
    scenario_prompts = {
        "first_date": "Act as someone on a first date. Be friendly, curious, and slightly nervous.",
        "casual_chat": "Act as a casual match on a dating app. Be relaxed and conversational.",
        "flirty": "Act as someone who's interested and flirty, but respectful.",
    }
    
    system_prompt = (
        f"You are practicing dating conversation. {scenario_prompts.get(scenario, scenario_prompts['first_date'])} "
        "Respond naturally to the user's messages. Be friendly but realistic. Do not break character."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})
    
    response = await chat_completion(messages)
    if "error" in response:
        return "..."
        
    return response["choices"][0]["message"]["content"]

async def imitate_ex(message: str, history: List[Dict[str, str]] = None, chat_history_context: str = None) -> str:
    """FR-17: Miss Ex"""
    system_prompt = (
        f"Imitate the communication style found in the following chat history context: "
        f"'{chat_history_context or 'casual and friendly'}'. Respond to the user's message in that style."
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
