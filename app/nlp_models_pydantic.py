"""
Pydantic Models for NLP Services
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Base text input
class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")

# Sentiment Analysis
class SentimentResponse(BaseModel):
    label: str = Field(..., description="Sentiment label (positive/negative/neutral)")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    confidence: str = Field(..., description="Confidence level (high/medium/low)")

# Emotion Analysis
class EmotionResponse(BaseModel):
    label: str = Field(..., description="Emotion label")
    score: float = Field(..., ge=0, le=1, description="Confidence score")
    confidence: str = Field(..., description="Confidence level (high/medium/low)")

# Toxicity Detection
class ToxicityResponse(BaseModel):
    toxic: float = Field(..., ge=0, le=1, description="Toxicity probability")
    level: str = Field(..., description="Toxicity level (high/medium/low)")
    safe: bool = Field(..., description="Whether the text is safe")

# Distress Detection
class DistressResponse(BaseModel):
    is_urgent: bool = Field(..., description="Whether urgent intervention is needed")
    reason: str = Field(..., description="Reason for the assessment")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in assessment")
    recommendation: str = Field(..., description="Recommended action")

# Risk Assessment
class RiskScoreResponse(BaseModel):
    risk_score: float = Field(..., ge=0, le=1, description="Overall risk score")
    level: str = Field(..., description="Risk level (high/medium/low)")
    advice: str = Field(..., description="General advice")
    recommendations: List[str] = Field(..., description="Specific recommendations")
    sentiment_risk: Optional[float] = Field(None, description="Sentiment-based risk score")
    emotion_risk: Optional[float] = Field(None, description="Emotion-based risk score")

# Chatbot
class ChatRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User identifier")
    message: str = Field(..., min_length=1, max_length=1000, description="User message")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Chatbot response")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Message analysis results")

# History requests
class SentimentHistoryRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User identifier")
    sentiments: List[str] = Field(..., description="List of sentiment labels")

class EmotionHistoryRequest(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=50, description="User identifier")
    emotions: List[str] = Field(..., description="List of emotion labels")

# Comprehensive Analysis
class ComprehensiveAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to analyze")
    user_id: Optional[str] = Field(None, description="User identifier for context")

class ComprehensiveAnalysisResponse(BaseModel):
    sentiment: SentimentResponse
    emotion: EmotionResponse
    toxicity: ToxicityResponse
    distress: DistressResponse
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: Optional[str] = None

# Conversation History
class ConversationHistoryResponse(BaseModel):
    user_id: str
    conversations: List[Dict[str, Any]]
    total_count: int
    latest_analysis: Optional[Dict[str, Any]] = None
