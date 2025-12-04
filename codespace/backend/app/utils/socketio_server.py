"""
Socket.IO server for real-time random chat matching.

Handles:
- User queue management
- Gender-based matching
- Real-time message broadcasting
- Connection/disconnection handling
"""
import socketio
from collections import deque
from typing import Dict, Optional
from app.config import settings
from app.utils.security import decode_access_token

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]
)

# Data structures for matching
waiting_queue: deque = deque()  # Users waiting for a match
active_chats: Dict[str, dict] = {}  # sid -> {partner_sid, user_id, partner_user_id}
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
            
            # Create chat session
            active_chats[sid] = {
                'partner_sid': waiting_sid,
                'user_id': current_user['user_id'],
                'partner_user_id': waiting_user['user_id']
            }
            active_chats[waiting_sid] = {
                'partner_sid': sid,
                'user_id': waiting_user['user_id'],
                'partner_user_id': current_user['user_id']
            }
            
            # Notify both users of the match
            await sio.emit('match_found', {
                'partner': {
                    'user_id': waiting_user['user_id'],
                    'display_name': waiting_user['profile']['display_name'],
                    'age': waiting_user['profile']['age'],
                    'interests': waiting_user['profile']['interests']
                }
            }, room=sid)
            
            await sio.emit('match_found', {
                'partner': {
                    'user_id': current_user['user_id'],
                    'display_name': current_user['profile']['display_name'],
                    'age': current_user['profile']['age'],
                    'interests': current_user['profile']['interests']
                }
            }, room=waiting_sid)
            
            return
    
    # No match found, add to queue
    if sid not in waiting_queue:
        waiting_queue.append(sid)
        await sio.emit('searching', {'message': 'Searching for a compatible partner...'}, room=sid)


@sio.event
async def connect(sid, environ):
    """Handle new Socket.IO connection."""
    print(f"Client connected: {sid}")


@sio.event
async def disconnect(sid):
    """Handle Socket.IO disconnection."""
    print(f"Client disconnected: {sid}")
    
    # Remove from queue if waiting
    if sid in waiting_queue:
        waiting_queue.remove(sid)
    
    # Notify partner if in active chat
    if sid in active_chats:
        partner_sid = active_chats[sid]['partner_sid']
        if partner_sid in active_chats:
            await sio.emit('partner_disconnected', {}, room=partner_sid)
            del active_chats[partner_sid]
        del active_chats[sid]
    
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
    
    message_data = {
        'message': data.get('message'),
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
