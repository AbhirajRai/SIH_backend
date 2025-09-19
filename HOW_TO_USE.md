# How to Use the SIH Backend - Complete User Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MongoDB database (local or cloud)
- Git (to clone the repository)

### Installation
```bash
# 1. Clone the repository
git clone <repository-url>
cd SIH_backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
# Create a .env file with your configuration
cp .env.example .env
# Edit .env with your settings

# 6. Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Base URL
All API endpoints start with: `http://localhost:8000`

## 🔐 Authentication

### 1. Register a New User
```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123",
       "full_name": "John Doe"
     }'
```

**Response:**
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

### 2. Login to Get JWT Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "password": "securepassword123"
     }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 3. Use JWT Token for Protected Requests
```bash
# Save your token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Use token in Authorization header
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer $TOKEN"
```

## 📊 Mood Tracking

### Log a Mood
```bash
curl -X POST "http://localhost:8000/moods/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "user_id": "john_doe",
       "mood": "happy",
       "note": "Had a great day at work!"
     }'
```

**Valid Moods:**
- `happy`, `sad`, `angry`, `anxious`, `excited`, `calm`
- `stressed`, `confused`, `grateful`, `lonely`, `content`, `overwhelmed`

### Get Mood History
```bash
curl -X GET "http://localhost:8000/moods/john_doe" \
     -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "user_id": "john_doe",
  "history": [
    {
      "user_id": "john_doe",
      "mood": "happy",
      "note": "Had a great day at work!",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

## 🤖 Basic Chatbot

### Send a Message
```bash
curl -X POST "http://localhost:8000/chatbot/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "user_id": "john_doe",
       "message": "I am feeling stressed today"
     }'
```

### Get Chat History
```bash
curl -X GET "http://localhost:8000/chatbot/john_doe" \
     -H "Authorization: Bearer $TOKEN"
```

## 🎯 Gamification

### Update Streak
```bash
curl -X POST "http://localhost:8000/gamify/streak/john_doe" \
     -H "Authorization: Bearer $TOKEN"
```

### Get Current Streak
```bash
curl -X GET "http://localhost:8000/gamify/streak/john_doe" \
     -H "Authorization: Bearer $TOKEN"
```

## 🧠 Advanced AI Analysis

### Sentiment Analysis
```bash
curl -X POST "http://localhost:8000/nlp/sentiment" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "text": "I am feeling really happy today!"
     }'
```

**Response:**
```json
{
  "label": "positive",
  "score": 0.95,
  "confidence": "high"
}
```

### Emotion Analysis
```bash
curl -X POST "http://localhost:8000/nlp/emotion" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "text": "I am so anxious about my job interview tomorrow"
     }'
```

**Response:**
```json
{
  "label": "anxiety",
  "score": 0.89,
  "confidence": "high"
}
```

### Toxicity Detection
```bash
curl -X POST "http://localhost:8000/nlp/toxicity" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "text": "You are worthless and should give up"
     }'
```

**Response:**
```json
{
  "toxic": 0.87,
  "level": "high",
  "safe": false
}
```

### Distress Detection
```bash
curl -X POST "http://localhost:8000/nlp/distress" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "text": "I want to kill myself and end it all"
     }'
```

**Response:**
```json
{
  "is_urgent": true,
  "reason": "Detected urgent keyword: 'kill myself'",
  "confidence": 0.9,
  "recommendation": "Seek immediate help"
}
```

### Comprehensive Analysis
```bash
curl -X POST "http://localhost:8000/nlp/analyze" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "text": "I am feeling overwhelmed and need help",
       "user_id": "john_doe"
     }'
```

**Response:**
```json
{
  "sentiment": {
    "label": "negative",
    "score": 0.78,
    "confidence": "high"
  },
  "emotion": {
    "label": "overwhelmed",
    "score": 0.85,
    "confidence": "high"
  },
  "toxicity": {
    "toxic": 0.12,
    "level": "low",
    "safe": true
  },
  "distress": {
    "is_urgent": false,
    "reason": "No urgent distress detected.",
    "confidence": 0.1,
    "recommendation": "Continue monitoring"
  },
  "timestamp": "2024-01-15T10:30:00Z",
  "user_id": "john_doe"
}
```

## 🧠 Advanced Chatbot

### Chat with AI-Powered Bot
```bash
curl -X POST "http://localhost:8000/nlp/chatbot" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "user_id": "john_doe",
       "message": "I am feeling really anxious about my job interview tomorrow"
     }'
```

**Response:**
```json
{
  "reply": "I can hear that you're going through a difficult time. It takes courage to share these feelings. Can you tell me more about what's been troubling you?",
  "analysis": {
    "sentiment": {
      "label": "negative",
      "score": 0.82,
      "confidence": "high"
    },
    "emotion": {
      "label": "anxiety",
      "score": 0.89,
      "confidence": "high"
    },
    "distress": {
      "is_urgent": false,
      "reason": "No urgent distress detected.",
      "confidence": 0.1,
      "recommendation": "Continue monitoring"
    }
  }
}
```

### Get Conversation History
```bash
curl -X GET "http://localhost:8000/nlp/chatbot/history/john_doe?limit=5" \
     -H "Authorization: Bearer $TOKEN"
