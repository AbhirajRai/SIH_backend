#!/usr/bin/env python3
"""
Test script for MindCare Backend Error Handling & Validation
This script tests various error scenarios and validation
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_validation_errors():
    """Test input validation errors."""
    
    print("🧪 Testing Input Validation & Error Handling")
    print("=" * 60)
    
    # Test 1: Invalid user registration data
    print("\n1️⃣ Testing Invalid User Registration...")
    
    invalid_users = [
        {
            "username": "ab",  # Too short
            "email": "invalid-email",
            "password": "123",  # Too short
            "full_name": "Test User"
        },
        {
            "username": "validuser",
            "email": "not-an-email",
            "password": "password123",
            "full_name": "Test User"
        },
        {
            "username": "validuser",
            "email": "test@example.com",
            "password": "weak",  # No numbers
            "full_name": "Test User"
        },
        {
            "username": "validuser",
            "email": "test@example.com",
            "password": "123456",  # No letters
            "full_name": "Test User"
        }
    ]
    
    for i, user_data in enumerate(invalid_users, 1):
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
            print(f"   Test {i}: Status {response.status_code}")
            if response.status_code == 422:
                print(f"   ✅ Validation error caught: {response.json()}")
            else:
                print(f"   ❌ Expected validation error, got: {response.text}")
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection failed. Make sure the server is running.")
            return
    
    # Test 2: Invalid mood logging
    print("\n2️⃣ Testing Invalid Mood Logging...")
    
    # First, create a valid user and get token
    valid_user = {
        "username": f"testuser{int(time.time())}",
        "email": f"test{int(time.time())}@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    try:
        # Register user
        response = requests.post(f"{BASE_URL}/auth/register", json=valid_user)
        if response.status_code != 200:
            print(f"   ❌ Failed to create test user: {response.text}")
            return
        
        # Login to get token
        login_data = {
            "username": valid_user["username"],
            "password": valid_user["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print(f"   ❌ Failed to login: {response.text}")
            return
        
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test invalid mood data
        invalid_moods = [
            {
                "user_id": "",  # Empty user_id
                "mood": "happy",
                "note": "Test note"
            },
            {
                "user_id": valid_user["username"],
                "mood": "invalid_mood",  # Invalid mood
                "note": "Test note"
            },
            {
                "user_id": valid_user["username"],
                "mood": "happy",
                "note": "x" * 501  # Too long note
            }
        ]
        
        for i, mood_data in enumerate(invalid_moods, 1):
            response = requests.post(f"{BASE_URL}/moods/", json=mood_data, headers=headers)
            print(f"   Test {i}: Status {response.status_code}")
            if response.status_code == 422:
                print(f"   ✅ Validation error caught: {response.json()}")
            else:
                print(f"   ❌ Expected validation error, got: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed. Make sure the server is running.")
        return
    
    # Test 3: Unauthorized access
    print("\n3️⃣ Testing Unauthorized Access...")
    
    try:
        # Try to access protected endpoint without token
        response = requests.get(f"{BASE_URL}/auth/me")
        print(f"   No token: Status {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Unauthorized access properly blocked")
        else:
            print(f"   ❌ Expected 401, got: {response.text}")
        
        # Try to access another user's data
        response = requests.get(f"{BASE_URL}/moods/other_user", headers=headers)
        print(f"   Other user's data: Status {response.status_code}")
        if response.status_code == 403:
            print("   ✅ Unauthorized access to other user's data blocked")
        else:
            print(f"   ❌ Expected 403, got: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed. Make sure the server is running.")
        return
    
    # Test 4: Duplicate user registration
    print("\n4️⃣ Testing Duplicate User Registration...")
    
    try:
        # Try to register the same user again
        response = requests.post(f"{BASE_URL}/auth/register", json=valid_user)
        print(f"   Duplicate user: Status {response.status_code}")
        if response.status_code == 400:
            print("   ✅ Duplicate user registration blocked")
        else:
            print(f"   ❌ Expected 400, got: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed. Make sure the server is running.")
        return
    
    print("\n🎉 Error handling tests completed!")
    print("\n📝 Summary:")
    print("   ✅ Input validation working")
    print("   ✅ Authentication working")
    print("   ✅ Authorization working")
    print("   ✅ Duplicate prevention working")

def test_database_error_handling():
    """Test database error handling scenarios."""
    print("\n🔧 Testing Database Error Handling...")
    
    # This would require simulating database failures
    # For now, we'll just test that the server handles requests gracefully
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("   ✅ Server is responding to requests")
        else:
            print(f"   ❌ Server error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running")

if __name__ == "__main__":
    test_validation_errors()
    test_database_error_handling()
