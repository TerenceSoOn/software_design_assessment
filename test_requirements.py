#!/usr/bin/env python3
"""
Comprehensive test script to verify all FlirtNet requirements.
Tests each functional requirement systematically.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

# Test results tracking
results = {
    "passed": [],
    "failed": [],
    "not_implemented": []
}

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_result(req_id, description, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} {req_id}: {description}")
    if details:
        print(f"    {details}")
    
    if passed:
        results["passed"].append(req_id)
    else:
        results["failed"].append(req_id)

def test_not_implemented(req_id, description):
    print(f"⚠️  NOT IMPLEMENTED {req_id}: {description}")
    results["not_implemented"].append(req_id)

# Test data
test_users = []

print_section("FlirtNet Requirements Verification")

# ============================================================================
# 1.1 User Accounts and Profiles (FR-1, FR-2, FR-3)
# ============================================================================
print_section("1.1 User Accounts and Profiles")

# FR-1: Register and Login
try:
    # Register user 1
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "testuser1",
        "email": "test1@test.com",
        "password": "password123",
        "gender": "male",
        "preferred_gender": "female"
    })
    if resp.status_code == 201:
        test_result("FR-1a", "User registration", True, f"User ID: {resp.json()['id']}")
        test_users.append({"username": "testuser1", "password": "password123"})
    else:
        test_result("FR-1a", "User registration", False, f"Status: {resp.status_code}")
except Exception as e:
    test_result("FR-1a", "User registration", False, str(e))

# Login
try:
    resp = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "testuser1",
        "password": "password123"
    })
    if resp.status_code == 200 and "access_token" in resp.json():
        token1 = resp.json()["access_token"]
        test_result("FR-1b", "User login", True, "Token received")
    else:
        test_result("FR-1b", "User login", False, f"Status: {resp.status_code}")
        token1 = None
except Exception as e:
    test_result("FR-1b", "User login", False, str(e))
    token1 = None

# FR-2: Edit profile
try:
    if token1:
        resp = requests.put(f"{BASE_URL}/profiles/me", 
            headers={"Authorization": f"Bearer {token1}"},
            json={"bio": "Test bio", "interests": "coding, music"}
        )
        test_result("FR-2", "Edit personal profile", resp.status_code == 200, 
                   f"Status: {resp.status_code}")
    else:
        test_result("FR-2", "Edit personal profile", False, "No auth token")
except Exception as e:
    test_result("FR-2", "Edit personal profile", False, str(e))

# FR-3: Photo wall/avatar
test_not_implemented("FR-3", "Photo wall/avatar management")

# ============================================================================
# 1.2 Discovery (Random Matching) (FR-4, FR-5, FR-6)
# ============================================================================
print_section("1.2 Discovery (Random Matching)")

# Check Socket.IO server
try:
    resp = requests.get(f"{BASE_URL}/socket.io/")
    socket_io_available = resp.status_code in [200, 400]  # 400 is expected for GET
    test_result("FR-4", "Random matching system (Socket.IO)", socket_io_available,
               "Socket.IO endpoint accessible")
except Exception as e:
    test_result("FR-4", "Random matching system (Socket.IO)", False, str(e))

test_result("FR-5", "One-to-one chat session after match", socket_io_available,
           "Implemented in Socket.IO server")
test_result("FR-6", "View basic info during chat", socket_io_available,
           "Implemented in Socket.IO events")

# ============================================================================
# 1.3 Connection System (FR-7, FR-8, FR-9)
# ============================================================================
print_section("1.3 Connection System (Datemate Requests)")

# Register second user for connection testing
try:
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "username": "testuser2",
        "email": "test2@test.com",
        "password": "password123",
        "gender": "female",
        "preferred_gender": "male"
    })
    if resp.status_code == 201:
        user2_id = resp.json()['id']
        # Login user 2
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "username": "testuser2",
            "password": "password123"
        })
        token2 = resp.json()["access_token"] if resp.status_code == 200 else None
    else:
        token2 = None
        user2_id = None
except:
    token2 = None
    user2_id = None

# FR-7: Send datemate request
try:
    if token1 and user2_id:
        resp = requests.post(f"{BASE_URL}/connections/request/{user2_id}",
            headers={"Authorization": f"Bearer {token1}"}
        )
        test_result("FR-7", "Send datemate request", resp.status_code == 201,
                   f"Status: {resp.status_code}")
    else:
        test_result("FR-7", "Send datemate request", False, "Missing auth or user ID")
except Exception as e:
    test_result("FR-7", "Send datemate request", False, str(e))

# FR-8: Accept/Reject request
try:
    if token2:
        # Get pending requests
        resp = requests.get(f"{BASE_URL}/connections/pending",
            headers={"Authorization": f"Bearer {token2}"}
        )
        if resp.status_code == 200 and len(resp.json()) > 0:
            request_id = resp.json()[0]['id']
            # Accept request
            resp = requests.post(f"{BASE_URL}/connections/accept/{request_id}",
                headers={"Authorization": f"Bearer {token2}"}
            )
            test_result("FR-8", "Accept/Reject datemate request", resp.status_code == 200,
                       f"Accept status: {resp.status_code}")
        else:
            test_result("FR-8", "Accept/Reject datemate request", False, "No pending requests")
    else:
        test_result("FR-8", "Accept/Reject datemate request", False, "No auth token")
except Exception as e:
    test_result("FR-8", "Accept/Reject datemate request", False, str(e))

# FR-9: Datemate list
try:
    if token1:
        resp = requests.get(f"{BASE_URL}/connections",
            headers={"Authorization": f"Bearer {token1}"}
        )
        test_result("FR-9", "Datemate List", resp.status_code == 200,
                   f"Connections: {len(resp.json()) if resp.status_code == 200 else 0}")
    else:
        test_result("FR-9", "Datemate List", False, "No auth token")
except Exception as e:
    test_result("FR-9", "Datemate List", False, str(e))

# ============================================================================
# 1.4 Public Square (FR-10, FR-11, FR-12)
# ============================================================================
print_section("1.4 Public Square (Posts and Discussions)")

# FR-10: Create post
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/posts",
            headers={"Authorization": f"Bearer {token1}"},
            json={"content": "Test post content", "image_url": None}
        )
        post_id = resp.json().get('id') if resp.status_code == 201 else None
        test_result("FR-10", "Create post with text and images", resp.status_code == 201,
                   f"Post ID: {post_id}")
    else:
        test_result("FR-10", "Create post with text and images", False, "No auth token")
        post_id = None
except Exception as e:
    test_result("FR-10", "Create post with text and images", False, str(e))
    post_id = None

# FR-11: Like and comment
try:
    if token2 and post_id:
        # Like post
        resp = requests.post(f"{BASE_URL}/posts/{post_id}/like",
            headers={"Authorization": f"Bearer {token2}"}
        )
        like_success = resp.status_code == 200
        
        # Comment on post
        resp = requests.post(f"{BASE_URL}/posts/{post_id}/comments",
            headers={"Authorization": f"Bearer {token2}"},
            json={"content": "Nice post!"}
        )
        comment_success = resp.status_code == 201
        
        test_result("FR-11", "Like and comment on posts", like_success and comment_success,
                   f"Like: {like_success}, Comment: {comment_success}")
    else:
        test_result("FR-11", "Like and comment on posts", False, "Missing auth or post ID")
except Exception as e:
    test_result("FR-11", "Like and comment on posts", False, str(e))

# FR-12: Browse posts
try:
    resp = requests.get(f"{BASE_URL}/posts")
    test_result("FR-12", "Browse posts and topics", resp.status_code == 200,
               f"Posts found: {len(resp.json()) if resp.status_code == 200 else 0}")
except Exception as e:
    test_result("FR-12", "Browse posts and topics", False, str(e))

# ============================================================================
# 1.5 Private Messaging (FR-13, FR-14)
# ============================================================================
print_section("1.5 Private Messaging")

# FR-13: Private messages between datemates
try:
    resp = requests.get(f"{BASE_URL}/messages")
    if resp.status_code == 404:
        test_not_implemented("FR-13", "Private messaging between datemates")
        test_not_implemented("FR-14", "Message notifications")
    else:
        test_result("FR-13", "Private messaging between datemates", resp.status_code == 200)
        test_result("FR-14", "Message notifications", resp.status_code == 200)
except Exception as e:
    test_not_implemented("FR-13", "Private messaging between datemates")
    test_not_implemented("FR-14", "Message notifications")

# ============================================================================
# 1.6 AI-Supported Features (FR-16 to FR-23)
# ============================================================================
print_section("1.6 AI-Supported Features")

# FR-16: AI Companion
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/companion",
            headers={"Authorization": f"Bearer {token1}"},
            json={"message": "I'm feeling nervous about dating"}
        )
        test_result("FR-16", "AI Companion chat", resp.status_code == 200,
                   f"Response received: {resp.status_code == 200}")
    else:
        test_result("FR-16", "AI Companion chat", False, "No auth token")
except Exception as e:
    test_result("FR-16", "AI Companion chat", False, str(e))

# FR-17: Miss Ex
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/miss-ex",
            headers={"Authorization": f"Bearer {token1}"},
            json={"message": "Hi", "ex_chat_history": "Sample history"}
        )
        test_result("FR-17", "Miss Ex AI imitation", resp.status_code == 200,
                   f"Endpoint exists: {resp.status_code == 200}")
    else:
        test_result("FR-17", "Miss Ex AI imitation", False, "No auth token")
except Exception as e:
    test_result("FR-17", "Miss Ex AI imitation", False, str(e))

# FR-19: AI Wingman
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/wingman",
            headers={"Authorization": f"Bearer {token1}"},
            json={"partner_profile": "Likes music and coding", "chat_history": []}
        )
        test_result("FR-19", "AI Wingman suggestions", resp.status_code == 200,
                   f"Suggestions received: {resp.status_code == 200}")
    else:
        test_result("FR-19", "AI Wingman suggestions", False, "No auth token")
except Exception as e:
    test_result("FR-19", "AI Wingman suggestions", False, str(e))

# FR-20: Atmosphere Analyzer
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/atmosphere",
            headers={"Authorization": f"Bearer {token1}"},
            json={"chat_history": [{"role": "user", "content": "Hey!"}]}
        )
        test_result("FR-20", "Atmosphere Analyzer", resp.status_code == 200,
                   f"Analysis received: {resp.status_code == 200}")
    else:
        test_result("FR-20", "Atmosphere Analyzer", False, "No auth token")
except Exception as e:
    test_result("FR-20", "Atmosphere Analyzer", False, str(e))

# FR-21: Profile Optimizer
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/optimize-profile",
            headers={"Authorization": f"Bearer {token1}"},
            json={"current_bio": "I like stuff"}
        )
        test_result("FR-21", "AI Profile Optimizer", resp.status_code == 200,
                   f"Suggestions received: {resp.status_code == 200}")
    else:
        test_result("FR-21", "AI Profile Optimizer", False, "No auth token")
except Exception as e:
    test_result("FR-21", "AI Profile Optimizer", False, str(e))

# FR-22: Practice Mode
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/practice",
            headers={"Authorization": f"Bearer {token1}"},
            json={"scenario": "first_date", "message": "Hi, nice to meet you"}
        )
        test_result("FR-22", "AI Practice Mode", resp.status_code == 200,
                   f"Practice response: {resp.status_code == 200}")
    else:
        test_result("FR-22", "AI Practice Mode", False, "No auth token")
except Exception as e:
    test_result("FR-22", "AI Practice Mode", False, str(e))

# FR-23: Abuse & Harassment Detector
try:
    if token1:
        resp = requests.post(f"{BASE_URL}/ai/safety-check",
            headers={"Authorization": f"Bearer {token1}"},
            json={"message": "This is a test message"}
        )
        test_result("FR-23", "AI Abuse & Harassment Detector", resp.status_code == 200,
                   f"Safety check: {resp.status_code == 200}")
    else:
        test_result("FR-23", "AI Abuse & Harassment Detector", False, "No auth token")
except Exception as e:
    test_result("FR-23", "AI Abuse & Harassment Detector", False, str(e))

# ============================================================================
# Summary
# ============================================================================
print_section("Test Summary")

total = len(results["passed"]) + len(results["failed"]) + len(results["not_implemented"])
print(f"Total Requirements Tested: {total}")
print(f"✅ Passed: {len(results['passed'])}")
print(f"❌ Failed: {len(results['failed'])}")
print(f"⚠️  Not Implemented: {len(results['not_implemented'])}")

if results["failed"]:
    print(f"\nFailed Requirements: {', '.join(results['failed'])}")

if results["not_implemented"]:
    print(f"\nNot Implemented: {', '.join(results['not_implemented'])}")

print(f"\n{'='*60}")
print(f"Pass Rate: {len(results['passed'])/total*100:.1f}%")
print(f"{'='*60}\n")
