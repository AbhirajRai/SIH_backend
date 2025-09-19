#!/usr/bin/env python3
"""
SIH Backend Test Script
Tests all major backend functionality
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.main import app
    from app.database import test_connection, init_database
    from app.auth import get_password_hash, create_access_token
    from app.nlp_services import analyze_sentiment, analyze_emotion, analyze_distress
    from app.models import UserCreate, MoodLog
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class BackendTester:
    def __init__(self):
        self.test_results = []
        self.test_user = None
        self.test_token = None

    def log_test(self, test_name, status, message, details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status_icon = "✅" if status == "PASSED" else "❌"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            print(f"   Details: {details}")

    async def test_database_connection(self):
        """Test database connectivity"""
        try:
            if test_connection():
                self.log_test("Database Connection", "PASSED", "MongoDB connection successful")
                return True
            else:
                self.log_test("Database Connection", "FAILED", "MongoDB connection failed")
                return False
        except Exception as e:
            self.log_test("Database Connection", "FAILED", f"Database error: {str(e)}")
            return False

    async def test_database_initialization(self):
        """Test database initialization"""
        try:
            if init_database():
                self.log_test("Database Initialization", "PASSED", "Database collections initialized")
                return True
            else:
                self.log_test("Database Initialization", "FAILED", "Database initialization failed")
                return False
        except Exception as e:
            self.log_test("Database Initialization", "FAILED", f"Initialization error: {str(e)}")
            return False

    async def test_nlp_models(self):
        """Test NLP model loading and functionality"""
        try:
            # Test sentiment analysis
            sentiment_result = analyze_sentiment("I am feeling great today!")
            if sentiment_result and 'label' in sentiment_result:
                self.log_test("Sentiment Analysis", "PASSED", f"Sentiment detected: {sentiment_result['label']}")
            else:
                self.log_test("Sentiment Analysis", "FAILED", "Sentiment analysis returned invalid result")
                return False

            # Test emotion analysis
            emotion_result = analyze_emotion("I am feeling anxious about my exams")
            if emotion_result and 'label' in emotion_result:
                self.log_test("Emotion Detection", "PASSED", f"Emotion detected: {emotion_result['label']}")
            else:
                self.log_test("Emotion Detection", "FAILED", "Emotion analysis returned invalid result")
                return False

            # Test distress detection
            distress_result = analyze_distress("I want to hurt myself")
            if distress_result and 'is_urgent' in distress_result:
                self.log_test("Distress Detection", "PASSED", f"Distress detection working: urgent={distress_result['is_urgent']}")
            else:
                self.log_test("Distress Detection", "FAILED", "Distress detection returned invalid result")
                return False

            return True
        except Exception as e:
            self.log_test("NLP Models", "FAILED", f"NLP error: {str(e)}")
            return False

    async def test_authentication(self):
        """Test authentication functionality"""
        try:
            # Test password hashing
            test_password = "TestPassword123!"
            hashed = get_password_hash(test_password)
            if hashed and len(hashed) > 20:
                self.log_test("Password Hashing", "PASSED", "Password hashing working")
            else:
                self.log_test("Password Hashing", "FAILED", "Password hashing failed")
                return False

            # Test JWT token creation
            test_username = "test_user"
            token = create_access_token(data={"sub": test_username})
            if token and len(token) > 50:
                self.log_test("JWT Token Creation", "PASSED", "JWT token creation working")
                self.test_token = token
            else:
                self.log_test("JWT Token Creation", "FAILED", "JWT token creation failed")
                return False

            return True
        except Exception as e:
            self.log_test("Authentication", "FAILED", f"Authentication error: {str(e)}")
            return False

    async def test_data_models(self):
        """Test Pydantic data models"""
        try:
            # Test UserCreate model
            user_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "TestPassword123!",
                "full_name": "Test User"
            }
            user = UserCreate(**user_data)
            if user.username == "testuser":
                self.log_test("User Model", "PASSED", "UserCreate model validation working")
            else:
                self.log_test("User Model", "FAILED", "UserCreate model validation failed")
                return False

            # Test MoodLog model
            mood_data = {
                "user_id": "testuser",
                "mood": "happy",
                "note": "Test mood entry"
            }
            mood = MoodLog(**mood_data)
            if mood.user_id == "testuser" and mood.mood == "happy":
                self.log_test("Mood Model", "PASSED", "MoodLog model validation working")
            else:
                self.log_test("Mood Model", "FAILED", "MoodLog model validation failed")
                return False

            return True
        except Exception as e:
            self.log_test("Data Models", "FAILED", f"Model validation error: {str(e)}")
            return False

    async def test_fastapi_app(self):
        """Test FastAPI application"""
        try:
            # Test if app is properly configured
            if hasattr(app, 'routes') and len(app.routes) > 0:
                self.log_test("FastAPI App", "PASSED", f"FastAPI app configured with {len(app.routes)} routes")
            else:
                self.log_test("FastAPI App", "FAILED", "FastAPI app not properly configured")
                return False

            # Test CORS middleware
            if hasattr(app, 'user_middleware') and len(app.user_middleware) > 0:
                self.log_test("CORS Middleware", "PASSED", "CORS middleware configured")
            else:
                self.log_test("CORS Middleware", "FAILED", "CORS middleware not configured")
                return False

            return True
        except Exception as e:
            self.log_test("FastAPI App", "FAILED", f"FastAPI error: {str(e)}")
            return False

    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting SIH Backend Test Suite...")
        print("=" * 50)

        tests = [
            self.test_database_connection,
            self.test_database_initialization,
            self.test_nlp_models,
            self.test_authentication,
            self.test_data_models,
            self.test_fastapi_app
        ]

        passed = 0
        failed = 0

        for test in tests:
            try:
                result = await test()
                if result:
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1
                print(f"❌ Test {test.__name__} crashed: {str(e)}")

        print("=" * 50)
        print(f"📊 TEST SUMMARY:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")

        if failed == 0:
            print("🎉 ALL TESTS PASSED! Backend is ready for production!")
        else:
            print("⚠️ Some tests failed. Please review the results above.")

        return failed == 0

    def generate_report(self):
        """Generate detailed test report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASSED']),
                'failed': len([r for r in self.test_results if r['status'] == 'FAILED'])
            },
            'results': self.test_results
        }

        with open('test_report.json', 'w') as f:
            json.dump(report, f, indent=2)

        print(f"📄 Detailed report saved to test_report.json")

async def main():
    """Main test function"""
    tester = BackendTester()
    success = await tester.run_all_tests()
    tester.generate_report()
    
    if success:
        print("\n🎯 Backend is ready for integration testing!")
        print("Next steps:")
        print("1. Start the server: uvicorn app.main:app --reload")
        print("2. Test frontend integration")
        print("3. Run comprehensive test suite")
    else:
        print("\n🔧 Please fix the failing tests before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
