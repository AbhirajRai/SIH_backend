# nlp.py - Advanced AI Analysis and Mental Health Detection Routes

## What This File Does
This file defines API endpoints for advanced AI-powered mental health analysis. It provides sophisticated text analysis, emotion detection, crisis intervention, and an intelligent chatbot with conversation memory.

## In Simple Terms
Think of this as the "AI brain" of the mental health app that can understand emotions, detect crisis situations, analyze patterns over time, and provide intelligent responses. It's like having a mental health professional who can analyze text and provide insights.

## API Endpoints

### 1. **POST /nlp/sentiment** - Sentiment Analysis
```python
@router.post("/sentiment", response_model=SentimentResponse)
async def sentiment_analysis(request: TextRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Analyzes text to determine if it's positive, negative, or neutral
**Input:** Text to analyze
**Output:** Sentiment label, confidence score, and confidence level
**Security:** Requires JWT authentication

**Example Request:**
```json
{
    "text": "I'm feeling really down today and nothing seems to be going right"
}
```

**Example Response:**
```json
{
    "label": "negative",
    "score": 0.89,
    "confidence": "high"
}
```

### 2. **POST /nlp/emotion** - Emotion Analysis
```python
@router.post("/emotion", response_model=EmotionResponse)
async def emotion_analysis(request: TextRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Identifies specific emotions in text
**Input:** Text to analyze
**Output:** Emotion label, confidence score, and confidence level
**Security:** Requires JWT authentication

**Example Request:**
```json
{
    "text": "I'm so anxious about the presentation tomorrow"
}
```

**Example Response:**
```json
{
    "label": "anxiety",
    "score": 0.92,
    "confidence": "high"
}
```

### 3. **POST /nlp/toxicity** - Toxicity Detection
```python
@router.post("/toxicity", response_model=ToxicityResponse)
async def toxicity_analysis(request: TextRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Detects harmful, offensive, or toxic content
**Input:** Text to analyze
**Output:** Toxicity probability, level, and safety status
**Security:** Requires JWT authentication

**Example Request:**
```json
{
    "text": "You're worthless and should just give up"
}
```

**Example Response:**
```json
{
    "toxic": 0.87,
    "level": "high",
    "safe": false
}
```

### 4. **POST /nlp/distress** - Distress Detection
```python
@router.post("/distress", response_model=DistressResponse)
async def distress_analysis(request: TextRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Identifies if someone is in immediate danger or crisis
**Input:** Text to analyze
**Output:** Urgency status, reason, confidence, and recommendation
**Security:** Requires JWT authentication

**Example Request:**
```json
{
    "text": "I want to kill myself and end it all"
}
```

**Example Response:**
```json
{
    "is_urgent": true,
    "reason": "Detected urgent keyword: 'kill myself'",
    "confidence": 0.9,
    "recommendation": "Seek immediate help"
}
```

### 5. **POST /nlp/analyze** - Comprehensive Analysis
```python
@router.post("/analyze", response_model=ComprehensiveAnalysisResponse)
async def comprehensive_analysis(request: ComprehensiveAnalysisRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Performs all AI analyses in one request
**Input:** Text to analyze and optional user ID
**Output:** Complete analysis including sentiment, emotion, toxicity, and distress
**Security:** Requires JWT authentication

**Example Request:**
```json
{
    "text": "I'm feeling really overwhelmed and don't know what to do",
    "user_id": "john_doe"
}
```

**Example Response:**
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

### 6. **POST /nlp/chatbot** - Advanced Chatbot
```python
@router.post("/chatbot", response_model=ChatResponse)
async def chatbot_interaction(request: ChatRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Interacts with the advanced mental health chatbot
**Input:** User ID and message
**Output:** Bot response and analysis results
**Security:** Requires JWT authentication, user can only chat for themselves

**Example Request:**
```json
{
    "user_id": "john_doe",
    "message": "I'm feeling really anxious about my job interview tomorrow"
}
```

**Example Response:**
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

### 7. **POST /nlp/risk/sentiment** - Risk Assessment from Sentiment
```python
@router.post("/risk/sentiment", response_model=RiskScoreResponse)
async def risk_assessment_sentiment(request: SentimentHistoryRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Calculates mental health risk based on sentiment history
**Input:** User ID and list of past sentiments
**Output:** Risk score, level, advice, and recommendations
**Security:** Requires JWT authentication, user can only access their own data

**Example Request:**
```json
{
    "user_id": "john_doe",
    "sentiments": ["negative", "negative", "positive", "negative", "negative"]
}
```

**Example Response:**
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

### 8. **POST /nlp/risk/emotion** - Risk Assessment from Emotions
```python
@router.post("/risk/emotion", response_model=RiskScoreResponse)
async def risk_assessment_emotion(request: EmotionHistoryRequest, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Calculates mental health risk based on emotion history
**Input:** User ID and list of past emotions
**Output:** Risk score, level, advice, and recommendations
**Security:** Requires JWT authentication, user can only access their own data

**Example Request:**
```json
{
    "user_id": "john_doe",
    "emotions": ["sadness", "anxiety", "joy", "sadness", "anxiety"]
}
```

**Example Response:**
```json
{
    "risk_score": 0.6,
    "level": "medium",
    "advice": "Monitor closely and consider intervention",
    "recommendations": [
        "Schedule regular check-ins",
        "Practice stress management techniques",
        "Consider talking to a counselor"
    ],
    "sentiment_risk": null,
    "emotion_risk": 0.6
}
```

### 9. **GET /nlp/chatbot/history/{user_id}** - Get Conversation History
```python
@router.get("/chatbot/history/{user_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(user_id: str, limit: int = 10, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Retrieves conversation history with the advanced chatbot
**Input:** User ID and optional limit
**Output:** List of conversations with analysis results
**Security:** Requires JWT authentication, user can only access their own history

**Example Request:**
```
GET /nlp/chatbot/history/john_doe?limit=5
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "user_id": "john_doe",
    "conversations": [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "user_message": "I'm feeling really anxious about my job interview tomorrow",
            "bot_response": "I can hear that you're going through a difficult time...",
            "analysis": {
                "sentiment": {"label": "negative", "score": 0.82, "confidence": "high"},
                "emotion": {"label": "anxiety", "score": 0.89, "confidence": "high"},
                "distress": {"is_urgent": false, "reason": "No urgent distress detected.", "confidence": 0.1, "recommendation": "Continue monitoring"}
            }
        }
    ],
    "total_count": 1,
    "latest_analysis": {
        "sentiment": {"label": "negative", "score": 0.82, "confidence": "high"},
        "emotion": {"label": "anxiety", "score": 0.89, "confidence": "high"},
        "distress": {"is_urgent": false, "reason": "No urgent distress detected.", "confidence": 0.1, "recommendation": "Continue monitoring"}
    }
}
```

### 10. **POST /nlp/chatbot/reset/{user_id}** - Reset Chatbot Session
```python
@router.post("/chatbot/reset/{user_id}")
async def reset_chatbot_session(user_id: str, current_user: User = Depends(get_current_active_user)):
```
**What it does:** Resets the chatbot conversation session for a user
**Input:** User ID in URL path
**Output:** Confirmation message
**Security:** Requires JWT authentication, user can only reset their own session

**Example Request:**
```
POST /nlp/chatbot/reset/john_doe
Authorization: Bearer <jwt_token>
```

**Example Response:**
```json
{
    "message": "Chatbot session reset successfully",
    "user_id": "john_doe"
}
```

### 11. **GET /nlp/health** - Health Check
```python
@router.get("/health")
async def nlp_health_check():
```
**What it does:** Checks if NLP services are working properly
**Input:** None
**Output:** Service status and health information
**Security:** No authentication required (public endpoint)

**Example Request:**
```
GET /nlp/health
```

**Example Response:**
```json
{
    "status": "healthy",
    "services": {
        "sentiment_analysis": "working",
        "emotion_analysis": "working",
        "chatbot": "working"
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## How AI Analysis Works

### 1. **Sentiment Analysis Process**
```
Text input → AI model → Sentiment classification → Confidence scoring → Response
```

### 2. **Emotion Analysis Process**
```
Text input → AI model → Emotion identification → Confidence scoring → Response
```

### 3. **Toxicity Detection Process**
```
Text input → AI model → Toxicity probability → Level classification → Safety assessment
```

### 4. **Distress Detection Process**
```
Text input → Keyword check → AI analysis → Urgency assessment → Recommendation
```

### 5. **Risk Assessment Process**
```
Historical data → Pattern analysis → Risk calculation → Level determination → Recommendations
```

## Advanced Chatbot Features

### 1. **Conversation Memory**
- Remembers previous conversations
- Maintains context across messages
- Tracks conversation state

### 2. **Emotional Intelligence**
- Analyzes user emotions in real-time
- Adapts responses based on emotional state
- Provides empathetic responses

### 3. **Crisis Intervention**
- Detects urgent distress situations
- Provides immediate crisis resources
- Escalates serious concerns

### 4. **State Management**
- Tracks conversation flow
- Manages different conversation states
- Provides context-aware responses

## Security Features

### 1. **Authentication Required**
- All endpoints require valid JWT tokens
- Users must be logged in to use AI features
- Automatic token validation

### 2. **User Isolation**
- Users can only access their own data
- AI analysis is user-specific
- No cross-user data access

### 3. **Input Validation**
- Text length limits (1-1000 characters)
- User ID validation
- Prevents malicious input

### 4. **Error Handling**
- Comprehensive error handling for all scenarios
- Clear error messages for failures
- Database error handling

## Error Responses

### 1. **Validation Errors**
```json
// Text too long
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "text",
            "message": "Text must be between 1-1000 characters",
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
    "detail": "You can only access your own data",
    "error_code": "UNAUTHORIZED_ACCESS",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. **Service Errors**
```json
// AI analysis failure
{
    "detail": "Sentiment analysis failed: Model not available",
    "error_code": "SERVICE_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Usage Examples

### 1. **Basic Sentiment Analysis**
```bash
curl -X POST "http://localhost:8000/nlp/sentiment" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{"text": "I am feeling great today!"}'
```

### 2. **Comprehensive Analysis**
```bash
curl -X POST "http://localhost:8000/nlp/analyze" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{"text": "I am feeling overwhelmed and need help"}'
```

### 3. **Advanced Chatbot Interaction**
```bash
curl -X POST "http://localhost:8000/nlp/chatbot" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{"user_id": "john_doe", "message": "I am feeling really anxious"}'
```

### 4. **Risk Assessment**
```bash
curl -X POST "http://localhost:8000/nlp/risk/sentiment" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <jwt_token>" \
     -d '{"user_id": "john_doe", "sentiments": ["negative", "negative", "positive"]}'
```

## Integration with Other Features

### 1. **Mood Tracking Integration**
- AI analysis of mood notes
- Sentiment tracking over time
- Emotional pattern recognition

### 2. **Basic Chatbot Enhancement**
- Advanced responses based on AI analysis
- Emotion-aware conversations
- Crisis detection and intervention

### 3. **Gamification Integration**
- AI-powered engagement tracking
- Personalized recommendations
- Progress insights

## Why This Structure Matters

### 1. **Mental Health Support**
- Advanced AI analysis for mental health insights
- Crisis detection and intervention
- Personalized support recommendations

### 2. **User Experience**
- Intelligent chatbot with conversation memory
- Real-time emotional analysis
- Comprehensive mental health insights

### 3. **Data Insights**
- Pattern recognition over time
- Risk assessment and early intervention
- Personalized mental health analytics

### 4. **Scalability**
- Modular AI analysis components
- Easy to add new AI features
- Clear separation of concerns

This advanced NLP system provides sophisticated AI-powered mental health analysis, crisis intervention, and intelligent chatbot capabilities while maintaining security and user data isolation.
