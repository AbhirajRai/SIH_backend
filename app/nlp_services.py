"""
NLP Services for Mental Health Detection
"""

import torch.nn.functional as F
from typing import List, Dict
from app.nlp_models import nlp_models, is_synonym_in_set
from app.nlp_config import settings
import logging

logger = logging.getLogger(__name__)

def analyze_sentiment(text: str) -> Dict[str, any]:
    """Analyze sentiment of the given text."""
    try:
        result = nlp_models.sentiment_analyzer(text, truncation=True)[0]
        return {
            "label": result["label"], 
            "score": float(result["score"]),
            "confidence": "high" if result["score"] > 0.8 else "medium" if result["score"] > 0.6 else "low"
        }
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return {"label": "neutral", "score": 0.5, "confidence": "low", "error": str(e)}

def analyze_emotion(text: str) -> Dict[str, any]:
    """Analyze emotions in the given text."""
    try:
        result = nlp_models.emotion_analyzer(text, truncation=True)[0]
        return {
            "label": result["label"], 
            "score": float(result["score"]),
            "confidence": "high" if result["score"] > 0.8 else "medium" if result["score"] > 0.6 else "low"
        }
    except Exception as e:
        logger.error(f"Emotion analysis error: {e}")
        return {"label": "neutral", "score": 0.5, "confidence": "low", "error": str(e)}

def analyze_toxicity(text: str) -> Dict[str, any]:
    """Analyze toxicity level of the given text."""
    try:
        inputs = nlp_models.toxicity_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = nlp_models.toxicity_model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1)
        toxic_prob = probs[0][1].item()
        
        return {
            "toxic": toxic_prob,
            "level": "high" if toxic_prob > 0.7 else "medium" if toxic_prob > 0.4 else "low",
            "safe": toxic_prob < 0.3
        }
    except Exception as e:
        logger.error(f"Toxicity analysis error: {e}")
        return {"toxic": 0.0, "level": "low", "safe": True, "error": str(e)}

def analyze_distress(text: str) -> Dict[str, any]:
    """Analyze distress level and detect urgent situations."""
    try:
        lower_text = text.lower()
        is_urgent = False
        reason = ""
        confidence = 0.0
        
        # 1. Rule-based keyword detection
        for keyword in settings.urgent_keywords:
            if keyword in lower_text:
                is_urgent = True
                reason = f"Detected urgent keyword: '{keyword}'"
                confidence = 0.9
                break
        
        # 2. NLP-based sentiment and emotion detection for subtle cases
        if not is_urgent:
            sentiment = analyze_sentiment(text)
            emotion = analyze_emotion(text)
            
            # Check for very negative sentiment
            if sentiment["label"].lower() in ["negative", "neg"] and sentiment["score"] > 0.9:
                is_urgent = True
                reason = f"Very negative sentiment detected (score: {sentiment['score']:.2f})"
                confidence = sentiment["score"]
            
            # Check for severe emotions
            elif emotion["label"].lower() in settings.severe_emotions and emotion["score"] > settings.distress_confidence_threshold:
                is_urgent = True
                reason = f"Strong negative emotion detected: {emotion['label']} (score: {emotion['score']:.2f})"
                confidence = emotion["score"]
        
        if not is_urgent:
            reason = "No urgent distress detected."
            confidence = 0.1
        
        return {
            "is_urgent": is_urgent,
            "reason": reason,
            "confidence": confidence,
            "recommendation": "Seek immediate help" if is_urgent else "Continue monitoring"
        }
        
    except Exception as e:
        logger.error(f"Distress analysis error: {e}")
        return {
            "is_urgent": False,
            "reason": f"Analysis error: {str(e)}",
            "confidence": 0.0,
            "recommendation": "Manual review recommended"
        }

def calculate_risk_score(sentiments: List[str], emotions: List[str] = None) -> Dict[str, any]:
    """Calculate risk score from sentiment and emotion history."""
    try:
        total_sentiments = len(sentiments)
        total_emotions = len(emotions) if emotions else 0
        
        if total_sentiments == 0 and total_emotions == 0:
            return {
                "risk_score": 0.0,
                "level": "low",
                "advice": "No history to analyze.",
                "recommendations": ["Continue regular check-ins"]
            }
        
        # Analyze sentiment risk
        sentiment_risk = 0.0
        if total_sentiments > 0:
            negative_ref = {"negative", "neg", "bad", "sad", "angry", "upset", "unhappy"}
            negative_count = sum(1 for s in sentiments if is_synonym_in_set(s, negative_ref))
            sentiment_risk = negative_count / total_sentiments
        
        # Analyze emotion risk
        emotion_risk = 0.0
        if emotions and total_emotions > 0:
            risky_count = sum(1 for e in emotions if is_synonym_in_set(e, set(settings.severe_emotions)))
            emotion_risk = risky_count / total_emotions
        
        # Calculate overall risk
        overall_risk = (sentiment_risk + emotion_risk) / 2 if emotions else sentiment_risk
        
        # Determine risk level and advice
        if overall_risk > 0.7:
            level = "high"
            advice = "Immediate attention recommended"
            recommendations = [
                "Consider professional mental health support",
                "Increase monitoring frequency",
                "Implement immediate coping strategies"
            ]
        elif overall_risk > 0.4:
            level = "medium"
            advice = "Monitor closely and consider intervention"
            recommendations = [
                "Schedule regular check-ins",
                "Practice stress management techniques",
                "Consider talking to a counselor"
            ]
        else:
            level = "low"
            advice = "Continue current support level"
            recommendations = [
                "Maintain regular check-ins",
                "Continue current coping strategies"
            ]
        
        return {
            "risk_score": round(overall_risk, 2),
            "level": level,
            "advice": advice,
            "recommendations": recommendations,
            "sentiment_risk": round(sentiment_risk, 2),
            "emotion_risk": round(emotion_risk, 2) if emotions else None
        }
        
    except Exception as e:
        logger.error(f"Risk calculation error: {e}")
        return {
            "risk_score": 0.0,
            "level": "unknown",
            "advice": f"Analysis error: {str(e)}",
            "recommendations": ["Manual review recommended"]
        }
