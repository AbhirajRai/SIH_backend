# moods.py - Mood Tracking Routes

## What This File Does
This file defines API endpoints for mood tracking functionality. It allows users to log their daily moods, retrieve their mood history over time, and delete unwanted mood entries.

## In Simple Terms
Think of this as a digital mood diary where users can record how they're feeling each day, add notes about their mood, look back at their emotional patterns over time, and delete entries they no longer want to keep.

## API Endpoints

### 1. **POST /moods/** - Log a New Mood
```python
@router.post("/")
def log_mood(mood: MoodLog, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Records a new mood entry for the current user
**Input:** User ID, mood type, and optional note
**Output:** Confirmation message and mood data
**Security:** Requires JWT authentication, user can only log moods for themselves

**Example Request:**
```json
{
    "user_id": "john_doe",
    "mood": "happy",
    "note": "Had a great day at work!"
}
```

**Example Response:**
```json
{
    "message": "Mood logged successfully ✅",
    "id": "507f1f77bcf86cd799439011",
    "data": {
        "user_id": "john_doe",
        "mood": "happy",
        "note": "Had a great day at work!"
    }
}
```

### 2. **GET /moods/{user_id}** - Get Mood History
```python
@router.get("/{user_id}")
def get_mood_history(user_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Retrieves all mood entries for a specific user
**Input:** User ID in URL path
**Output:** List of mood entries with timestamps
**Security:** Requires JWT authentication, user can only access their own mood history

**Example Request:**
```
GET /moods/john_doe
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "user_id": "john_doe",
    "history": [
        {
            "user_id": "john_doe",
            "mood": "happy",
            "note": "Had a great day at work!",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "user_id": "john_doe",
            "mood": "anxious",
            "note": "Feeling nervous about the presentation",
            "timestamp": "2024-01-14T15:45:00Z"
        }
    ],
    "count": 2
}
```

### 3. **DELETE /moods/{mood_id}** - Delete a Mood Log
```python
@router.delete("/{mood_id}")
def delete_mood_log(mood_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Permanently deletes a specific mood entry for the current user
**Input:** Mood ID in URL path
**Output:** Confirmation message with deleted mood ID
**Security:** Requires JWT authentication, user can only delete their own mood logs

**Example Request:**
```
DELETE /moods/507f1f77bcf86cd799439011
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "message": "Mood log deleted successfully ✅",
    "deleted_id": "507f1f77bcf86cd799439011"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid mood ID format
- `403 Forbidden`: User trying to delete someone else's mood log
- `404 Not Found`: Mood log not found or already deleted

## Mood Types

The system supports the following mood categories:
- **happy** - Feeling joyful and positive
- **sad** - Feeling down or melancholy
- **angry** - Feeling frustrated or irritated
- **anxious** - Feeling worried or nervous
- **excited** - Feeling enthusiastic and energetic
- **calm** - Feeling peaceful and relaxed
- **stressed** - Feeling overwhelmed or pressured
- **confused** - Feeling uncertain or puzzled
- **grateful** - Feeling thankful and appreciative
- **lonely** - Feeling isolated or disconnected
- **content** - Feeling satisfied and at ease
- **overwhelmed** - Feeling swamped or unable to cope

## How Mood Tracking Works

### 1. **Mood Logging Process**
```
User submits mood data
↓
System validates mood type and user ID
↓
System checks if user is authenticated
↓
System verifies user can only log moods for themselves
↓
Timestamp is automatically added
↓
Mood entry is stored in database
↓
Confirmation is returned to user
```

### 2. **Mood History Retrieval**
```
User requests mood history
↓
System validates JWT token
↓
System checks if user can access requested data
↓
System queries database for user's mood entries
↓
Mood history is returned with timestamps
```

## Data Validation

### 1. **Mood Type Validation**
```python
@validator('mood')
def validate_mood(cls, v):
    valid_moods = ['happy', 'sad', 'angry', 'anxious', 'excited', 'calm', 'stressed', 'confused', 'grateful', 'lonely', 'content', 'overwhelmed']
    if v.lower() not in valid_moods:
        raise ValueError(f'Mood must be one of: {", ".join(valid_moods)}')
    return v.lower()
```

### 2. **User ID Validation**
```python
@validator('user_id')
def validate_user_id(cls, v):
    if not re.match(r'^[a-zA-Z0-9_-]+$', v):
        raise ValueError('User ID can only contain letters, numbers, underscores, and hyphens')
    return v
```

### 3. **Note Length Validation**
- Notes are optional
- Maximum length: 500 characters
- Prevents extremely long notes that could cause issues

## Security Features

### 1. **Authentication Required**
- All endpoints require valid JWT tokens
- Users must be logged in to log or view moods
- Automatic token validation

### 2. **User Isolation**
- Users can only log moods for themselves
- Users can only view their own mood history
- Database queries filter by authenticated user

### 3. **Input Validation**
- Mood types are restricted to predefined list
- User IDs are validated for format
- Note length is limited

### 4. **Error Handling**
- Comprehensive error handling for all scenarios
- Clear error messages for validation failures
- Database error handling

## Error Responses

### 1. **Validation Errors**
```json
// Invalid mood type
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "mood",
            "message": "Mood must be one of: happy, sad, angry, anxious, excited, calm, stressed, confused, grateful, lonely, content, overwhelmed",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}

// Note too long
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "note",
            "message": "Note must be less than 500 characters",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 2. **Authorization Errors**
```json
// Trying to access another user's data
{
    "detail": "You can only access your own mood history",
    "error_code": "UNAUTHORIZED_ACCESS",
    "timestamp": "2024-01-15T10:30:00Z"
}

// Invalid JWT token
{
    "detail": "Could not validate credentials",
    "error_code": "UNAUTHORIZED",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. **Database Errors**
```json
// Database connection failure
{
    "detail": "Database service temporarily unavailable. Please try again later.",
    "error_code": "DATABASE_CONNECTION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Usage Examples

### 1. **Logging a Mood**
```bash
# Log a happy mood
curl -X POST "http://localhost:8000/moods/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{
       "user_id": "john_doe",
       "mood": "happy",
       "note": "Had a great day at work!"
     }'

# Log a sad mood without note
curl -X POST "http://localhost:8000/moods/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{
       "user_id": "john_doe",
       "mood": "sad"
     }'
