#!/usr/bin/env python3
"""
Detailed debug of mood history endpoint
"""

import requests
import json
import time

def debug_mood_history_detailed():
    """Debug mood history endpoint with detailed logging."""
    base_url = "http://localhost:8000"
    
    print("🔍 Detailed mood history debug...")
    
    # Step 1: Create a test user
    unique_id = str(int(time.time()))
    test_user = {
        "username": f"debugmood{unique_id}",
        "email": f"debugmood{unique_id}@example.com",
        "password": "testpass123",
        "full_name": "Debug Mood User"
    }
    
    print("1. Creating test user...")
    register_response = requests.post(f"{base_url}/auth/register", 
                                    json=test_user, 
                                    headers={"Content-Type": "application/json"},
                                    timeout=10)
    
    if register_response.status_code not in [200, 201]:
        print(f"❌ Registration failed: {register_response.status_code}")
        print(f"Response: {register_response.text}")
        return
    
    print("✅ User created successfully")
    
    # Step 2: Login to get token
    print("2. Logging in...")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    login_response = requests.post(f"{base_url}/auth/login",
                                 json=login_data,
                                 headers={"Content-Type": "application/json"},
                                 timeout=10)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token_data = login_response.json()
    token = token_data["access_token"]
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # Step 3: Add a test mood entry first
    print("3. Adding a test mood entry...")
    mood_data = {
        "user_id": test_user["username"],
        "mood": "happy",
        "note": "Test mood entry"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    mood_log_response = requests.post(f"{base_url}/moods/", 
                                    json=mood_data,
                                    headers=headers, 
                                    timeout=10)
    
    print(f"Mood log status: {mood_log_response.status_code}")
    if mood_log_response.status_code == 200:
        print("✅ Mood entry added successfully")
    else:
        print(f"❌ Mood entry failed: {mood_log_response.text}")
    
    # Step 4: Test mood history endpoint
    print("4. Testing mood history endpoint...")
    
    mood_response = requests.get(f"{base_url}/moods/{test_user['username']}", 
                               headers=headers, 
                               timeout=10)
    
    print(f"Status Code: {mood_response.status_code}")
    print(f"Headers: {dict(mood_response.headers)}")
    
    if mood_response.status_code == 200:
        try:
            response_data = mood_response.json()
            print(f"✅ Mood history endpoint working!")
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except Exception as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Raw response: {mood_response.text}")
    else:
        print(f"❌ Mood history endpoint failed: {mood_response.status_code}")
        try:
            error_data = mood_response.json()
            print(f"Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw response: {mood_response.text}")

if __name__ == "__main__":
    debug_mood_history_detailed()
