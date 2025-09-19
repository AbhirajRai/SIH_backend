# nlp_models_pydantic.py - AI Analysis Data Models

## What This File Does
This file defines all the data models (schemas) used for AI analysis requests and responses. It's like the "blueprint" that describes what data the AI analysis endpoints expect and what they return.

## In Simple Terms
Think of this as the instruction manual that tells the API what information to expect when someone wants to analyze text, and what format to return the analysis results in.

## Data Models Explained

### 1. **TextRequest Model**
```python
class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")
```
**What it does:** Defines the input for text analysis requests
**Fields:** 
- `text`: The text to analyze (1-1000 characters)
**Used for:** Sentiment analysis, emotion analysis, toxicity detection, distress detection

### 2. **SentimentResponse Model**
```python
class SentimentResponse(BaseModel):
    label: str = Field(..., description="Sentiment label (positive/negative/neutral)")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    confidence: str = Field(..., description="Confidence level (high/medium/low)")
```
**What it does:** Defines the response format for sentiment analysis
**Fields:**
- `label`: The sentiment (positive, negative, or neutral)
- `score`: Confidence score (0-1, where 1 is most confident)
- `confidence`: Confidence level (high, medium, or low)

### 3. **EmotionResponse Model**
```python
class EmotionResponse(BaseModel):
    label: str = Field(..., description="Emotion label")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    confidence: str = Field(..., description="Confidence level (high/medium/low)")
```
**What it does:** Defines the response format for emotion analysis
**Fields:**
- `label`: The detected emotion (anxiety, sadness, joy, anger, etc.)
- `score`: Confidence score (0-1)
- `confidence`: Confidence level (high, medium, or low)

### 4. **ToxicityResponse Model**
```python
class ToxicityResponse(BaseModel):
    toxic: float = Field(..., ge=0, le=1, description="Toxicity probability")
    level: str = Field(..., description="Toxicity level (high/medium/low)")
    safe: bool = Field(..., description="Whether the text is safe")
```
**What it does:** Defines the response format for toxicity detection
**Fields:**
- `toxic`: Probability of toxicity (0-1)
- `level`: Toxicity level (high, medium, or low)
- `safe`: Boolean indicating if text is safe

### 5. **DistressResponse Model**
```python
class DistressResponse(BaseModel):
    is_urgent: bool = Field(..., description="Whether urgent intervention is needed")
    reason: str = Field(..., description="Reason for the assessment")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in assessment")
    recommendation: str = Field(..., description="Recommended action")
```
**What it does:** Defines the response format for distress detection
**Fields:**
- `is_urgent`: Whether immediate intervention is needed
- `reason`: Explanation of why distress was detected
- `confidence`: Confidence in the assessment (0-1)
- `recommendation`: Suggested action (e.g., "Seek immediate help")

### 6. **RiskScoreResponse Model**
```python
class RiskScoreResponse(BaseModel):
    risk_score: float = Field(..., ge=0, le=1, description="Overall risk score")
    level: str = Field(..., description="Risk level (high/medium/low)")
    advice: str = Field(..., description="General advice")
    recommendations: List[str] = Field(..., description="Specific recommendations")
    sentiment_risk: Optional[float] = Field(None, description="Sentiment-based risk score")
    emotion_risk: Optional[float] = Field(None, description="Emotion-based risk score")
```
**What it does:** Defines the response format for risk assessment
**Fields:**
- `risk_score`: Overall risk score (0-1)
- `level`: Risk level (high, medium, or low)
- `advice`: General advice based on risk level
- `recommendations`: Specific actionable recommendations
- `sentiment_risk`: Risk score based on sentiment history
- `emotion_risk`: Risk score based on emotion history

### 7. **ChatRequest Model**
```python
class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User identifier")
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
```
**What it does:** Defines the input for chatbot interactions
**Fields:**
- `user_id`: User identifier (1-50 characters)
- `message`: The message to send to the chatbot (1-1000 characters)

### 8. **ChatResponse Model**
```python
class ChatResponse(BaseModel):
    reply: str = Field(..., description="Chatbot response")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Message analysis results")
```
**What it does:** Defines the response format for chatbot interactions
**Fields:**
- `reply`: The chatbot's response message
- `analysis`: Optional analysis results (sentiment, emotion, distress)

