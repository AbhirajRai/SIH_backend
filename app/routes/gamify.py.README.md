# gamify.py - Gamification and Streak Tracking Routes

## What This File Does
This file defines API endpoints for gamification features, specifically streak tracking. It encourages users to maintain consistent mental health check-ins by tracking their daily engagement.

## In Simple Terms
Think of this as a points and streaks system that rewards users for regularly using the mental health app. It's like a fitness app that tracks your daily workout streak - but for mental health activities.

## API Endpoints

### 1. **POST /gamify/streak/{user_id}** - Update Streak
```python
@router.post("/streak/{user_id}")
def update_streak(user_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Increments the streak count for a user (typically called when they log a mood or use the app)
**Input:** User ID in URL path
**Output:** Updated streak count and confirmation message
**Security:** Requires JWT authentication, user can only update their own streak

**Example Request:**
```
POST /gamify/streak/john_doe
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "user_id": "john_doe",
    "streak": 5,
    "message": "Streak updated successfully"
}
```

### 2. **GET /gamify/streak/{user_id}** - Get Current Streak
```python
@router.get("/streak/{user_id}")
def get_streak(user_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Retrieves the current streak count for a user
**Input:** User ID in URL path
**Output:** Current streak count
**Security:** Requires JWT authentication, user can only access their own streak

**Example Request:**
```
GET /gamify/streak/john_doe
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "user_id": "john_doe",
    "streak": 5,
    "message": "Current streak: 5 days"
}
```

## How Streak Tracking Works

### 1. **Streak Update Process**
```
User performs an action (logs mood, uses chatbot, etc.)
↓
System validates user authentication
↓
System checks if user can update their own streak
↓
System finds existing streak or creates new one
↓
Streak count is incremented by 1
↓
Updated streak is stored in database
↓
Confirmation is returned to user
```

### 2. **Streak Retrieval Process**
```
User requests their current streak
↓
System validates JWT token
↓
System checks if user can access requested data
↓
System queries database for user's streak
↓
Streak count is returned (0 if no streak exists)
```

### 3. **Database Operations**
```python
# Check if streak exists
user_streak = safe_db_operation(streaks_collection.find_one, {"user_id": user_id})

if user_streak:
    # Increment existing streak
    new_streak = user_streak["streak"] + 1
    safe_db_operation(
        streaks_collection.update_one,
        {"user_id": user_id},
        {"$set": {"streak": new_streak}}
    )
else:
    # Create new streak starting at 1
    new_streak = 1
    safe_db_operation(streaks_collection.insert_one, {"user_id": user_id, "streak": new_streak})
```

## Gamification Benefits

### 1. **User Engagement**
- Encourages daily app usage
- Creates positive reinforcement
- Builds healthy habits

### 2. **Motivation**
- Visual progress tracking
- Achievement recognition
- Goal-oriented behavior

### 3. **Consistency**
- Promotes regular mental health check-ins
- Establishes routine
- Maintains engagement over time

### 4. **Mental Health Benefits**
- Regular mood tracking
- Consistent self-reflection
- Habit formation for well-being

## Security Features

### 1. **Authentication Required**
- All endpoints require valid JWT tokens
- Users must be logged in to update or view streaks
- Automatic token validation

### 2. **User Isolation**
- Users can only update their own streaks
- Users can only view their own streak data
- Database queries filter by authenticated user

### 3. **Data Validation**
- User IDs are validated for format
- Prevents unauthorized access
- Ensures data integrity

### 4. **Error Handling**
- Comprehensive error handling for all scenarios
- Clear error messages for failures
- Database error handling

## Error Responses

### 1. **Authorization Errors**
```json
// Trying to access another user's data
{
    "detail": "You can only update your own streak",
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

### 2. **Database Errors**
```json
// Database connection failure
{
    "detail": "Database service temporarily unavailable. Please try again later.",
    "error_code": "DATABASE_CONNECTION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. **Not Found Errors**
```json
// No streak found for user
{
    "user_id": "john_doe",
    "streak": 0,
    "message": "No streak found"
}
```

## Usage Examples

### 1. **Updating a Streak**
```bash
# Update streak count
curl -X POST "http://localhost:8000/gamify/streak/john_doe" \
     -H "Authorization: Bearer <jwt_token>"
```

### 2. **Getting Current Streak**
```bash
# Get current streak
curl -X GET "http://localhost:8000/gamify/streak/john_doe" \
     -H "Authorization: Bearer <jwt_token>"
```

### 3. **Using in Applications**
```python
import requests

# Set up authentication
headers = {"Authorization": f"Bearer {jwt_token}"}

# Update streak (e.g., after logging a mood)
response = requests.post("http://localhost:8000/gamify/streak/john_doe", headers=headers)
streak_data = response.json()
print(f"Streak updated to: {streak_data['streak']} days")

# Get current streak
response = requests.get("http://localhost:8000/gamify/streak/john_doe", headers=headers)
streak_info = response.json()
print(f"Current streak: {streak_info['streak']} days")
```

## Database Structure

### Streaks Collection
```json
{
    "_id": "ObjectId",
    "user_id": "string",
    "streak": "number"
}
```

### Indexes
- **user_id**: Unique index for fast user-specific queries
- Prevents duplicate streak records per user

## Integration with Other Features

### 1. **Mood Tracking Integration**
```python
# In mood logging endpoint
@router.post("/moods/")
def log_mood(mood: MoodLog, current_user: User = Depends(get_current_active_user)):
    # Log the mood
    result = safe_db_operation(moods_collection.insert_one, mood_data)
    
    # Update streak
    streak_response = requests.post(f"http://localhost:8000/gamify/streak/{current_user.username}", 
                                  headers={"Authorization": f"Bearer {jwt_token}"})
    
    return {"message": "Mood logged and streak updated", "data": mood}
```

### 2. **Chatbot Integration**
```python
# In chatbot endpoint
@router.post("/chatbot/")
def chat(msg: ChatMessage, current_user: User = Depends(get_current_active_user)):
    # Process chat message
    reply = generate_bot_response(msg.message)
    
    # Update streak for engagement
    update_streak(current_user.username)
    
    return {"user": msg.message, "bot": reply}
```

### 3. **AI Analysis Integration**
```python
# In NLP analysis endpoint
@router.post("/nlp/analyze")
def comprehensive_analysis(request: ComprehensiveAnalysisRequest, current_user: User = Depends(get_current_active_user)):
    # Perform AI analysis
    analysis_result = perform_analysis(request.text)
    
    # Update streak for using AI features
    update_streak(current_user.username)
    
    return analysis_result
```

## Future Enhancements

### 1. **Advanced Gamification**
- Achievement badges
- Level progression
- Reward systems
- Social features

### 2. **Streak Management**
- Streak recovery options
- Streak milestones
- Streak history
- Streak analytics

### 3. **Personalization**
- Custom streak goals
- Personalized rewards
- Adaptive challenges
- Progress insights

### 4. **Social Features**
- Friend comparisons
- Group challenges
- Leaderboards
- Sharing achievements

## Why This Structure Matters

### 1. **User Engagement**
- Encourages consistent app usage
- Creates positive reinforcement
- Builds healthy habits

### 2. **Mental Health Benefits**
- Promotes regular self-reflection
- Establishes routine check-ins
- Maintains engagement over time

### 3. **Data Collection**
- Tracks user engagement patterns
- Enables usage analytics
- Supports personalization

### 4. **Scalability**
- Easy to add new gamification features
- Modular design for enhancements
- Clear separation of concerns

## Best Practices

### 1. **Streak Logic**
- Update streaks for meaningful actions
- Consider streak recovery options
- Balance challenge with achievability

### 2. **User Experience**
- Provide clear streak information
- Celebrate milestones
- Offer encouragement for consistency

### 3. **Data Management**
- Ensure streak data integrity
- Handle edge cases gracefully
- Provide streak history when needed

This gamification system provides a foundation for encouraging consistent mental health engagement while maintaining security and data integrity. It can be easily enhanced with additional features like achievements, rewards, and social elements.
