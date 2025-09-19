# test_error_handling.py - Error Handling and Validation Test Script

## What This File Does
This file is a comprehensive test script that validates error handling, input validation, and security features of the MindCare API. It tests various error scenarios to ensure the system handles them gracefully.

## In Simple Terms
Think of this as a stress test for the API that tries to break it in various ways to make sure it handles errors properly. It's like having a quality inspector who deliberately tries to cause problems to see if the system can handle them safely.

## Test Coverage

### 1. **Input Validation Tests**
```python
def test_validation_errors():
    # Test 1: Invalid user registration data
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
        }
    ]
```

**What it tests:**
- Username length validation (minimum 3 characters)
- Email format validation
- Password strength requirements
- Input format restrictions

### 2. **Mood Logging Validation Tests**
```python
    # Test 2: Invalid mood logging
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
```

**What it tests:**
- Required field validation
- Mood type validation (must be from predefined list)
- Note length limits (maximum 500 characters)
- User ID format validation

### 3. **Authorization Tests**
```python
    # Test 3: Unauthorized access
    # Try to access protected endpoint without token
    response = requests.get(f"{BASE_URL}/auth/me")
    if response.status_code == 401:
        print("✅ Unauthorized access properly blocked")
    
    # Try to access another user's data
    response = requests.get(f"{BASE_URL}/moods/other_user", headers=headers)
    if response.status_code == 403:
        print("✅ Unauthorized access to other user's data blocked")
```

**What it tests:**
- Missing JWT token handling
- Invalid token handling
- Cross-user data access prevention
- Authorization enforcement

### 4. **Duplicate User Tests**
```python
    # Test 4: Duplicate user registration
    # Try to register the same user again
    response = requests.post(f"{BASE_URL}/auth/register", json=valid_user)
    if response.status_code == 400:
        print("✅ Duplicate user registration blocked")
```

**What it tests:**
- Duplicate username prevention
- Duplicate email prevention
- Database constraint enforcement
- Error message clarity

## Test Functions

### 1. **test_validation_errors()**
```python
def test_validation_errors():
    """Test input validation errors."""
    
    print("🧪 Testing Input Validation & Error Handling")
    print("=" * 60)
    
    # Test invalid user registration data
    # Test invalid mood logging data
    # Test unauthorized access scenarios
    # Test duplicate user registration
```

**Purpose:** Tests all input validation and error handling scenarios

### 2. **test_database_error_handling()**
```python
def test_database_error_handling():
    """Test database error handling scenarios."""
    
    print("\n🔧 Testing Database Error Handling...")
    
    # Test server responsiveness
    # Test database connection handling
    # Test service availability
```

**Purpose:** Tests database error handling and service availability

## Test Scenarios

### 1. **Invalid User Registration**
```python
invalid_users = [
    {
        "username": "ab",  # Too short (minimum 3)
        "email": "invalid-email",
        "password": "123",  # Too short (minimum 6)
        "full_name": "Test User"
    },
    {
        "username": "validuser",
        "email": "not-an-email",  # Invalid email format
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
```

**Expected Results:**
- All should return 422 (Validation Error)
- Clear error messages for each validation failure
- Specific field-level error details

### 2. **Invalid Mood Logging**
```python
invalid_moods = [
    {
        "user_id": "",  # Empty user_id
        "mood": "happy",
        "note": "Test note"
    },
    {
        "user_id": valid_user["username"],
        "mood": "invalid_mood",  # Not in allowed list
        "note": "Test note"
    },
    {
        "user_id": valid_user["username"],
        "mood": "happy",
        "note": "x" * 501  # Too long (maximum 500)
    }
]
```

**Expected Results:**
- All should return 422 (Validation Error)
- Specific validation error messages
- Field-level error details

### 3. **Unauthorized Access**
```python
# Test without token
response = requests.get(f"{BASE_URL}/auth/me")
# Expected: 401 Unauthorized

# Test with invalid token
headers = {"Authorization": "Bearer invalid_token"}
response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
# Expected: 401 Unauthorized

# Test accessing another user's data
response = requests.get(f"{BASE_URL}/moods/other_user", headers=valid_headers)
# Expected: 403 Forbidden
```

**Expected Results:**
- 401 for missing/invalid tokens
- 403 for unauthorized data access
- Clear error messages

### 4. **Duplicate User Registration**
```python
# Register user first time
response = requests.post(f"{BASE_URL}/auth/register", json=valid_user)
# Expected: 200 Success

# Try to register same user again
response = requests.post(f"{BASE_URL}/auth/register", json=valid_user)
# Expected: 400 Bad Request
```

