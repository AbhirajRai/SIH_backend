from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


# Text input for general NLP endpoints
class TextRequest(BaseModel):
    text: str


# Sentiment analysis response
class SentimentResponse(BaseModel):
    label: str
    score: float


# Toxicity detection response
class ToxicityResponse(BaseModel):
    toxic: float


# Emotion detection response
class EmotionResponse(BaseModel):
    label: str
    score: float


# Chatbot request and response
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str


# Distress detection response
class DistressResponse(BaseModel):
    is_urgent: bool
    reason: str


# Mood tracking request and responses
class MoodLogRequest(BaseModel):
    user_id: str
    mood_rating: int  # e.g., scale 1-5
    note: Optional[str] = None

class MoodLogResponse(BaseModel):
    user_id: str
    mood_rating: int
    note: Optional[str] = None
    timestamp: datetime

class MoodTrendResponse(BaseModel):
    date: str  # YYYY-MM-DD
    average_mood: float


# Risk scoring for sentiment and emotion histories
class SentimentHistoryRequest(BaseModel):
    user_id: str
    sentiments: List[str]  # e.g., ["positive", "negative", "negative", ...]

class EmotionHistoryRequest(BaseModel):
    user_id: str
    emotions: List[str]  # e.g., ["joy", "sadness", "sadness", ...]

class RiskScoreResponse(BaseModel):
    risk_score: float
    advice: str
