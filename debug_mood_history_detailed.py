#!/usr/bin/env python3
"""
Detailed debugging of mood history endpoint
"""

import requests
import json
import time

def debug_mood_history_detailed():
    """Debug mood history with detailed logging."""
    base_url = "http://127.0.0.1:8000"  # Same as frontend
    
    print("🔍 Detailed Mood History Debug")
    print("=" * 50)
    
    # Step 1: Test server health
    print("1. Testing server health...")
    try:
        health_response = requests.get(f"{base_url}/", timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return
    
    # Step 2: Create test user
    print("\n2. Creating test user...")
    unique_id = str(int(time.time()))
    test_user = {
        "username": f"debuguser{unique_id}",
        "email": f"debug{unique_id}@example.com",
        "password": "testpass123",
        "full_name": "Debug User"
    }
    
    try:
        register_response = requests.post(f"{base_url}/auth/register", 
                                        json=test_user, 
                                        headers={"Content-Type": "application/json"},
                                        timeout=10)
        
        if register_response.status_code == 200:
            print("✅ User registration successful")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(f"Response: {register_response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Step 3: Login to get token
    print("\n3. Logging in...")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    try:
        login_response = requests.post(f"{base_url}/auth/login",
                                     json=login_data,
                                     headers={"Content-Type": "application/json"},
                                     timeout=10)
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data["access_token"]
            print(f"✅ Login successful, token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 4: Test mood history endpoint (should be empty)
    print("\n4. Testing mood history endpoint (empty)...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        mood_history_response = requests.get(f"{base_url}/moods/{test_user['username']}", 
                                           headers=headers, 
                                           timeout=10)
        
        print(f"Status Code: {mood_history_response.status_code}")
        print(f"Headers: {dict(mood_history_response.headers)}")
        
        if mood_history_response.status_code == 200:
            mood_data = mood_history_response.json()
            print(f"✅ Mood history successful! Found {mood_data['count']} entries")
            print(f"Response: {json.dumps(mood_data, indent=2)}")
        else:
            print(f"❌ Mood history failed: {mood_history_response.status_code}")
            try:
                error_data = mood_history_response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {mood_history_response.text}")
    except Exception as e:
        print(f"❌ Mood history request error: {e}")
        return
    
    # Step 5: Add a mood entry
    print("\n5. Adding test mood entry...")
    mood_entry = {
        "user_id": test_user["username"],
        "mood": "happy",
        "note": "Test mood for debugging"
    }
    
    try:
        mood_log_response = requests.post(f"{base_url}/moods/", 
                                        json=mood_entry,
                                        headers=headers, 
                                        timeout=10)
        
        print(f"Mood log status: {mood_log_response.status_code}")
        if mood_log_response.status_code == 200:
            print("✅ Mood entry added successfully")
        else:
            print(f"❌ Mood entry failed: {mood_log_response.status_code}")
            try:
                error_data = mood_log_response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {mood_log_response.text}")
    except Exception as e:
        print(f"❌ Mood entry error: {e}")
        return
    
    # Step 6: Test mood history again (should have 1 entry)
    print("\n6. Testing mood history with data...")
    try:
        mood_history_response2 = requests.get(f"{base_url}/moods/{test_user['username']}", 
                                            headers=headers, 
                                            timeout=10)
        
        print(f"Status Code: {mood_history_response2.status_code}")
        if mood_history_response2.status_code == 200:
            mood_data2 = mood_history_response2.json()
            print(f"✅ Mood history with data successful! Found {mood_data2['count']} entries")
            print(f"Response: {json.dumps(mood_data2, indent=2)}")
        else:
            print(f"❌ Mood history with data failed: {mood_history_response2.status_code}")
            try:
                error_data = mood_history_response2.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {mood_history_response2.text}")
    except Exception as e:
        print(f"❌ Mood history with data error: {e}")

if __name__ == "__main__":
    debug_mood_history_detailed()
