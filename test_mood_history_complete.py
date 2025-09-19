#!/usr/bin/env python3
"""
Complete test of mood history functionality
"""

import requests
import json
import time

def test_mood_history_complete():
    """Test complete mood history flow with authentication."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing complete mood history functionality...")
    
    # Step 1: Register a test user
    unique_id = str(int(time.time()))
    test_user = {
        "username": f"moodtest{unique_id}",
        "email": f"moodtest{unique_id}@example.com",
        "password": "testpass123",
        "full_name": "Mood Test User"
    }
    
    print("1. Registering test user...")
    register_response = requests.post(f"{base_url}/auth/register", 
                                    json=test_user, 
                                    headers={"Content-Type": "application/json"},
                                    timeout=10)
    
    if register_response.status_code != 200:
        print(f"❌ Registration failed: {register_response.status_code}")
        print(f"Response: {register_response.text}")
        return False
    
    print("✅ User registration successful")
    
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
        return False
    
    token_data = login_response.json()
    token = token_data["access_token"]
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # Step 3: Test mood history endpoint (should be empty initially)
    print("3. Testing mood history endpoint (empty)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    mood_history_response = requests.get(f"{base_url}/moods/{test_user['username']}", 
                                       headers=headers, 
                                       timeout=10)
    
    print(f"Mood history status: {mood_history_response.status_code}")
    if mood_history_response.status_code == 200:
        mood_data = mood_history_response.json()
        print(f"✅ Mood history endpoint working! Found {mood_data['count']} entries")
        print(f"Response: {json.dumps(mood_data, indent=2)}")
    else:
        print(f"❌ Mood history failed: {mood_history_response.text}")
        return False
    
    # Step 4: Add a test mood entry
    print("4. Adding test mood entry...")
    mood_entry = {
        "user_id": test_user["username"],
        "mood": "happy",
        "note": "Test mood entry for debugging"
    }
    
    mood_log_response = requests.post(f"{base_url}/moods/", 
                                    json=mood_entry,
                                    headers=headers, 
                                    timeout=10)
    
    print(f"Mood log status: {mood_log_response.status_code}")
    if mood_log_response.status_code == 200:
        print("✅ Mood entry added successfully")
    else:
        print(f"❌ Mood entry failed: {mood_log_response.text}")
        return False
    
    # Step 5: Test mood history again (should now have 1 entry)
    print("5. Testing mood history endpoint (with data)...")
    mood_history_response2 = requests.get(f"{base_url}/moods/{test_user['username']}", 
                                        headers=headers, 
                                        timeout=10)
    
    print(f"Mood history status: {mood_history_response2.status_code}")
    if mood_history_response2.status_code == 200:
        mood_data2 = mood_history_response2.json()
        print(f"✅ Mood history with data working! Found {mood_data2['count']} entries")
        print(f"Response: {json.dumps(mood_data2, indent=2)}")
        return True
    else:
        print(f"❌ Mood history with data failed: {mood_history_response2.text}")
        return False

if __name__ == "__main__":
    success = test_mood_history_complete()
    if success:
        print("\n🎉 All mood history tests passed!")
    else:
        print("\n❌ Some tests failed.")
