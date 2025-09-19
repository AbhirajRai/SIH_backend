# auth.py - User Authentication Routes

## What This File Does
This file defines all the API endpoints related to user authentication and account management. It's like the "front desk" of the application where users sign up, log in, and manage their accounts.

## In Simple Terms
Think of this as the login system for the mental health app - it handles user registration, login, and provides access to user account information.

## API Endpoints

### 1. **POST /auth/register** - User Registration
```python
@router.post("/register", response_model=User)
async def register(user: UserCreate):
```
**What it does:** Creates a new user account
**Input:** Username, email, password, full name
**Output:** User information (without password)
**Security:** Validates email format, password strength, unique username/email

**Example Request:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
}
```

**Example Response:**
```json
{
    "id": "507f1f77bcf86cd799439011",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. **POST /auth/login** - User Login
```python
@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
```
**What it does:** Authenticates user and returns JWT token
**Input:** Username and password
**Output:** JWT access token
**Security:** Verifies password against stored hash

**Example Request:**
```json
{
    "username": "john_doe",
    "password": "securepassword123"
}
```

**Example Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 3. **POST /auth/token** - Alternative Login
```python
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
```
**What it does:** Alternative login endpoint for FastAPI documentation
**Input:** Username and password via form data
**Output:** JWT access token
**Purpose:** Used by Swagger UI for testing protected endpoints

### 4. **GET /auth/me** - Get Current User
```python
@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
```
**What it does:** Returns information about the currently logged-in user
**Input:** JWT token in Authorization header
**Output:** User profile information
**Security:** Requires valid JWT token

**Example Request:**
```
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

**Example Response:**
```json
{
    "id": "507f1f77bcf86cd799439011",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z"
}
```

### 5. **GET /auth/users/me/items/** - Example Protected Endpoint
```python
@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
```
**What it does:** Example of a protected endpoint that returns user-specific data
**Input:** JWT token in Authorization header
**Output:** User's items (example data)
**Purpose:** Demonstrates how to create protected endpoints

## How Authentication Works

### 1. **Registration Process**
```
User submits registration data
↓
System validates input (email format, password strength, etc.)
↓
System checks if username/email already exists
↓
Password is hashed with bcrypt
↓
User data is stored in database
↓
User account is created successfully
```

### 2. **Login Process**
```
User submits username and password
↓
System finds user in database
↓
Password is verified against stored hash
↓
JWT token is created with user information
↓
Token is returned to user
↓
User can use token for API requests
```

### 3. **Protected Route Access**
```
User makes request with JWT token
↓
System verifies token signature and expiration
↓
User information is extracted from token
↓
Route handler receives authenticated user
↓
User can access their own data
```

## Security Features

### 1. **Password Security**
- **Hashing**: Passwords are hashed with bcrypt before storage
- **Salt**: Each password gets a unique random salt
- **Verification**: Passwords are verified against hashes, never stored in plain text

### 2. **JWT Token Security**
- **Secret Key**: Tokens are signed with a secret key
- **Expiration**: Tokens expire after 30 minutes
- **Algorithm**: Uses HS256 for secure signing

### 3. **Input Validation**
- **Email Format**: Validates email addresses
- **Password Strength**: Requires minimum length, letters, and numbers
- **Username Format**: Restricts special characters
- **Unique Constraints**: Prevents duplicate usernames/emails

### 4. **Error Handling**
- **Duplicate Users**: Returns 400 error for existing username/email
- **Invalid Credentials**: Returns 401 error for wrong password
- **Database Errors**: Handles connection failures gracefully
- **Validation Errors**: Returns 422 error for invalid input

## Error Responses

### 1. **Registration Errors**
```json
// Duplicate username
{
    "detail": "Username already registered",
    "error_code": "DUPLICATE_USER",
    "timestamp": "2024-01-15T10:30:00Z"
}

// Invalid email format
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "email",
            "message": "Invalid email format",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. **Login Errors**
```json
// Invalid credentials
{
    "detail": "Invalid username or password",
    "error_code": "INVALID_CREDENTIALS",
    "timestamp": "2024-01-15T10:30:00Z"
}

// Database connection error
{
    "detail": "Database service temporarily unavailable. Please try again later.",
    "error_code": "DATABASE_CONNECTION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. **Protected Route Errors**
```json
// Missing or invalid token
{
    "detail": "Could not validate credentials",
    "error_code": "UNAUTHORIZED",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Usage Examples

### 1. **Complete Registration and Login Flow**
```bash
# 1. Register a new user
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpassword123",
       "full_name": "Test User"
     }'

# 2. Login to get JWT token
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpassword123"
     }'

# 3. Use JWT token for protected endpoints
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer <your_jwt_token>"
```

### 2. **Using JWT Token in Requests**
```python
import requests

# Login to get token
response = requests.post("http://localhost:8000/auth/login", json={
    "username": "testuser",
    "password": "testpassword123"
})
token = response.json()["access_token"]

# Use token for protected requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/auth/me", headers=headers)
user_info = response.json()
```

## Integration with Other Routes

### 1. **Dependency Injection**
Other routes use the authentication system:
```python
from app.auth import get_current_active_user

@router.get("/moods/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    # current_user is automatically populated from JWT token
    pass
```

### 2. **User Isolation**
All routes ensure users can only access their own data:
```python
if user_id != current_user.username:
    raise UnauthorizedAccessError("You can only access your own data")
```

## Why This Structure Matters

### 1. **Security**
- Secure password storage and verification
- JWT token-based authentication
- User data isolation

### 2. **User Experience**
- Simple registration and login process
- Clear error messages
- Consistent API responses

### 3. **Maintainability**
- Centralized authentication logic
- Reusable authentication dependencies
- Clear separation of concerns

### 4. **Scalability**
- Stateless JWT authentication
- Efficient user verification
- Easy to add new protected endpoints

This authentication system provides a secure, user-friendly foundation for the MindCare API, ensuring that only authorized users can access their own mental health data.