```

### 2. **Retrieving Mood History**
```bash
# Get all moods for a user
curl -X GET "http://localhost:8000/moods/john_doe" \
     -H "Authorization: Bearer <jwt_token>"
```

### 3. **Using in Applications**
```python
import requests

# Set up authentication
headers = {"Authorization": f"Bearer {jwt_token}"}

# Log a mood
mood_data = {
    "user_id": "john_doe",
    "mood": "anxious",
    "note": "Feeling nervous about the presentation tomorrow"
}
response = requests.post("http://localhost:8000/moods/", json=mood_data, headers=headers)
print(response.json())

# Get mood history
response = requests.get("http://localhost:8000/moods/john_doe", headers=headers)
mood_history = response.json()
print(f"User has {mood_history['count']} mood entries")
```

## Database Structure

### Moods Collection
```json
{
    "_id": "ObjectId",
    "user_id": "string",
    "mood": "string",
    "note": "string (optional)",
    "timestamp": "datetime"
}
```

### Indexes
- **user_id**: For fast user-specific queries
- **(user_id, timestamp)**: For sorted mood history

## Integration with Other Features

### 1. **AI Analysis**
Mood data can be used for:
- Sentiment analysis over time
- Emotion pattern recognition
- Risk assessment based on mood trends

### 2. **Gamification**
Mood logging can contribute to:
- Streak tracking for consistent check-ins
- Achievement systems
- Progress monitoring

### 3. **Chatbot Integration**
Mood data can inform:
- Personalized chatbot responses
- Emotional context for conversations
- Targeted support recommendations

## Why This Structure Matters

### 1. **User Experience**
- Simple mood logging process
- Clear mood categories
- Optional notes for context

### 2. **Data Quality**
- Validated mood types
- Consistent data format
- Timestamp tracking

### 3. **Privacy and Security**
- User data isolation
- Authentication required
- Secure data storage

### 4. **Analytics Potential**
- Historical mood tracking
- Pattern recognition
- Trend analysis

This mood tracking system provides a foundation for users to monitor their emotional well-being over time, with the data being used for AI analysis, gamification, and personalized support.
