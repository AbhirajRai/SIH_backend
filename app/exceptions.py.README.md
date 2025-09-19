# exceptions.py - Error Handling and Exception Management

## What This File Does
This file defines custom error types and handles all the different kinds of errors that can occur in the MindCare API. It's like the "emergency response team" that knows how to handle different types of problems.

## In Simple Terms
Think of this as the customer service department that knows exactly what to say and do when something goes wrong. Instead of showing confusing technical errors to users, it provides clear, helpful messages.

## Key Responsibilities

### 1. **Custom Exception Classes**
- Defines specific error types for different scenarios
- Makes error handling more precise and organized
- Allows different error types to be handled differently

### 2. **Error Response Formatting**
- Converts technical errors into user-friendly messages
- Provides consistent error response format
- Includes helpful information like error codes and timestamps

### 3. **Error Logging**
- Records errors for debugging and monitoring
- Helps developers understand what went wrong
- Provides audit trail for security issues

## Custom Exception Classes

### 1. **DatabaseConnectionError**
```python
class DatabaseConnectionError(Exception):
    """Raised when database connection fails"""
```
**When it occurs:** Database server is down, network issues, connection timeouts
**User sees:** "Database service temporarily unavailable. Please try again later."

### 2. **UserNotFoundError**
```python
class UserNotFoundError(Exception):
    """Raised when user is not found"""
```
**When it occurs:** Trying to access a user that doesn't exist
**User sees:** "User not found"

### 3. **InvalidCredentialsError**
```python
class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid"""
```
**When it occurs:** Wrong username or password during login
**User sees:** "Invalid username or password"

### 4. **DuplicateUserError**
```python
class DuplicateUserError(Exception):
    """Raised when trying to create a user that already exists"""
```
**When it occurs:** Trying to register with existing username or email
**User sees:** "User with this username or email already exists"

### 5. **UnauthorizedAccessError**
```python
class UnauthorizedAccessError(Exception):
    """Raised when user tries to access data they don't own"""
```
**When it occurs:** User tries to access another user's data
**User sees:** "You can only access your own data"

## Error Handler Functions

### 1. **Database Connection Handler**
```python
async def database_connection_handler(request: Request, exc: DatabaseConnectionError):
    return JSONResponse(
        status_code=503,  # Service Unavailable
        content={
            "detail": "Database service temporarily unavailable. Please try again later.",
            "error_code": "DATABASE_CONNECTION_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 2. **User Not Found Handler**
```python
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,  # Not Found
        content={
            "detail": "User not found",
            "error_code": "USER_NOT_FOUND",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 3. **Invalid Credentials Handler**
```python
async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=401,  # Unauthorized
        content={
            "detail": "Invalid username or password",
            "error_code": "INVALID_CREDENTIALS",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 4. **Validation Error Handler**
```python
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append({
            "field": field,
            "message": message,
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={
            "detail": "Validation error",
            "errors": errors,
            "error_code": "VALIDATION_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

## Error Response Format

### Standard Error Response
```json
{
    "detail": "Human-readable error message",
    "error_code": "MACHINE_READABLE_CODE",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Validation Error Response
```json
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "password",
            "message": "Password must contain at least one letter",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## HTTP Status Codes

### 1. **400 Bad Request**
- Duplicate user registration
- Invalid data format
- Business logic errors

### 2. **401 Unauthorized**
- Invalid login credentials
- Missing or invalid JWT token
- Authentication failures

### 3. **403 Forbidden**
- User trying to access another user's data
- Insufficient permissions
- Authorization failures

### 4. **404 Not Found**
- User not found
- Resource doesn't exist
- Invalid endpoint

### 5. **422 Unprocessable Entity**
- Validation errors
- Invalid input data
- Format errors

### 6. **500 Internal Server Error**
- Unexpected application errors
- System failures
- Unhandled exceptions

### 7. **503 Service Unavailable**
- Database connection failures
- External service failures
- System maintenance

## Error Handling Flow

### 1. **Error Occurs**
```python
# In a route handler
if user_id != current_user.username:
    raise UnauthorizedAccessError("You can only access your own data")
```

### 2. **Exception Handler Catches It**
```python
# In main.py
app.add_exception_handler(UnauthorizedAccessError, unauthorized_access_handler)
```

### 3. **Handler Processes Error**
```python
async def unauthorized_access_handler(request: Request, exc: UnauthorizedAccessError):
    return JSONResponse(
        status_code=403,
        content={
            "detail": "You can only access your own data",
            "error_code": "UNAUTHORIZED_ACCESS",
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

### 4. **Client Receives Response**
```json
{
    "detail": "You can only access your own data",
    "error_code": "UNAUTHORIZED_ACCESS",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Security Features

### 1. **Information Hiding**
- Technical details are not exposed to users
- Error messages don't reveal system internals
- Sensitive information is logged but not returned

### 2. **Consistent Responses**
- All errors follow the same format
- Error codes help with programmatic handling
- Timestamps help with debugging

### 3. **Logging**
- Errors are logged for monitoring
- Helps identify security issues
- Provides audit trail

## Why This Structure Matters

### 1. **User Experience**
- Clear, helpful error messages
- Consistent error format
- No confusing technical jargon

### 2. **Security**
- Sensitive information is protected
- Error messages don't reveal system details
- Proper HTTP status codes

### 3. **Maintainability**
- Centralized error handling
- Easy to modify error messages
- Clear separation of concerns

### 4. **Debugging**
- Errors are logged for developers
- Error codes help identify issues
- Timestamps help with troubleshooting

## Usage Examples

### In Route Handlers
```python
@router.get("/moods/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    if user_id != current_user.username:
        raise UnauthorizedAccessError("You can only access your own data")
    
    # If database fails, DatabaseConnectionError will be raised automatically
    moods = list(moods_collection.find({"user_id": user_id}))
    return {"moods": moods}
```

### Error Response Example
```python
# Client receives this when trying to access another user's data
{
    "detail": "You can only access your own data",
    "error_code": "UNAUTHORIZED_ACCESS",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

This exception handling system provides a robust, user-friendly way to handle errors while maintaining security and providing useful information for debugging and monitoring.
