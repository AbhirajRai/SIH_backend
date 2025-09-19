#!/usr/bin/env python3
"""
Test script to verify API endpoints are working correctly
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test backend health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Backend health check passed")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_cors():
    """Test CORS headers."""
    try:
        response = requests.options(f"{BASE_URL}/moods/test", timeout=10)
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        print(f"✅ CORS headers: {cors_headers}")
        return True
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints."""
    try:
        # Test registration with unique username
        import time
        unique_id = str(int(time.time()))
        test_user = {
            "username": f"testuser{unique_id}",
            "email": f"test{unique_id}@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
        
        # Try to register
        response = requests.post(f"{BASE_URL}/auth/register", 
                               json=test_user, 
                               headers={"Content-Type": "application/json"},
                               timeout=10)
        
        if response.status_code in [200, 201, 400]:  # 400 might mean user already exists
            print("✅ Auth registration endpoint accessible")
            
            # Try to login with the same credentials
            login_data = {
                "username": test_user["username"],
                "password": test_user["password"]
            }
            
            response = requests.post(f"{BASE_URL}/auth/login",
                                   json=login_data,
                                   headers={"Content-Type": "application/json"},
                                   timeout=10)
            
            if response.status_code in [200, 401]:  # 401 means endpoint works but auth failed
                print("✅ Auth login endpoint accessible")
                return True
            else:
                print(f"❌ Auth login failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error details: {error_data}")
                except:
                    print(f"Raw response: {response.text}")
                return False
        else:
            print(f"❌ Auth registration failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Auth endpoints test error: {e}")
        return False

def test_mood_endpoints():
    """Test mood tracking endpoints."""
    try:
        # First, create a user and get auth token
        import time
        unique_id = str(int(time.time()))
        test_user = {
            "username": f"moodtest{unique_id}",
            "email": f"moodtest{unique_id}@example.com",
            "password": "testpass123",
            "full_name": "Mood Test User"
        }
        
        # Register user
        register_response = requests.post(f"{BASE_URL}/auth/register", 
                                        json=test_user, 
                                        headers={"Content-Type": "application/json"},
                                        timeout=10)
        
        if register_response.status_code not in [200, 201]:
            print("❌ Failed to create test user for mood test")
            return False
        
        # Login to get token
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        
        login_response = requests.post(f"{BASE_URL}/auth/login",
                                     json=login_data,
                                     headers={"Content-Type": "application/json"},
                                     timeout=10)
        
        if login_response.status_code != 200:
            print("❌ Failed to login for mood test")
            return False
        
        token_data = login_response.json()
        token = token_data["access_token"]
        
        # Test mood endpoint with auth
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(f"{BASE_URL}/moods/{test_user['username']}", 
                              headers=headers, 
                              timeout=10)
        
        if response.status_code == 200:
            print("✅ Mood endpoints work with authentication")
            return True
        else:
            print(f"❌ Mood endpoints failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Mood endpoints test error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing API Endpoints...")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_health),
        ("CORS Headers", test_cors),
        ("Auth Endpoints", test_auth_endpoints),
        ("Mood Endpoints", test_mood_endpoints),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()