**Expected Results:**
- 200 for first registration
- 400 for duplicate registration
- Clear duplicate user error message

## Test Output

### 1. **Success Messages**
```
🧪 Testing Input Validation & Error Handling
============================================================

1️⃣ Testing Invalid User Registration...
   Test 1: Status 422
   ✅ Validation error caught: {"detail": "Validation error", "errors": [...]}
   Test 2: Status 422
   ✅ Validation error caught: {"detail": "Validation error", "errors": [...]}

2️⃣ Testing Invalid Mood Logging...
   Test 1: Status 422
   ✅ Validation error caught: {"detail": "Validation error", "errors": [...]}

3️⃣ Testing Unauthorized Access...
   No token: Status 401
   ✅ Unauthorized access properly blocked
   Other user's data: Status 403
   ✅ Unauthorized access to other user's data blocked

4️⃣ Testing Duplicate User Registration...
   Duplicate user: Status 400
   ✅ Duplicate user registration blocked

🎉 Error handling tests completed!

📝 Summary:
   ✅ Input validation working
   ✅ Authentication working
   ✅ Authorization working
   ✅ Duplicate prevention working
```

### 2. **Error Messages**
```
❌ Expected validation error, got: {"detail": "Internal server error"}
❌ Expected 401, got: 200
❌ Expected 403, got: 200
❌ Connection failed. Make sure the server is running.
```

## Test Data Management

### 1. **Valid Test User Creation**
```python
# First, create a valid user and get token
valid_user = {
    "username": f"testuser{int(time.time())}",
    "email": f"test{int(time.time())}@example.com",
    "password": "testpass123",
    "full_name": "Test User"
}

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
```

**Benefits:**
- Creates valid test data for authorization tests
- Ensures tests can run independently
- Provides authentication for protected endpoint tests
- Handles test data cleanup

### 2. **Test Result Validation**
```python
for i, user_data in enumerate(invalid_users, 1):
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"   Test {i}: Status {response.status_code}")
    if response.status_code == 422:
        print(f"   ✅ Validation error caught: {response.json()}")
    else:
        print(f"   ❌ Expected validation error, got: {response.text}")
```

**Features:**
- Iterates through test cases
- Validates response status codes
- Checks error message format
- Reports test results clearly

## Error Handling

### 1. **Connection Errors**
```python
except requests.exceptions.ConnectionError:
    print("   ❌ Connection failed. Make sure the server is running.")
    return
```

**What it handles:**
- Server not running
- Network connectivity issues
- Invalid server URLs
- Service unavailability

### 2. **Test Failures**
```python
if response.status_code != 200:
    print(f"   ❌ Failed to create test user: {response.text}")
    return  # Stop testing if critical setup fails
```

**What it handles:**
- Critical test setup failures
- Test sequence interruption
- Error propagation
- Test result reporting

### 3. **Unexpected Responses**
```python
if response.status_code == 422:
    print(f"   ✅ Validation error caught: {response.json()}")
else:
    print(f"   ❌ Expected validation error, got: {response.text}")
```

**What it handles:**
- Unexpected response codes
- Validation error format changes
- API behavior changes
- Test result validation

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
python test_error_handling.py
```

### 3. **Expected Results**
- All validation tests should return 422 errors
- All authorization tests should return 401/403 errors
- All duplicate tests should return 400 errors
- Clear error messages for all scenarios

## Test Benefits

### 1. **Quality Assurance**
- Validates error handling functionality
- Ensures security features work correctly
- Verifies input validation
- Confirms error response format

### 2. **Security Validation**
- Tests authentication enforcement
- Validates authorization controls
- Verifies user data isolation
- Confirms security boundaries

### 3. **API Robustness**
- Tests edge cases and error scenarios
- Validates graceful error handling
- Ensures consistent error responses
- Confirms system stability

### 4. **Development Support**
- Quick validation of error handling changes
- Automated error scenario testing
- Clear error reporting
- Test result documentation

## Integration with CI/CD

### 1. **Automated Testing**
- Can be integrated into CI/CD pipelines
- Automated error handling validation
- Test result reporting
- Deployment validation

### 2. **Quality Gates**
- Prevents deployment of broken error handling
- Ensures security features are working
- Validates API robustness
- Maintains system reliability

### 3. **Monitoring**
- Regular error handling validation
- Continuous security verification
- API robustness monitoring
- System stability tracking

This test script provides comprehensive validation of error handling, input validation, and security features, ensuring that the MindCare API handles errors gracefully and maintains security boundaries.