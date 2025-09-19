#!/usr/bin/env python3
"""
Debug mood endpoint issues
"""

import requests
import json
import time

def debug_mood_endpoint():
    """Debug mood endpoint with proper authentication."""
    base_url = "http://localhost:8000"
    
    # Create a test user
    unique_id = str(int(time.time()))
    test_user = {
        "username": f"debugmood{unique_id}",
        "email": f"debugmood{unique_id}@example.com",
        "password": "testpass123",
        "full_name": "Debug Mood User"
    }
    
    print("🔍 Creating test user...")
    
    # Register user
    register_response = requests.post(f"{base_url}/auth/register", 
                                    json=test_user, 
                                    headers={"Content-Type": "application/json"},
                                    timeout=10)
    
    if register_response.status_code not in [200, 201]:
        print(f"❌ Registration failed: {register_response.status_code}")
        print(f"Response: {register_response.text}")
        return
    
    print("✅ User created successfully")
    
    # Login to get token
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    print("🔍 Logging in...")
    
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
    
    # Test mood endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"🔍 Testing mood endpoint for user: {test_user['username']}")
    
    mood_response = requests.get(f"{base_url}/moods/{test_user['username']}", 
                               headers=headers, 
                               timeout=10)
    
    print(f"Status Code: {mood_response.status_code}")
    print(f"Headers: {dict(mood_response.headers)}")
    
    try:
        response_data = mood_response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
    except:
        print(f"Raw Response: {mood_response.text}")

if __name__ == "__main__":
    debug_mood_endpoint()
