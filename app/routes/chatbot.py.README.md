# chatbot.py - Basic Chatbot Routes

## What This File Does
This file defines API endpoints for basic chatbot functionality. It provides simple conversation capabilities where users can send messages and receive responses.

## In Simple Terms
Think of this as a simple chat interface where users can talk to a basic chatbot. It's like having a conversation with a helpful assistant that remembers what you've talked about.

## API Endpoints

### 1. **POST /chatbot/** - Send Message to Chatbot
```python
@router.post("/")
def chat(msg: ChatMessage, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Sends a message to the chatbot and receives a response
**Input:** User ID and message text
**Output:** User's message and bot's reply
**Security:** Requires JWT authentication, user can only chat for themselves

**Example Request:**
```json
{
    "user_id": "john_doe",
    "message": "I'm feeling really stressed today"
}
```

**Example Response:**
```json
{
    "user": "I'm feeling really stressed today",
    "bot": "Hey john_doe, I hear you. Stay strong ❤️"
}
```

### 2. **GET /chatbot/{user_id}** - Get Chat History
```python
@router.get("/{user_id}")
def get_chat_history(user_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Retrieves all chat messages for a specific user
**Input:** User ID in URL path
**Output:** List of chat messages with timestamps
**Security:** Requires JWT authentication, user can only access their own chat history

**Example Request:**
```
GET /chatbot/john_doe
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "user_id": "john_doe",
    "history": [
        {
            "user_id": "john_doe",
            "message": "I'm feeling really stressed today",
            "bot_reply": "Hey john_doe, I hear you. Stay strong ❤️",
            "timestamp": "2024-01-15T10:30:00Z"
        },
        {
            "user_id": "john_doe",
            "message": "How can I manage my stress?",
            "bot_reply": "Hey john_doe, I hear you. Stay strong ❤️",
            "timestamp": "2024-01-15T10:35:00Z"
        }
    ],
    "count": 2
}
```

## How the Basic Chatbot Works

### 1. **Message Processing**
```
User sends message
↓
System validates user authentication
↓
System checks if user can chat for themselves
↓
System generates bot response
↓
Conversation is stored in database
↓
Response is returned to user
```

### 2. **Response Generation**
The basic chatbot currently provides simple, supportive responses:
```python
# Dummy chatbot reply
reply = f"Hey {msg.user_id}, I hear you. Stay strong ❤️"
```

### 3. **Chat History Storage**
```python
chat_doc = {
    "user_id": msg.user_id,
    "message": msg.message,
    "bot_reply": reply,
    "timestamp": datetime.utcnow()
}
safe_db_operation(chat_collection.insert_one, chat_doc)
```

## Data Validation

### 1. **Message Validation**
```python
class ChatMessage(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User ID must be between 1-50 characters")
    message: str = Field(..., min_length=1, max_length=1000, description="Message must be between 1-1000 characters")
```

### 2. **User ID Validation**
```python
@validator('user_id')
def validate_user_id(cls, v):
    if not re.match(r'^[a-zA-Z0-9_-]+$', v):
        raise ValueError('User ID can only contain letters, numbers, underscores, and hyphens')
    return v
```

## Security Features

### 1. **Authentication Required**
- All endpoints require valid JWT tokens
- Users must be logged in to chat or view history
- Automatic token validation

### 2. **User Isolation**
- Users can only chat for themselves
- Users can only view their own chat history
- Database queries filter by authenticated user

### 3. **Input Validation**
- Message length is limited (1-1000 characters)
- User IDs are validated for format
- Prevents extremely long messages

### 4. **Error Handling**
- Comprehensive error handling for all scenarios
- Clear error messages for validation failures
- Database error handling

## Error Responses

### 1. **Validation Errors**
```json
// Message too long
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "message",
            "message": "Message must be between 1-1000 characters",
            "type": "value_error"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}

// Empty message
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "message",
            "message": "Message must be between 1-1000 characters",
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
    "detail": "You can only access your own chat history",
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

### 1. **Sending a Message**
```bash
# Send a message to the chatbot
curl -X POST "http://localhost:8000/chatbot/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{
       "user_id": "john_doe",
       "message": "I'm feeling really stressed today"
     }'
```

### 2. **Getting Chat History**
```bash
# Get chat history for a user
curl -X GET "http://localhost:8000/chatbot/john_doe" \
     -H "Authorization: Bearer <jwt_token>"
```

### 3. **Using in Applications**
```python
import requests

# Set up authentication
headers = {"Authorization": f"Bearer {jwt_token}"}

# Send a message
message_data = {
    "user_id": "john_doe",
    "message": "How can I manage my anxiety?"
}
response = requests.post("http://localhost:8000/chatbot/", json=message_data, headers=headers)
chat_response = response.json()
print(f"Bot: {chat_response['bot']}")

# Get chat history
response = requests.get("http://localhost:8000/chatbot/john_doe", headers=headers)
chat_history = response.json()
print(f"User has {chat_history['count']} chat messages")
```

## Database Structure

### Chats Collection
```json
{
    "_id": "ObjectId",
    "user_id": "string",
    "message": "string",
    "bot_reply": "string",
    "timestamp": "datetime"
}
```

### Indexes
- **user_id**: For fast user-specific queries
- **(user_id, timestamp)**: For sorted chat history

## Current Limitations

### 1. **Basic Responses**
- Currently provides simple, generic responses
- No context awareness or conversation memory
- No AI-powered analysis

### 2. **No Advanced Features**
- No emotion detection
- No sentiment analysis
- No personalized responses

### 3. **Simple Logic**
- Static response generation
- No conversation flow management
- No topic-specific responses

## Future Enhancements

### 1. **AI Integration**
- Connect to advanced chatbot with AI analysis
- Emotion detection and sentiment analysis
- Personalized responses based on user context

### 2. **Conversation Memory**
- Remember previous conversations
- Context-aware responses
- Topic continuity

### 3. **Advanced Features**
- Crisis detection and intervention
- Mental health resource recommendations
- Mood-based response adaptation

## Integration with Other Features

### 1. **Advanced Chatbot**
The basic chatbot can be enhanced by integrating with the advanced chatbot in `nlp.py`:
- AI-powered responses
- Emotion analysis
- Crisis detection

### 2. **Mood Tracking**
Chat data can be used for:
- Mood pattern analysis
- Emotional context tracking
- Risk assessment

### 3. **Gamification**
Chat interactions can contribute to:
- Engagement tracking
- Streak maintenance
- Progress monitoring

## Why This Structure Matters

### 1. **Foundation**
- Provides basic chat functionality
- Establishes conversation data structure
- Enables future AI enhancements

### 2. **User Experience**
- Simple chat interface
- Conversation history
- Consistent responses

### 3. **Data Collection**
- Stores conversation data
- Enables analysis and insights
- Supports future AI training

### 4. **Scalability**
- Easy to enhance with AI features
- Modular design for upgrades
- Clear separation of concerns

This basic chatbot system provides a foundation for user interaction while maintaining security and data integrity. It can be easily enhanced with AI capabilities for more sophisticated mental health support.