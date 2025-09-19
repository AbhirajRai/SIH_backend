#!/usr/bin/env python3
"""
Comprehensive Test Suite for SIH Backend - MindCare Mental Health API
Tests all major components and functionality
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": f"testuser_{int(time.time())}",
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "TestPassword123",
    "full_name": "Test User"
}

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name, passed, details=""):
        self.tests.append({"name": name, "passed": passed, "details": details})
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"🧪 COMPREHENSIVE TEST RESULTS")
        print(f"{'='*60}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Total: {self.passed + self.failed}")
        print(f"🎯 Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        
        if self.failed > 0:
            print(f"\n❌ Failed Tests:")
            for test in self.tests:
                if not test["passed"]:
                    print(f"   - {test['name']}: {test['details']}")
        
        print(f"\n{'='*60}")

def test_server_health():
    """Test if the server is running and healthy"""
    print("🏥 Testing Server Health...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            return True, f"Server is running: {data.get('message', 'OK')}"
        else:
            return False, f"Server returned status {response.status_code}"
    except Exception as e:
        return False, f"Server connection failed: {str(e)}"

def test_nlp_health():
    """Test NLP services health"""
    print("🧠 Testing NLP Services Health...")
    try:
        response = requests.get(f"{BASE_URL}/nlp/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                return True, "NLP services are healthy"
            else:
                return False, f"NLP services unhealthy: {data}"
        else:
            return False, f"NLP health check failed: {response.status_code}"
    except Exception as e:
        return False, f"NLP health check error: {str(e)}"

def test_user_registration():
    """Test user registration"""
    print("👤 Testing User Registration...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=TEST_USER)
        if response.status_code == 200:
            data = response.json()
            return True, f"User registered: {data.get('username')}"
        else:
            return False, f"Registration failed: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def test_user_login():
    """Test user login and get JWT token"""
    print("🔐 Testing User Login...")
    try:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                return True, f"Login successful, token received"
            else:
                return False, "Login successful but no token received"
        else:
            return False, f"Login failed: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def get_auth_token():
    """Get authentication token for protected endpoints"""
    try:
        login_data = {
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        return None
    except:
        return None

def test_protected_endpoint():
    """Test accessing protected endpoint"""
    print("🛡️ Testing Protected Endpoint...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Protected endpoint accessed: {data.get('username')}"
        else:
            return False, f"Protected endpoint failed: {response.status_code}"
    except Exception as e:
        return False, f"Protected endpoint error: {str(e)}"

def test_mood_logging():
    """Test mood logging functionality"""
    print("😊 Testing Mood Logging...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        mood_data = {
            "user_id": TEST_USER["username"],
            "mood": "happy",
            "note": "Feeling great after testing!"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/moods/", json=mood_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Mood logged: {data.get('message')}"
        else:
            return False, f"Mood logging failed: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Mood logging error: {str(e)}"

def test_mood_history():
    """Test mood history retrieval"""
    print("📊 Testing Mood History...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/moods/{TEST_USER['username']}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Mood history retrieved: {data.get('count', 0)} entries"
        else:
            return False, f"Mood history failed: {response.status_code}"
    except Exception as e:
        return False, f"Mood history error: {str(e)}"

def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("💭 Testing Sentiment Analysis...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        text_data = {"text": "I am feeling really happy and excited today!"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/sentiment", json=text_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Sentiment: {data.get('label')} (confidence: {data.get('confidence')})"
        else:
            return False, f"Sentiment analysis failed: {response.status_code}"
    except Exception as e:
        return False, f"Sentiment analysis error: {str(e)}"

def test_emotion_analysis():
    """Test emotion analysis"""
    print("😢 Testing Emotion Analysis...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        text_data = {"text": "I am feeling anxious about my job interview tomorrow"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/emotion", json=text_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Emotion: {data.get('label')} (confidence: {data.get('confidence')})"
        else:
            return False, f"Emotion analysis failed: {response.status_code}"
    except Exception as e:
        return False, f"Emotion analysis error: {str(e)}"

def test_toxicity_detection():
    """Test toxicity detection"""
    print("🚫 Testing Toxicity Detection...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        text_data = {"text": "You are a wonderful person and I appreciate you"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/toxicity", json=text_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Toxicity: {data.get('level')} (safe: {data.get('safe')})"
        else:
            return False, f"Toxicity detection failed: {response.status_code}"
    except Exception as e:
        return False, f"Toxicity detection error: {str(e)}"

def test_distress_detection():
    """Test distress detection"""
    print("🚨 Testing Distress Detection...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        text_data = {"text": "I am feeling overwhelmed and need help"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/distress", json=text_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Distress: urgent={data.get('is_urgent')} - {data.get('reason')}"
        else:
            return False, f"Distress detection failed: {response.status_code}"
    except Exception as e:
        return False, f"Distress detection error: {str(e)}"

def test_comprehensive_analysis():
    """Test comprehensive analysis"""
    print("🔍 Testing Comprehensive Analysis...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        text_data = {
            "text": "I am feeling really happy and excited about my new job!",
            "user_id": TEST_USER["username"]
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/analyze", json=text_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Comprehensive analysis completed for user: {data.get('user_id')}"
        else:
            return False, f"Comprehensive analysis failed: {response.status_code}"
    except Exception as e:
        return False, f"Comprehensive analysis error: {str(e)}"

def test_advanced_chatbot():
    """Test advanced chatbot"""
    print("🤖 Testing Advanced Chatbot...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        chat_data = {
            "user_id": TEST_USER["username"],
            "message": "Hello, I am feeling a bit stressed today"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/nlp/chatbot", json=chat_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Chatbot responded: {data.get('reply', '')[:50]}..."
        else:
            return False, f"Chatbot failed: {response.status_code}"
    except Exception as e:
        return False, f"Chatbot error: {str(e)}"

def test_basic_chatbot():
    """Test basic chatbot"""
    print("💬 Testing Basic Chatbot...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        chat_data = {
            "user_id": TEST_USER["username"],
            "message": "Hi there!"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/chatbot/", json=chat_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return True, f"Basic chatbot responded: {data.get('bot', '')[:50]}..."
        else:
            return False, f"Basic chatbot failed: {response.status_code}"
    except Exception as e:
        return False, f"Basic chatbot error: {str(e)}"

def test_gamification():
    """Test gamification features"""
    print("🎯 Testing Gamification...")
    try:
        token = get_auth_token()
        if not token:
            return False, "Could not get authentication token"
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test streak update
        response = requests.post(f"{BASE_URL}/gamify/streak/{TEST_USER['username']}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            streak = data.get('streak', 0)
            
            # Test streak retrieval
            response2 = requests.get(f"{BASE_URL}/gamify/streak/{TEST_USER['username']}", headers=headers)
            if response2.status_code == 200:
                data2 = response2.json()
                return True, f"Streak updated and retrieved: {data2.get('streak', 0)}"
            else:
                return False, f"Streak retrieval failed: {response2.status_code}"
        else:
            return False, f"Streak update failed: {response.status_code}"
    except Exception as e:
        return False, f"Gamification error: {str(e)}"

def test_api_documentation():
    """Test API documentation endpoints"""
    print("📚 Testing API Documentation...")
    try:
        # Test Swagger UI
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200 and "swagger" in response.text.lower():
            return True, "Swagger UI is accessible"
        else:
            return False, f"Swagger UI failed: {response.status_code}"
    except Exception as e:
        return False, f"API documentation error: {str(e)}"

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Test Suite for SIH Backend")
    print("=" * 60)
    
    results = TestResults()
    
    # Test functions
    tests = [
        ("Server Health", test_server_health),
        ("NLP Services Health", test_nlp_health),
        ("User Registration", test_user_registration),
        ("User Login", test_user_login),
        ("Protected Endpoint", test_protected_endpoint),
        ("Mood Logging", test_mood_logging),
        ("Mood History", test_mood_history),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Emotion Analysis", test_emotion_analysis),
        ("Toxicity Detection", test_toxicity_detection),
        ("Distress Detection", test_distress_detection),
        ("Comprehensive Analysis", test_comprehensive_analysis),
        ("Advanced Chatbot", test_advanced_chatbot),
        ("Basic Chatbot", test_basic_chatbot),
        ("Gamification", test_gamification),
        ("API Documentation", test_api_documentation),
    ]
    
    # Run all tests
    for test_name, test_func in tests:
        try:
            passed, details = test_func()
            results.add_test(test_name, passed, details)
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} {test_name}: {details}")
        except Exception as e:
            results.add_test(test_name, False, f"Test error: {str(e)}")
            print(f"❌ FAIL {test_name}: Test error: {str(e)}")
        
        time.sleep(0.5)  # Small delay between tests
    
    # Print summary
    results.print_summary()
    
    # Exit with appropriate code
    if results.failed > 0:
        print(f"\n⚠️ Some tests failed. Please check the server and try again.")
        sys.exit(1)
    else:
        print(f"\n🎉 All tests passed! The SIH Backend is working perfectly!")
        sys.exit(0)

if __name__ == "__main__":
    main()
