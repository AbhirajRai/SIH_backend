#!/usr/bin/env python3
"""
Gamification Backend Test Script
Tests all gamification endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "test_gamification_user",
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
}

class GamificationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        self.test_results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "details": []
        }

    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")

    def record_test(self, test_name, passed, details=""):
        self.test_results["total"] += 1
        if passed:
            self.test_results["passed"] += 1
            self.log(f"✅ {test_name}", "PASS")
        else:
            self.test_results["failed"] += 1
            self.log(f"❌ {test_name}: {details}", "FAIL")
        
        self.test_results["details"].append({
            "test": test_name,
            "passed": passed,
            "details": details
        })

    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to backend. Make sure it's running on localhost:8000")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")

    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = self.make_request("GET", "/")
            if response.status_code == 200 and "running" in response.json().get("message", ""):
                self.record_test("Backend Health Check", True)
                return True
            else:
                self.record_test("Backend Health Check", False, "Unexpected response")
                return False
        except Exception as e:
            self.record_test("Backend Health Check", False, str(e))
            return False

    def test_user_registration(self):
        """Test user registration"""
        try:
            response = self.make_request("POST", "/auth/register", data=TEST_USER)
            if response.status_code == 200:
                self.record_test("User Registration", True)
                return True
            else:
                self.record_test("User Registration", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.record_test("User Registration", False, str(e))
            return False

    def test_user_login(self):
        """Test user login and get token"""
        try:
            login_data = {
                "username": TEST_USER["username"],
                "password": TEST_USER["password"]
            }
            response = self.make_request("POST", "/auth/login", data=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.user_id = TEST_USER["username"]
                self.record_test("User Login", True)
                return True
            else:
                self.record_test("User Login", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.record_test("User Login", False, str(e))
            return False

    def test_xp_system(self):
        """Test XP addition and retrieval"""
        if not self.token:
            self.record_test("XP System", False, "No authentication token")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Test adding XP
            xp_data = {
                "action": "test_action",
                "xp_amount": 25,
                "description": "Test XP addition"
            }
            response = self.make_request("POST", f"/gamify/xp/add/{self.user_id}", 
                                      data=xp_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("xp_added") == 25:
                    self.record_test("XP Addition", True)
                else:
                    self.record_test("XP Addition", False, "XP not added correctly")
                    return False
            else:
                self.record_test("XP Addition", False, f"Status: {response.status_code}")
                return False

            # Test getting progress
            response = self.make_request("GET", f"/gamify/progress/{self.user_id}", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("xp", 0) >= 25:
                    self.record_test("Progress Retrieval", True)
                    return True
                else:
                    self.record_test("Progress Retrieval", False, "Progress not updated")
                    return False
            else:
                self.record_test("Progress Retrieval", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.record_test("XP System", False, str(e))
            return False

    def test_achievements(self):
        """Test achievement system"""
        if not self.token:
            self.record_test("Achievements", False, "No authentication token")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Test getting achievements
            response = self.make_request("GET", f"/gamify/achievements/{self.user_id}", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "achievements" in data and "total_achievements" in data:
                    self.record_test("Get Achievements", True)
                else:
                    self.record_test("Get Achievements", False, "Invalid response format")
                    return False
            else:
                self.record_test("Get Achievements", False, f"Status: {response.status_code}")
                return False

            # Test checking achievements
            response = self.make_request("POST", f"/gamify/achievements/check/{self.user_id}", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "new_achievements" in data:
                    self.record_test("Check Achievements", True)
                    return True
                else:
                    self.record_test("Check Achievements", False, "Invalid response format")
                    return False
            else:
                self.record_test("Check Achievements", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.record_test("Achievements", False, str(e))
            return False

    def test_streak_system(self):
        """Test streak system"""
        if not self.token:
            self.record_test("Streak System", False, "No authentication token")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Test updating streak
            response = self.make_request("POST", f"/gamify/streak/{self.user_id}", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "streak" in data:
                    self.record_test("Update Streak", True)
                else:
                    self.record_test("Update Streak", False, "Invalid response format")
                    return False
            else:
                self.record_test("Update Streak", False, f"Status: {response.status_code}")
                return False

            # Test getting streak
            response = self.make_request("GET", f"/gamify/streak/{self.user_id}", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "streak" in data:
                    self.record_test("Get Streak", True)
                    return True
                else:
                    self.record_test("Get Streak", False, "Invalid response format")
                    return False
            else:
                self.record_test("Get Streak", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.record_test("Streak System", False, str(e))
            return False

    def test_mood_tracking(self):
        """Test mood tracking integration"""
        if not self.token:
            self.record_test("Mood Tracking", False, "No authentication token")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Test logging a mood
            mood_data = {
                "user_id": self.user_id,
                "mood": "happy",
                "note": "Test mood for gamification"
            }
            response = self.make_request("POST", "/moods/", data=mood_data, headers=headers)
            
            if response.status_code == 200:
                self.record_test("Mood Logging", True)
            else:
                self.record_test("Mood Logging", False, f"Status: {response.status_code}")
                return False

            # Test getting mood history
            response = self.make_request("GET", f"/moods/{self.user_id}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.record_test("Mood History", True)
                    return True
                else:
                    self.record_test("Mood History", False, "Invalid response format")
                    return False
            else:
                self.record_test("Mood History", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.record_test("Mood Tracking", False, str(e))
            return False

    def test_ai_chat(self):
        """Test AI chat integration"""
        if not self.token:
            self.record_test("AI Chat", False, "No authentication token")
            return False

        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            # Test AI chat
            chat_data = {
                "user_id": self.user_id,
                "message": "Hello, this is a test message for gamification"
            }
            response = self.make_request("POST", "/nlp/chatbot", data=chat_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "reply" in data:
                    self.record_test("AI Chat", True)
                    return True
                else:
                    self.record_test("AI Chat", False, "Invalid response format")
                    return False
            else:
                self.record_test("AI Chat", False, f"Status: {response.status_code}")
                return False

        except Exception as e:
            self.record_test("AI Chat", False, str(e))
            return False

    def run_all_tests(self):
        """Run all gamification tests"""
        self.log("🚀 Starting Gamification Backend Test Suite", "INFO")
        self.log("=" * 50, "INFO")
        
        # Run tests in sequence
        self.test_backend_health()
        self.test_user_registration()
        self.test_user_login()
        self.test_xp_system()
        self.test_achievements()
        self.test_streak_system()
        self.test_mood_tracking()
        self.test_ai_chat()
        
        # Print results
        self.log("=" * 50, "INFO")
        self.log(f"🏁 Test Suite Completed!", "INFO")
        self.log(f"Total Tests: {self.test_results['total']}", "INFO")
        self.log(f"Passed: {self.test_results['passed']}", "INFO")
        self.log(f"Failed: {self.test_results['failed']}", "INFO")
        self.log(f"Success Rate: {(self.test_results['passed']/self.test_results['total']*100):.1f}%", "INFO")
        
        return self.test_results

if __name__ == "__main__":
    tester = GamificationTester()
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    if results['failed'] > 0:
        exit(1)
    else:
        exit(0)
