#!/usr/bin/env python3
"""
Test script for MindCare Backend Authentication System
Run this script to test the authentication endpoints
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_authentication():
    """Test the complete authentication flow."""
    
    print("🧪 Testing MindCare Backend Authentication System")
    print("=" * 50)
    
    # Test data
    import time
    timestamp = int(time.time())
    test_user = {
        "username": f"testuser{timestamp}",
        "email": f"testuser{timestamp}@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # 1. Test Registration
    print("\n1️⃣ Testing User Registration...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        if response.status_code == 200:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"   User ID: {user_data.get('id')}")
            print(f"   Username: {user_data.get('username')}")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return
    
    # 2. Test Login
    print("\n2️⃣ Testing User Login...")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login successful!")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   Token type: {token_data['token_type']}")
            print(f"   Access token: {access_token[:50]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return
    
    # 3. Test Protected Endpoint - Get Current User
    print("\n3️⃣ Testing Protected Endpoint (Get Current User)...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
            user_info = response.json()
            print(f"   Current user: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
        else:
            print(f"❌ Protected endpoint access failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return
    
    # 4. Test Mood Logging (Protected)
    print("\n4️⃣ Testing Mood Logging (Protected Endpoint)...")
    mood_data = {
        "user_id": test_user["username"],
        "mood": "happy",
        "note": "Feeling great after implementing auth!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/moods/", json=mood_data, headers=headers)
        if response.status_code == 200:
            print("✅ Mood logging successful!")
            mood_result = response.json()
            print(f"   Message: {mood_result['message']}")
        else:
            print(f"❌ Mood logging failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return
    
    # 5. Test Unauthorized Access
    print("\n5️⃣ Testing Unauthorized Access...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me")  # No token
        if response.status_code == 401:
            print("✅ Unauthorized access properly blocked!")
        else:
            print(f"❌ Unauthorized access not blocked: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
        return
    
    print("\n🎉 All authentication tests completed!")
    print("\n📝 Next steps:")
    print("   1. Visit http://localhost:8000/docs to see the API documentation")
    print("   2. Try the authentication endpoints in the Swagger UI")
    print("   3. Test the protected endpoints with your JWT token")

if __name__ == "__main__":
    test_authentication()
