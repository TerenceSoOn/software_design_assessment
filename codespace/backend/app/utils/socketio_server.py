"""
Socket.IO server for real-time random chat matching.

Handles:
- User queue management
- Gender-based matching
- Real-time message broadcasting
- Connection/disconnection handling
"""
import socketio
import uuid
from collections import deque
from typing import Dict, Optional
from datetime import datetime
from app.config import settings
from app.utils.security import decode_access_token
from app.database import SessionLocal
from app.models.random_chat_history import RandomChatHistory

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*' # Allow all origins for Socket.IO
)

# Data structures for matching
waiting_queue: deque = deque()  # Users waiting for a match
active_chats: Dict[str, dict] = {}  # sid -> {partner_sid, user_id, partner_user_id, session_id}
sid_to_user: Dict[str, dict] = {}  # sid -> {user_id, gender, preferred_gender, profile}


def check_match_compatibility(user1: dict, user2: dict) -> bool:
    """
    Check if two users are compatible for matching based on gender preferences.
    
    Args:
        user1: First user dict with gender and preferred_gender
        user2: Second user dict with gender and preferred_gender
    
    Returns:
        True if users are compatible for matching
    """
    # User1 wants user2's gender (or any)
    user1_wants_user2 = (
        user1['preferred_gender'] == 'any' or 
        user1['preferred_gender'] == user2['gender']
    )
    
    # User2 wants user1's gender (or any)
    user2_wants_user1 = (
        user2['preferred_gender'] == 'any' or 
        user2['preferred_gender'] == user1['gender']
    )
    
    return user1_wants_user2 and user2_wants_user1


async def try_match_user(sid: str):
    """
    Try to find a match for the given user from the waiting queue.
    
    Args:
        sid: Socket ID of the user to match
    """
    if sid not in sid_to_user:
        return
    
    current_user = sid_to_user[sid]
    
    # Search through waiting queue for a compatible match
    for i, waiting_sid in enumerate(waiting_queue):
        if waiting_sid not in sid_to_user:
            continue
            
        waiting_user = sid_to_user[waiting_sid]
        
        # Check compatibility
        if check_match_compatibility(current_user, waiting_user):
            # Remove from queue
            waiting_queue.remove(waiting_sid)
            
            # Generate unique session ID for this chat
            session_id = str(uuid.uuid4())
            
            # Create chat session
            active_chats[sid] = {
                'partner_sid': waiting_sid,
                'user_id': current_user['user_id'],
                'partner_user_id': waiting_user['user_id'],
                'session_id': session_id
            }
            active_chats[waiting_sid] = {
                'partner_sid': sid,
                'user_id': waiting_user['user_id'],
                'partner_user_id': current_user['user_id'],
                'session_id': session_id
            }
            
            # Notify both users of the match
            await sio.emit('match_found', {
                'partner': {
                    'user_id': waiting_user['user_id'],
                    'display_name': waiting_user['profile'].get('display_name'),
                    'age': waiting_user['profile'].get('age'),
                    'interests': waiting_user['profile'].get('interests'),
                    'bio': waiting_user['profile'].get('bio'),
                    'gender': waiting_user['profile'].get('gender'),
                    'avatar_url': waiting_user['profile'].get('avatar_url')
                }
            }, room=sid)
            
            await sio.emit('match_found', {
                'partner': {
                    'user_id': current_user['user_id'],
                    'display_name': current_user['profile'].get('display_name'),
                    'age': current_user['profile'].get('age'),
                    'interests': current_user['profile'].get('interests'),
                    'bio': current_user['profile'].get('bio'),
                    'gender': current_user['profile'].get('gender'),
                    'avatar_url': current_user['profile'].get('avatar_url')
                }
            }, room=waiting_sid)
            
            return
    
    # No match found, add to queue
    if sid not in waiting_queue:
        waiting_queue.append(sid)
        await sio.emit('searching', {'message': 'Searching for a compatible partner...'}, room=sid)