### 9. **ComprehensiveAnalysisRequest Model**
```python
class ComprehensiveAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")
    user_id: Optional[str] = Field(None, description="User identifier for context")
```
**What it does:** Defines the input for comprehensive analysis
**Fields:**
- `text`: The text to analyze (1-1000 characters)
- `user_id`: Optional user identifier for context

### 10. **ComprehensiveAnalysisResponse Model**
```python
class ComprehensiveAnalysisResponse(BaseModel):
    sentiment: SentimentResponse
    emotion: EmotionResponse
    toxicity: ToxicityResponse
    distress: DistressResponse
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None
```
**What it does:** Defines the response format for comprehensive analysis
**Fields:**
- `sentiment`: Sentiment analysis results
- `emotion`: Emotion analysis results
- `toxicity`: Toxicity detection results
- `distress`: Distress detection results
- `timestamp`: When the analysis was performed
- `user_id`: User identifier (if provided)

### 11. **ConversationHistoryResponse Model**
```python
class ConversationHistoryResponse(BaseModel):
    user_id: str
    conversations: List[Dict[str, Any]]
    total_count: int
    latest_analysis: Optional[Dict[str, Any]] = None
```
**What it does:** Defines the response format for conversation history
**Fields:**
- `user_id`: User identifier
- `conversations`: List of conversation records
- `total_count`: Total number of conversations
- `latest_analysis`: Analysis results from the most recent conversation

## How These Models Work

### 1. **Input Validation**
```python
# When a client sends data, Pydantic automatically validates it
request = TextRequest(text="I am feeling great today!")
# This will validate that text is 1-1000 characters and is a string
```

### 2. **Response Formatting**
```python
# When returning data, Pydantic ensures consistent format
response = SentimentResponse(
    label="positive",
    score=0.95,
    confidence="high"
)
# This ensures all responses have the same structure
```

### 3. **API Documentation**
```python
# FastAPI automatically generates documentation from these models
# Shows clients exactly what data to send and what to expect
```

## Field Validation

### 1. **String Length Validation**
```python
text: str = Field(..., min_length=1, max_length=1000)
# Ensures text is between 1 and 1000 characters
```

### 2. **Numeric Range Validation**
```python
score: float = Field(..., ge=0, le=1)
# Ensures score is between 0 and 1 (inclusive)
```

### 3. **Optional Fields**
```python
user_id: Optional[str] = Field(None, description="User identifier for context")
# Field is optional and defaults to None
```

### 4. **List Validation**
```python
recommendations: List[str] = Field(..., description="Specific recommendations")
# Ensures recommendations is a list of strings
```

## Usage Examples

### 1. **Sentiment Analysis Request**
```python
# Client sends this data
{
    "text": "I am feeling really happy today!"
}

# Server returns this response
{
    "label": "positive",
    "score": 0.92,
    "confidence": "high"
}
```

### 2. **Comprehensive Analysis Request**
```python
# Client sends this data
{
    "text": "I am feeling overwhelmed and need help",
    "user_id": "john_doe"
}

# Server returns this response
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

### 3. **Chatbot Interaction Request**
```python
# Client sends this data
{
    "user_id": "john_doe",
    "message": "I am feeling anxious about my job interview"
}

# Server returns this response
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

## Error Handling

### 1. **Validation Errors**
```python
# If client sends invalid data
{
    "text": ""  # Empty text (violates min_length=1)
}

# Server returns validation error
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

### 2. **Type Errors**
```python
# If client sends wrong data type
{
    "text": 123  # Number instead of string
}

# Server returns type error
{
    "detail": "Validation error",
    "errors": [
        {
            "field": "text",
            "message": "Input should be a valid string",
            "type": "type_error.str"
        }
    ],
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Why This Structure Matters

### 1. **Data Consistency**
- All AI analysis responses follow the same format
- Consistent field names and types
- Predictable data structure

### 2. **Input Validation**
- Prevents invalid data from reaching AI models
- Clear error messages for validation failures
- Protects against malicious input

### 3. **API Documentation**
- Automatic generation of API documentation
- Clear examples for clients
- Interactive testing interface

### 4. **Type Safety**
- Ensures data types are correct
- Prevents type-related errors
- Improves code reliability

### 5. **Maintainability**
- Centralized data model definitions
- Easy to modify response formats
- Clear separation of concerns

This models file provides a robust foundation for AI analysis data validation and response formatting, ensuring that all AI analysis endpoints have consistent, validated, and well-documented data structures.
