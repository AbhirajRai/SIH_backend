#!/usr/bin/env python3
"""
Debug authentication issues
"""

import requests
import json

def test_auth_debug():
    """Debug authentication registration."""
    base_url = "http://localhost:8000"
    
    # Test data
    test_user = {
        "username": "debuguser123",
        "email": "debug@example.com",
        "password": "testpass123",
        "full_name": "Debug User"
    }
    
    print("🔍 Testing auth registration...")
    print(f"Data: {json.dumps(test_user, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth_debug()
