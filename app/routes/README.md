# Routes Directory - API Endpoints

This directory contains all the API endpoint definitions for the MindCare mental health API. Each file defines a specific group of related endpoints.

## Files Overview

### 1. **auth.py** - User Authentication
- User registration and login
- JWT token management
- User profile management
- Protected route examples

### 2. **moods.py** - Mood Tracking
- Log daily moods with notes
- Retrieve mood history
- Delete unwanted mood entries 🆕
- User-specific mood data access

### 3. **chatbot.py** - Basic Chatbot
- Simple chatbot interactions
- Chat history storage
- Basic conversation management

### 4. **gamify.py** - Gamification
- Streak tracking for consistent check-ins
- User progress monitoring
- Engagement features

### 5. **nlp.py** - Advanced AI Analysis
- Sentiment analysis
- Emotion detection
- Toxicity screening
- Distress detection
- Risk assessment
- Advanced chatbot with AI

## How Routes Work

### 1. **Route Registration**
Routes are registered in `main.py`:
```python
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(moods.router, prefix="/moods", tags=["Moods"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Basic Chatbot"])
app.include_router(gamify.router, prefix="/gamify", tags=["Gamification"])
app.include_router(nlp.router, prefix="/nlp", tags=["NLP & Mental Health AI"])
```

### 2. **Authentication**
Most routes require JWT authentication:
```python
@router.get("/moods/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
    # current_user is automatically populated from JWT token
    pass
```

### 3. **User Isolation**
Users can only access their own data:
```python
if user_id != current_user.username:
    raise UnauthorizedAccessError("You can only access your own data")
```

### 4. **Error Handling**
Routes use custom exception handlers for consistent error responses:
```python
try:
    # Database operation
    result = safe_db_operation(collection.find, query)
except (ConnectionFailure, ServerSelectionTimeoutError):
    raise DatabaseConnectionError("Database connection failed")
```

## API Structure

### Base URL
All routes are prefixed with their respective paths:
- `/auth/*` - Authentication endpoints
- `/moods/*` - Mood tracking endpoints
- `/chatbot/*` - Basic chatbot endpoints
- `/gamify/*` - Gamification endpoints
- `/nlp/*` - AI analysis endpoints

### HTTP Methods
- **GET**: Retrieve data
- **POST**: Create new data
- **PUT**: Update existing data
- **DELETE**: Remove data

### Response Format
All endpoints return consistent JSON responses:
```json
{
    "data": "response_data",
    "message": "success_message",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Format
Error responses follow a consistent format:
```json
{
    "detail": "error_message",
    "error_code": "ERROR_CODE",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Security Features

### 1. **JWT Authentication**
- All protected routes require valid JWT tokens
- Tokens expire after 30 minutes
- Automatic token validation

### 2. **User Isolation**
- Users can only access their own data
- Database queries filter by authenticated user
- No cross-user data access

### 3. **Input Validation**
- All inputs are validated using Pydantic models
- Prevents invalid data from entering the system
- Clear error messages for validation failures

### 4. **Error Handling**
- Comprehensive error handling for all scenarios
- No sensitive information exposed in error messages
- Consistent error response format

## Documentation

### 1. **Auto-Generated Docs**
- Swagger UI available at `/docs`
- ReDoc available at `/redoc`
- Interactive API testing

### 2. **Endpoint Documentation**
- Each endpoint has detailed descriptions
- Request/response examples
- Parameter documentation

### 3. **Authentication Documentation**
- JWT token usage examples
- Protected endpoint access
- Error handling examples

This routes directory provides a comprehensive set of API endpoints for mental health tracking, AI analysis, and user management.
