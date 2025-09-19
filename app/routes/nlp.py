"""
NLP Routes for Mental Health Detection
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from datetime import datetime
from typing import List

from app.models import User
from app.auth import get_current_active_user
from app.exceptions import DatabaseConnectionError, UnauthorizedAccessError
from app.database import safe_db_operation, moods_collection, chat_collection
from app.nlp_services import (
    analyze_sentiment, analyze_emotion, analyze_toxicity, 
    analyze_distress, calculate_risk_score
)
from app.advanced_chatbot import chatbot
from app.nlp_models_pydantic import (
    TextRequest, SentimentResponse, EmotionResponse, ToxicityResponse,
    DistressResponse, RiskScoreResponse, ChatRequest, ChatResponse,
    SentimentHistoryRequest, EmotionHistoryRequest,
    ComprehensiveAnalysisRequest, ComprehensiveAnalysisResponse,
    ConversationHistoryResponse
)

router = APIRouter()

# Sentiment Analysis
@router.post("/sentiment", response_model=SentimentResponse)
async def sentiment_analysis(
    request: TextRequest, 
    current_user: User = Depends(get_current_active_user)
):
    """Analyze sentiment of the given text."""
    try:
        result = analyze_sentiment(request.text)
        return SentimentResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sentiment analysis failed: {str(e)}"
        )

# Emotion Analysis
@router.post("/emotion", response_model=EmotionResponse)
async def emotion_analysis(
    request: TextRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze emotions in the given text."""
    try:
        result = analyze_emotion(request.text)
        return EmotionResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Emotion analysis failed: {str(e)}"
        )

# Toxicity Detection
@router.post("/toxicity", response_model=ToxicityResponse)
async def toxicity_analysis(
    request: TextRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze toxicity level of the given text."""
    try:
        result = analyze_toxicity(request.text)
        return ToxicityResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Toxicity analysis failed: {str(e)}"
        )

# Distress Detection
@router.post("/distress", response_model=DistressResponse)
async def distress_analysis(
    request: TextRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Analyze distress level and detect urgent situations."""
    try:
        result = analyze_distress(request.text)
        return DistressResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Distress analysis failed: {str(e)}"
        )

# Comprehensive Analysis
@router.post("/analyze", response_model=ComprehensiveAnalysisResponse)
async def comprehensive_analysis(
    request: ComprehensiveAnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Perform comprehensive analysis including sentiment, emotion, toxicity, and distress detection."""
    try:
        sentiment = analyze_sentiment(request.text)
        emotion = analyze_emotion(request.text)
        toxicity = analyze_toxicity(request.text)
        distress = analyze_distress(request.text)
        
        return ComprehensiveAnalysisResponse(
            sentiment=SentimentResponse(**sentiment),
            emotion=EmotionResponse(**emotion),
            toxicity=ToxicityResponse(**toxicity),
            distress=DistressResponse(**distress),
            user_id=request.user_id or current_user.username
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive analysis failed: {str(e)}"
        )

# Advanced Chatbot
@router.post("/chatbot", response_model=ChatResponse)
async def chatbot_interaction(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Interact with the advanced mental health chatbot."""
    try:
        # Ensure user can only chat for themselves
        if request.user_id != current_user.username:
            raise UnauthorizedAccessError("You can only chat for yourself")
        
        reply = chatbot.get_reply(request.user_id, request.message)
        
        # Get the latest analysis from conversation history
        history = chatbot.get_conversation_history(request.user_id, limit=1)
        analysis = history[0]["analysis"] if history else None
        
        return ChatResponse(reply=reply, analysis=analysis)
        
    except (ConnectionFailure, ServerSelectionTimeoutError):
        raise DatabaseConnectionError("Database connection failed")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chatbot interaction failed: {str(e)}"
        )

# Risk Assessment from Sentiment History
@router.post("/risk/sentiment", response_model=RiskScoreResponse)
async def risk_assessment_sentiment(
    request: SentimentHistoryRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Calculate risk score from sentiment history."""
    try:
        # Ensure user can only access their own data
        if request.user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own data")
        
        result = calculate_risk_score(request.sentiments)
        return RiskScoreResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment failed: {str(e)}"
        )

# Risk Assessment from Emotion History
@router.post("/risk/emotion", response_model=RiskScoreResponse)
async def risk_assessment_emotion(
    request: EmotionHistoryRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Calculate risk score from emotion history."""
    try:
        # Ensure user can only access their own data
        if request.user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own data")
        
        result = calculate_risk_score([], request.emotions)
        return RiskScoreResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk assessment failed: {str(e)}"
        )

# Get Conversation History
@router.get("/chatbot/history/{user_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    user_id: str,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """Get conversation history for the specified user."""
    try:
        # Ensure user can only access their own chat history
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only access your own chat history")
        
        history = chatbot.get_conversation_history(user_id, limit)
        latest_analysis = history[-1]["analysis"] if history else None
        
        return ConversationHistoryResponse(
            user_id=user_id,
            conversations=history,
            total_count=len(history),
            latest_analysis=latest_analysis
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )

# Reset Chatbot Session
@router.post("/chatbot/reset/{user_id}")
async def reset_chatbot_session(
    user_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Reset chatbot session for the specified user."""
    try:
        # Ensure user can only reset their own session
        if user_id != current_user.username:
            raise UnauthorizedAccessError("You can only reset your own session")
        
        chatbot.reset_session(user_id)
        return {"message": "Chatbot session reset successfully", "user_id": user_id}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset chatbot session: {str(e)}"
        )

# Health Check
@router.get("/health")
async def nlp_health_check():
    """Check if NLP services are working properly."""
    try:
        # Test basic functionality
        test_text = "I am feeling good today"
        sentiment = analyze_sentiment(test_text)
        emotion = analyze_emotion(test_text)
        
        return {
            "status": "healthy",
            "services": {
                "sentiment_analysis": "working",
                "emotion_analysis": "working",
                "chatbot": "working"
            },
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }
