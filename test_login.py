#!/usr/bin/env python3
"""
Test login functionality
"""

import requests
import json
import time

def test_login():
    """Test login functionality with fallback database."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing login functionality...")
    
    # Step 1: Register a test user
    unique_id = str(int(time.time()))
    test_user = {
        "username": f"testuser{unique_id}",
        "email": f"test{unique_id}@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    print("1. Registering test user...")
    register_response = requests.post(f"{base_url}/auth/register", 
                                    json=test_user, 
                                    headers={"Content-Type": "application/json"},
                                    timeout=10)
    
    print(f"Registration status: {register_response.status_code}")
    if register_response.status_code == 200:
        print("✅ User registration successful")
    else:
        print(f"❌ Registration failed: {register_response.text}")
        return
    
    # Step 2: Test login
    print("2. Testing login...")
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    login_response = requests.post(f"{base_url}/auth/login",
                                 json=login_data,
                                 headers={"Content-Type": "application/json"},
                                 timeout=10)
    
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_result = login_response.json()
        print("✅ Login successful!")
        print(f"Token: {login_result.get('access_token', 'No token')[:20]}...")
        return True
    else:
        print(f"❌ Login failed: {login_response.text}")
        return False

if __name__ == "__main__":
    test_login()
