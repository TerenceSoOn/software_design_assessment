import asyncio
import socketio
import aiohttp

# Configuration
BASE_URL = "http://localhost:8000"
SOCKET_URL = "http://localhost:8000"

# Test Users
USER_A = {
    "username": "user_a", 
    "email": "user_a@example.com",
    "password": "password123", 
    "gender": "Male", 
    "preferred_gender": "Female"
}
USER_B = {
    "username": "user_b", 
    "email": "user_b@example.com",
    "password": "password123", 
    "gender": "Female", 
    "preferred_gender": "Male"
}

async def register_and_login(session, user_data):
    # Register
    async with session.post(f"{BASE_URL}/auth/register", json=user_data) as resp:
        if resp.status not in [201, 400]: # 400 if already exists
            print(f"Registration failed for {user_data['username']}: {resp.status}")
            text = await resp.text()
            print(f"Response: {text}")
            
    # Login
    async with session.post(f"{BASE_URL}/auth/login", json={
        "username": user_data['username'],
        "password": user_data['password']
    }) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data['access_token']
        else:
            print(f"Login failed for {user_data['username']}: {resp.status}")
            text = await resp.text()
            print(f"Response: {text}")
            return None

async def run_client(username, token, partner_username):
    # Enable logging
    # sio = socketio.AsyncClient(logger=True, engineio_logger=True)
    sio = socketio.AsyncClient()
    
    connected_future = asyncio.Future()
    matched_future = asyncio.Future()
    message_received_future = asyncio.Future()
    
    @sio.event
    async def connect():
        print(f"[{username}] Connected to socket")
        connected_future.set_result(True)
        
    @sio.event
    async def connect_error(data):
        print(f"[{username}] Connection failed: {data}")
        
    @sio.event
    async def disconnect():
        print(f"[{username}] Disconnected")
        
    @sio.event
    async def match_found(data):
        print(f"[{username}] Match found! Partner: {data.get('partner_name')}")
        matched_future.set_result(data)
        
    @sio.event
    async def receive_message(data):
        print(f"[{username}] Received message: {data['message']}")
        # Note: server sends sender_id, not username. 
        # For this test, we assume any message received is from partner since we don't echo back to sender in server logic usually
        # But let's just set result.
        message_received_future.set_result(data)

    try:
        # Try connecting with polling first, then upgrade to websocket
        await sio.connect(SOCKET_URL, auth={'token': token}, transports=['polling', 'websocket'])
        await connected_future
        
        # Join random chat
        print(f"[{username}] Joining random chat...")
        # await sio.emit('join_random_chat')
        await sio.emit('join_queue', {
            'token': token,
            'gender': 'Male' if username == 'user_a' else 'Female',
            'preferred_gender': 'Female' if username == 'user_a' else 'Male',
            'profile': {
                'display_name': username,
                'age': 25,
                'interests': ['coding']
            }
        })
        
        # Wait for match
        match_data = await asyncio.wait_for(matched_future, timeout=10.0)
        # room_id = match_data['room_id'] # Not used in this server implementation
        
        # If User A, send message
        if username == "user_a":
            await asyncio.sleep(1) # Wait for both to be ready
            print(f"[{username}] Sending message...")
            # await sio.emit('send_message', {'room_id': room_id, 'message': f"Hello from {username}"})
            await sio.emit('send_message', {'message': f"Hello from {username}", 'timestamp': "2025-01-01T12:00:00Z"})
            
        # Wait for message (User B should receive it)
        if username == "user_b":
            await asyncio.wait_for(message_received_future, timeout=10.0)
            print(f"[{username}] Verified message receipt!")
            
        await asyncio.sleep(2) # Keep connection alive briefly
        await sio.disconnect()
        return True
        
    except Exception as e:
        print(f"[{username}] Error: {e}")
        return False

async def main():
    async with aiohttp.ClientSession() as session:
        print("--- Setting up users ---")
        token_a = await register_and_login(session, USER_A)
        token_b = await register_and_login(session, USER_B)
        
        if not token_a or not token_b:
            print("Failed to get tokens")
            return

        print("\n--- Starting Concurrent Chat Verification ---")
        # Run both clients concurrently
        results = await asyncio.gather(
            run_client("user_a", token_a, "user_b"),
            run_client("user_b", token_b, "user_a")
        )
        
        if all(results):
            print("\n✅ SUCCESS: Multi-user random chat verified!")
        else:
            print("\n❌ FAILURE: Multi-user chat verification failed.")

if __name__ == "__main__":
    asyncio.run(main())