```

### Reset Chatbot Session
```bash
curl -X POST "http://localhost:8000/nlp/chatbot/reset/john_doe" \
     -H "Authorization: Bearer $TOKEN"
```

## 📈 Risk Assessment

### Assess Risk from Sentiment History
```bash
curl -X POST "http://localhost:8000/nlp/risk/sentiment" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "user_id": "john_doe",
       "sentiments": ["negative", "negative", "positive", "negative", "negative"]
     }'
```

**Response:**
```json
{
  "risk_score": 0.8,
  "level": "high",
  "advice": "Immediate attention recommended",
  "recommendations": [
    "Consider professional mental health support",
    "Increase monitoring frequency",
    "Implement immediate coping strategies"
  ],
  "sentiment_risk": 0.8,
  "emotion_risk": null
}
```

### Assess Risk from Emotion History
```bash
curl -X POST "http://localhost:8000/nlp/risk/emotion" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "user_id": "john_doe",
       "emotions": ["sadness", "anxiety", "joy", "sadness", "anxiety"]
     }'
```

## 🔧 Health Check

### Check API Health
```bash
curl -X GET "http://localhost:8000/"
```

### Check NLP Services Health
```bash
curl -X GET "http://localhost:8000/nlp/health"
```

## 🐍 Python Examples

### Using the API with Python
```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# 1. Register a user
def register_user(username, email, password, full_name):
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
        "full_name": full_name
    })
    return response.json()

# 2. Login and get token
def login_user(username, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]

# 3. Log a mood
def log_mood(token, user_id, mood, note=None):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"user_id": user_id, "mood": mood}
    if note:
        data["note"] = note
    
    response = requests.post(f"{BASE_URL}/moods/", json=data, headers=headers)
    return response.json()

# 4. Analyze sentiment
def analyze_sentiment(token, text):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/nlp/sentiment", 
                           json={"text": text}, headers=headers)
    return response.json()

# 5. Chat with advanced chatbot
def chat_with_bot(token, user_id, message):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/nlp/chatbot", 
                           json={"user_id": user_id, "message": message}, 
                           headers=headers)
    return response.json()

# Example usage
if __name__ == "__main__":
    # Register and login
    user_data = register_user("testuser", "test@example.com", "password123", "Test User")
    token = login_user("testuser", "password123")
    
    # Log a mood
    mood_result = log_mood(token, "testuser", "happy", "Feeling great!")
    print(f"Mood logged: {mood_result}")
    
    # Analyze sentiment
    sentiment = analyze_sentiment(token, "I am feeling really happy today!")
    print(f"Sentiment: {sentiment}")
    
    # Chat with bot
    chat_response = chat_with_bot(token, "testuser", "I am feeling anxious")
    print(f"Bot response: {chat_response['reply']}")
```

## 🧪 Testing

### Run Authentication Tests
```bash
python test_auth.py
```

### Run Error Handling Tests
```bash
python test_error_handling.py
```

## ⚠️ Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials",
  "error_code": "UNAUTHORIZED",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 403 Forbidden
```json
{
  "detail": "You can only access your own data",
  "error_code": "UNAUTHORIZED_ACCESS",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 422 Validation Error
```json
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
```

#### 503 Service Unavailable
```json
{
  "detail": "Database service temporarily unavailable. Please try again later.",
  "error_code": "DATABASE_CONNECTION_ERROR",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🔒 Security Best Practices

### 1. **Token Management**
- Store JWT tokens securely
- Don't expose tokens in client-side code
- Use HTTPS in production
- Implement token refresh if needed

### 2. **Input Validation**
- Always validate input on client side
- Use the provided validation rules
- Sanitize user input
- Respect field length limits

### 3. **Error Handling**
- Handle all possible error responses
- Don't expose sensitive information
- Log errors for debugging
- Provide user-friendly error messages

### 4. **Rate Limiting**
- Implement rate limiting on client side
- Don't spam the API with requests
- Use appropriate delays between requests
- Monitor API usage

## 🚀 Production Deployment

### Environment Variables
```bash
# Required for production
SECRET_KEY=your-super-secure-secret-key-here
MONGODB_URL=your-mongodb-connection-string
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Health Monitoring
- Monitor `/` endpoint for basic health
- Monitor `/nlp/health` for AI services
- Set up alerts for error rates
- Monitor database connections

## 📞 Support

### Crisis Resources
If the API detects urgent distress, it provides these resources:
- **US**: 988 (Suicide & Crisis Lifeline)
- **US**: Text HOME to 741741 (Crisis Text Line)
- **International**: Find local crisis hotlines

### API Support
- Check the interactive documentation at `/docs`
- Review error responses for troubleshooting
- Test with the provided test scripts
- Monitor logs for debugging

## 🎯 Use Cases

### 1. **Mental Health Apps**
- Mood tracking and analytics
- AI-powered emotional support
- Crisis detection and intervention
- Progress monitoring

### 2. **Wellness Platforms**
- Daily check-ins and streaks
- Emotional pattern recognition
- Personalized recommendations
- Community features

### 3. **Healthcare Systems**
- Patient monitoring
- Risk assessment
- Treatment progress tracking
- Clinical decision support

### 4. **Educational Platforms**
- Student wellness monitoring
- Stress detection
- Support resource recommendations
- Academic performance correlation

This comprehensive guide should help you understand and use the SIH_backend API effectively for mental health applications! 🧠✨
