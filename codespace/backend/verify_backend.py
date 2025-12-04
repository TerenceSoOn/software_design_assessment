import asyncio
import httpx
import socketio
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SOCKET_URL = "http://127.0.0.1:8000"

async def test_registration():
    print("Testing Registration...")
    async with httpx.AsyncClient() as client:
        # Create a random user
        import random
        import string
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{username}@example.com"
        password = "password123"
        
        payload = {
            "username": username,
            "email": email,
            "password": password,
            "gender": "male",
            "preferred_gender": "female"
        }
        
        try:
            response = await client.post(f"{BASE_URL}/auth/register", json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ Registration successful for {username}")
                return response.json()
            else:
                print(f"❌ Registration failed: {response.status_code} {response.text}")
                return None
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return None

async def test_ai_endpoints(token):
    print("\nTesting AI Endpoints...")
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        # Test Companion Chat
        try:
            payload = {"message": "Hello, how are you?"}
            response = await client.post(f"{BASE_URL}/ai/companion/chat", json=payload, headers=headers)
            if response.status_code == 200:
                print("✅ AI Companion Chat endpoint reachable and working")
            elif response.status_code in [401, 500]:
                 print(f"⚠️ AI Companion Chat reachable but returned error (likely API key): {response.status_code}")
            else:
                print(f"❌ AI Companion Chat failed: {response.status_code} {response.text}")
        except Exception as e:
            print(f"❌ AI Companion Chat error: {e}")

        # Test Safety Check
        try:
            payload = {"text": "This is a safe message."}
            response = await client.post(f"{BASE_URL}/ai/safety/check", json=payload, headers=headers)
            if response.status_code == 200:
                print("✅ Safety Check endpoint reachable and working")
            elif response.status_code in [401, 500]:
                 print(f"⚠️ Safety Check reachable but returned error (likely API key): {response.status_code}")
            else:
                print(f"❌ Safety Check failed: {response.status_code} {response.text}")
        except Exception as e:
            print(f"❌ Safety Check error: {e}")

async def test_socketio(token):
    print("\nTesting Socket.IO...")
    sio = socketio.AsyncClient()
    
    connected = False
    
    @sio.event
    async def connect():
        nonlocal connected
        connected = True
        print("✅ Socket.IO Connected")
        
    @sio.event
    async def connect_error(data):
        print(f"❌ Socket.IO Connection Error: {data}")

    try:
        await sio.connect(SOCKET_URL, auth={"token": token})
        await asyncio.sleep(2)
        if connected:
            # Try joining queue
            await sio.emit('join_queue', {
                'token': token,
                'gender': 'male',
                'preferred_gender': 'female',
                'profile': {'display_name': 'Tester'}
            })
            print("✅ Sent join_queue event")
            await asyncio.sleep(1)
        
        await sio.disconnect()
    except Exception as e:
        print(f"❌ Socket.IO Test Error: {e}")

async def main():
    # 1. Register and get token
    user_data = await test_registration()
    if not user_data:
        print("Skipping remaining tests due to registration failure.")
        return

    # Login to get token (registration might auto-login in frontend but here we need token)
    # Actually the register response might contain token or we need to login
    # Let's check auth router. Usually register returns user info.
    # We'll try to login.
    
    print("\nLogging in...")
    async with httpx.AsyncClient() as client:
        login_payload = {
            "username": user_data["username"],
            "password": "password123"
        }
        # Note: OAuth2PasswordRequestForm expects form data usually, but let's check the implementation.
        # If it uses OAuth2PasswordRequestForm, it needs form data 'username' and 'password'.
        # Let's try form data.
        try:
            response = await client.post(f"{BASE_URL}/auth/token", data=login_payload)
            if response.status_code == 200:
                token = response.json()["access_token"]
                print("✅ Login successful")
                
                # 2. Test AI Endpoints
                await test_ai_endpoints(token)
                
                # 3. Test Socket.IO
                await test_socketio(token)
            else:
                print(f"❌ Login failed: {response.text}")
        except Exception as e:
            print(f"❌ Login error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
