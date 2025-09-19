# auth.py - Authentication and Authorization

## What This File Does
This file handles all user authentication and authorization for the MindCare API. It's like the "security guard" that verifies who users are and what they're allowed to do.

## In Simple Terms
Think of this as the bouncer at a club - it checks IDs (passwords), issues wristbands (JWT tokens), and makes sure only authorized people can access certain areas of the application.

## Key Responsibilities

### 1. **Password Security**
- **Hash passwords**: Converts plain text passwords into secure hashes using bcrypt
- **Verify passwords**: Checks if a login password matches the stored hash
- **Secure storage**: Passwords are never stored in plain text

### 2. **JWT Token Management**
- **Create tokens**: Generates JWT tokens when users log in
- **Verify tokens**: Checks if tokens are valid and not expired
- **Token expiration**: Tokens automatically expire after 30 minutes for security

### 3. **User Authentication**
- **Login verification**: Checks username and password combinations
- **User lookup**: Finds users in the database by username
- **Active user check**: Ensures only active users can access the system

### 4. **Authorization**
- **Current user**: Gets the currently logged-in user from JWT tokens
- **Protected routes**: Ensures only authenticated users can access certain endpoints
- **User isolation**: Users can only access their own data

## How It Works

### Password Hashing
```python
def get_password_hash(password: str) -> str:
    # Converts "mypassword123" into something like "$2b$12$..."
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Checks if "mypassword123" matches the stored hash
    return pwd_context.verify(plain_password, hashed_password)
```

### JWT Token Creation
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Creates a token like "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### User Authentication Flow
```python
def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    # 1. Find user in database
    user = get_user(username)
    if not user:
        return None
    
    # 2. Check if password is correct
    if not verify_password(password, user.hashed_password):
        return None
    
    # 3. Return user if authentication successful
    return user
```

## Security Features

### 1. **Bcrypt Password Hashing**
- **Salt**: Each password gets a unique random salt
- **Cost factor**: Configurable difficulty (default 12 rounds)
- **Time-resistant**: Takes time to hash, making brute force attacks slow

### 2. **JWT Token Security**
- **Secret key**: Tokens are signed with a secret key
- **Expiration**: Tokens expire after 30 minutes
- **Algorithm**: Uses HS256 for secure signing

### 3. **User Isolation**
- Users can only access their own data
- JWT tokens contain username for identification
- Database queries filter by authenticated user

## Key Functions Explained

### 1. **get_user(username)**
- Finds a user in the database by username
- Returns user data including hashed password
- Used for login verification

### 2. **authenticate_user(username, password)**
- Verifies login credentials
- Returns user if credentials are correct
- Returns None if authentication fails

### 3. **create_access_token(data)**
- Creates JWT token with user information
- Sets expiration time
- Signs token with secret key

### 4. **verify_token(token)**
- Decodes and verifies JWT token
- Checks if token is expired
- Returns user data if valid

### 5. **get_current_user(credentials)**
- Gets current user from JWT token
- Used as dependency in protected routes
- Raises exception if token is invalid

### 6. **get_current_active_user(current_user)**
- Ensures user is active (not deactivated)
- Additional security layer
- Used for sensitive operations

## Authentication Flow

### 1. **User Registration**
```
User submits: username, email, password
↓
Password is hashed with bcrypt
↓
User data is stored in database
↓
User can now log in
```

### 2. **User Login**
```
User submits: username, password
↓
System finds user in database
↓
Password is verified against hash
↓
JWT token is created and returned
↓
User can use token for API requests
```

### 3. **Protected Route Access**
```
User makes request with JWT token
↓
Token is verified and decoded
↓
User information is extracted
↓
Route handler receives authenticated user
↓
User can access their own data
```

## Security Best Practices

### 1. **Password Security**
- Passwords are never stored in plain text
- Bcrypt provides strong hashing with salt
- Password verification is time-constant

### 2. **Token Security**
- Tokens expire automatically
- Secret key is configurable
- Tokens are signed to prevent tampering

### 3. **User Isolation**
- Users can only access their own data
- Database queries filter by authenticated user
- No cross-user data access

### 4. **Error Handling**
- Authentication failures don't reveal user existence
- Invalid tokens return generic error messages
- Logging helps with security monitoring

## Usage Examples

### In Route Handlers
```python
@router.get("/moods/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    # current_user is automatically populated from JWT token
    if user_id != current_user.username:
        raise HTTPException(status_code=403, detail="Access denied")
    # User can only access their own mood history
```

### Token Verification
```python
# This happens automatically in protected routes
token_data = verify_token(credentials.credentials)
if token_data is None:
    raise credentials_exception  # Token is invalid or expired
```

This authentication system provides secure, scalable user management with proper password protection, token-based authentication, and user data isolation.
