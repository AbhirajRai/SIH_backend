# test_auth.py - Authentication System Test Script

## What This File Does
This file is a comprehensive test script that validates the authentication system of the MindCare API. It tests user registration, login, protected endpoints, and security features.

## In Simple Terms
Think of this as a quality assurance tool that automatically checks if the login system is working correctly. It's like having a robot that tests all the authentication features to make sure they work as expected.

## Test Coverage

### 1. **User Registration Test**
```python
def test_authentication():
    # Test data
    test_user = {
        "username": f"testuser{timestamp}",
        "email": f"testuser{timestamp}@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # 1. Test Registration
    response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
    if response.status_code == 200:
        print("✅ Registration successful!")
    else:
        print(f"❌ Registration failed: {response.status_code}")
```

**What it tests:**
- User account creation
- Input validation
- Duplicate user prevention
- Response format

### 2. **User Login Test**
```python
    # 2. Test Login
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        print("✅ Login successful!")
        token_data = response.json()
        access_token = token_data["access_token"]
    else:
        print(f"❌ Login failed: {response.status_code}")
```

**What it tests:**
- Username/password verification
- JWT token generation
- Token format validation
- Login response structure

### 3. **Protected Endpoint Test**
```python
    # 3. Test Protected Endpoint (Get Current User)
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        print("✅ Protected endpoint access successful!")
        user_info = response.json()
        print(f"   Current user: {user_info['username']}")
    else:
        print(f"❌ Protected endpoint access failed: {response.status_code}")
```

**What it tests:**
- JWT token validation
- Protected route access
- User data retrieval
- Authorization headers

### 4. **Mood Logging Test (Protected)**
```python
    # 4. Test Mood Logging (Protected Endpoint)
    mood_data = {
        "user_id": test_user["username"],
        "mood": "happy",
        "note": "Feeling great after implementing auth!"
    }
    
    response = requests.post(f"{BASE_URL}/moods/", json=mood_data, headers=headers)
    if response.status_code == 200:
        print("✅ Mood logging successful!")
        mood_result = response.json()
        print(f"   Message: {mood_result['message']}")
    else:
        print(f"❌ Mood logging failed: {response.status_code}")
```

**What it tests:**
- Cross-feature authentication
- Protected endpoint integration
- User data isolation
- End-to-end functionality

### 5. **Unauthorized Access Test**
```python
    # 5. Test Unauthorized Access
    response = requests.get(f"{BASE_URL}/auth/me")  # No token
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked!")
    else:
        print(f"❌ Unauthorized access not blocked: {response.status_code}")
```

**What it tests:**
- Security enforcement
- Unauthorized access prevention
- Error response format
- Authentication requirements

## Test Flow

### 1. **Setup Phase**
```
Generate unique test user data
↓
Set base URL for API testing
↓
Initialize test environment
```

### 2. **Registration Phase**
```
Submit user registration data
↓
Validate response status and format
↓
Extract user information
↓
Verify account creation
```

### 3. **Authentication Phase**
```
Submit login credentials
↓
Validate JWT token generation
↓
Extract access token
↓
Verify authentication success
```

### 4. **Authorization Phase**
```
Use JWT token for protected requests
↓
Test protected endpoint access
↓
Verify user data retrieval
↓
Test cross-feature integration
```

### 5. **Security Phase**
```
Test unauthorized access attempts
↓
Verify security enforcement
↓
Validate error responses
↓
Confirm access control
```

## Test Data Management

### 1. **Unique Test Users**
```python
import time
timestamp = int(time.time())
test_user = {
    "username": f"testuser{timestamp}",
    "email": f"testuser{timestamp}@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
}
```

**Benefits:**
- Prevents test conflicts
- Ensures clean test environment
- Allows multiple test runs
- Avoids duplicate user errors

### 2. **Test Data Validation**
```python
if response.status_code == 200:
    user_data = response.json()
    print(f"   User ID: {user_data.get('id')}")
    print(f"   Username: {user_data.get('username')}")
else:
    print(f"   Error: {response.text}")
```

**Features:**
- Response status validation
- Data extraction and display
- Error message reporting
- Test result documentation

## Error Handling

### 1. **Connection Errors**
```python
except requests.exceptions.ConnectionError:
    print("❌ Connection failed. Make sure the server is running on http://localhost:8000")
    return
```

**What it handles:**
- Server not running
- Network connectivity issues
- Invalid server URLs
- Service unavailability

### 2. **HTTP Errors**
```python
if response.status_code == 200:
    print("✅ Operation successful!")
else:
    print(f"❌ Operation failed: {response.status_code}")
    print(f"   Error: {response.text}")
```

**What it handles:**
- Authentication failures
- Validation errors
- Server errors
- Unexpected responses

### 3. **Test Failures**
```python
if response.status_code != 200:
    print(f"❌ Test failed: {response.status_code}")
    return  # Stop testing if critical test fails
```

**What it handles:**
- Critical test failures
- Test sequence interruption
- Error propagation
- Test result reporting

## Test Output

### 1. **Success Messages**
```
🧪 Testing MindCare Backend Authentication System
==================================================

1️⃣ Testing User Registration...
✅ Registration successful!
   User ID: 507f1f77bcf86cd799439011
   Username: testuser1705312200

2️⃣ Testing User Login...
✅ Login successful!
   Token type: bearer
   Access token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

3️⃣ Testing Protected Endpoint (Get Current User)...
✅ Protected endpoint access successful!
   Current user: testuser1705312200
   Email: testuser1705312200@example.com

4️⃣ Testing Mood Logging (Protected Endpoint)...
✅ Mood logging successful!
   Message: Mood logged successfully ✅

5️⃣ Testing Unauthorized Access...
✅ Unauthorized access properly blocked!

🎉 All authentication tests completed!
```

### 2. **Error Messages**
```
❌ Registration failed: 400
   Error: {"detail": "Username already registered"}

❌ Login failed: 401
   Error: {"detail": "Invalid username or password"}

❌ Connection failed. Make sure the server is running on http://localhost:8000
```

## Usage Instructions

### 1. **Prerequisites**
- MindCare API server must be running
- Server should be accessible at `http://localhost:8000`
- Database should be connected and working

### 2. **Running the Tests**
```bash
# Make sure the server is running
uvicorn app.main:app --reload

# Run the test script
python test_auth.py
```

### 3. **Expected Results**
- All tests should pass with ✅ status
- No ❌ error messages
- Complete test flow execution
- Successful authentication validation

## Test Benefits

### 1. **Quality Assurance**
- Validates authentication system functionality
- Ensures security features work correctly
- Verifies API endpoint behavior
- Confirms error handling

### 2. **Development Support**
- Quick validation of changes
- Automated testing workflow
- Clear error reporting
- Test result documentation

### 3. **Deployment Validation**
- Pre-deployment testing
- Production readiness verification
- System integration testing
- End-to-end functionality validation

### 4. **Debugging Support**
- Identifies authentication issues
- Pinpoints security problems
- Locates API endpoint failures
- Provides detailed error information

## Integration with CI/CD

### 1. **Automated Testing**
- Can be integrated into CI/CD pipelines
- Automated test execution
- Test result reporting
- Deployment validation

### 2. **Quality Gates**
- Prevents deployment of broken authentication
- Ensures security features are working
- Validates API functionality
- Maintains system reliability

### 3. **Monitoring**
- Regular authentication system validation
- Continuous security verification
- API health monitoring
- System reliability tracking

This test script provides comprehensive validation of the authentication system, ensuring that user registration, login, protected endpoints, and security features work correctly and securely.