@sio.event
async def connect(sid, environ, auth=None):
    """Handle new Socket.IO connection."""
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid, reason=None):
    """Handle Socket.IO disconnection."""
    print(f"Client disconnected: {sid}, reason: {reason}")
    
    # Remove from queue if waiting
    try:
        if sid in waiting_queue:
            waiting_queue.remove(sid)
    except ValueError:
        pass # Already removed
    
    # Notify partner if in active chat
    if sid in active_chats:
        chat_info = active_chats.pop(sid, None)
        if chat_info:
            partner_sid = chat_info.get('partner_sid')
            if partner_sid and partner_sid in active_chats:
                await sio.emit('partner_disconnected', {}, room=partner_sid)
                active_chats.pop(partner_sid, None)
    
    # Remove user data
    if sid in sid_to_user:
        del sid_to_user[sid]


@sio.event
async def join_queue(sid, data):
    """
    User joins the matching queue.
    
    Expected data: {token: JWT token}
    """
    try:
        # Decode and verify JWT token
        token = data.get('token')
        if not token:
            await sio.emit('error', {'message': 'Authentication token required'}, room=sid)
            return
        
        payload = decode_access_token(token)
        if not payload:
            await sio.emit('error', {'message': 'Invalid or expired token'}, room=sid)
            return
        
        user_id = payload.get('user_id')
        
        # Get user profile from database (we'll need to pass db session)
        # For now, use data from frontend
        user_data = {
            'user_id': user_id,
            'gender': data.get('gender'),
            'preferred_gender': data.get('preferred_gender'),
            'profile': data.get('profile', {})
        }
        
        sid_to_user[sid] = user_data
        
        # Try to find a match
        await try_match_user(sid)
        
    except Exception as e:
        print(f"Error in join_queue: {e}")
        await sio.emit('error', {'message': 'Failed to join queue'}, room=sid)


@sio.event
async def send_message(sid, data):
    """
    Send a message to the matched partner.
    
    Expected data: {message: str, timestamp: str}
    """
    if sid not in active_chats:
        await sio.emit('error', {'message': 'Not in an active chat'}, room=sid)
        return
    
    partner_sid = active_chats[sid]['partner_sid']
    sender_user_id = active_chats[sid]['user_id']
    receiver_user_id = active_chats[sid]['partner_user_id']
    session_id = active_chats[sid]['session_id']
    
    message_text = data.get('message')
    
    # Save message to database (random chat history)
    try:
        db = SessionLocal()
        history_entry = RandomChatHistory(
            session_id=session_id,
            sender_id=sender_user_id,
            receiver_id=receiver_user_id,
            message_text=message_text,
            sent_at=datetime.utcnow()
        )
        db.add(history_entry)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Error saving chat history: {e}")
    
    message_data = {
        'message': message_text,
        'timestamp': data.get('timestamp'),
        'sender_id': sender_user_id
    }
    
    # Send to partner
    await sio.emit('receive_message', message_data, room=partner_sid)


@sio.event
async def leave_chat(sid):
    """User voluntarily leaves the current chat."""
    if sid in active_chats:
        partner_sid = active_chats[sid]['partner_sid']
        
        # Notify partner
        if partner_sid in active_chats:
            await sio.emit('partner_left', {}, room=partner_sid)
            del active_chats[partner_sid]
        
        del active_chats[sid]
        await sio.emit('chat_ended', {}, room=sid)


@sio.event
async def send_datemate_request(sid, data):
    """Send a datemate request to the current chat partner."""
    if sid not in active_chats:
        await sio.emit('error', {'message': 'Not in an active chat'}, room=sid)
        return
    
    partner_sid = active_chats[sid]['partner_sid']
    sender_user_id = active_chats[sid]['user_id']
    
    # Notify partner of datemate request
    await sio.emit('datemate_request_received', {
        'from_user_id': sender_user_id,
        'message': data.get('message', 'Would like to be datemates!')
    }, room=partner_sid)
    
    # Confirm to sender
    await sio.emit('datemate_request_sent', {}, room=sid)
