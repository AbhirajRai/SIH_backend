from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.services import (
    analyze_sentiment,
    analyze_toxicity,
    analyze_emotion,
    analyze_distress,
    risk_from_sentiments,
    risk_from_emotions,
)
from app.chatbot import chatbot
from app.schemas import (
    TextRequest,
    SentimentResponse,
    ToxicityResponse,
    EmotionResponse,
    ChatRequest,
    ChatResponse,
    DistressResponse,
    SentimentHistoryRequest,
    EmotionHistoryRequest,
    RiskScoreResponse,
)

app = FastAPI(title="MindCare NLP Microservice")


# Root GET endpoint (health check)
@app.get("/")
async def root():
    return {"message": "MindCare NLP Microservice is running."}


# Sentiment Analysis POST endpoint
@app.post("/nlp/sentiment", response_model=SentimentResponse)
async def sentiment_analysis(request: TextRequest):
    try:
        result = analyze_sentiment(request.text)
        return result
    except Exception as e:
        logging.error(f"Sentiment analysis error: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing sentiment")


# Distress Detection POST endpoint
@app.post("/nlp/distress", response_model=DistressResponse)
async def distress_analysis(request: TextRequest):
    try:
        result = analyze_distress(request.text)
        return result
    except Exception as e:
        logging.error(f"Distress analysis error: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing distress")


# Toxicity Detection POST endpoint
@app.post("/nlp/toxicity", response_model=ToxicityResponse)
async def toxicity_analysis(request: TextRequest):
    try:
        result = analyze_toxicity(request.text)
        return result
    except Exception as e:
        logging.error(f"Toxicity analysis error: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing toxicity")


# Emotion Detection POST endpoint
@app.post("/nlp/emotion", response_model=EmotionResponse)
async def emotion_analysis(request: TextRequest):
    try:
        result = analyze_emotion(request.text)
        return result
    except Exception as e:
        logging.error(f"Emotion analysis error: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing emotion")


# Chatbot Interaction POST endpoint
@app.post("/nlp/chatbot", response_model=ChatResponse)
async def chatbot_endpoint(request: ChatRequest):
    try:
        reply = chatbot.get_reply(request.user_id, request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        logging.error(f"Chatbot error: {e}")
        raise HTTPException(status_code=500, detail="Chatbot processing error")


# Sentiment Risk Score endpoint
@app.post("/nlp/risk_score/sentiment", response_model=RiskScoreResponse)
async def risk_score_sentiment(request: SentimentHistoryRequest):
    try:
        return risk_from_sentiments(request.sentiments)
    except Exception as e:
        logging.error(f"Sentiment risk scoring error: {e}")
        raise HTTPException(status_code=500, detail="Error calculating sentiment risk score")


# Emotion Risk Score endpoint
@app.post("/nlp/risk_score/emotion", response_model=RiskScoreResponse)
async def risk_score_emotion(request: EmotionHistoryRequest):
    try:
        return risk_from_emotions(request.emotions)
    except Exception as e:
        logging.error(f"Emotion risk scoring error: {e}")
        raise HTTPException(status_code=500, detail="Error calculating emotion risk score")
