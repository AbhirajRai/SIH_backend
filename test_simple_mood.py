#!/usr/bin/env python3
"""
Simple test to isolate mood endpoint issues
"""

import requests
import json

def test_simple_mood():
    """Test mood endpoints with minimal setup."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing simple mood endpoints...")
    
    # Test 1: Check if server is running
    print("1. Testing server health...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return
    
    # Test 2: Check if mood endpoint exists (without auth)
    print("2. Testing mood endpoint without auth...")
    try:
        response = requests.get(f"{base_url}/moods/test", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Mood endpoint exists (requires auth)")
        else:
            print(f"Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Mood endpoint test failed: {e}")
    
    # Test 3: Check if mood endpoint exists (POST without auth)
    print("3. Testing mood POST endpoint without auth...")
    try:
        mood_data = {
            "user_id": "test",
            "mood": "happy",
            "note": "test"
        }
        response = requests.post(f"{base_url}/moods/", 
                               json=mood_data,
                               headers={"Content-Type": "application/json"},
                               timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Mood POST endpoint exists (requires auth)")
        else:
            print(f"Unexpected status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
    except Exception as e:
        print(f"❌ Mood POST endpoint test failed: {e}")

if __name__ == "__main__":
    test_simple_mood()
