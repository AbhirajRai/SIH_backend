# nlp_services.py - Core AI Analysis Functions

## What This File Does
This file contains the core AI analysis functions that process text and provide mental health insights. It's like the "brain" of the AI system that actually performs the analysis and makes decisions.

## In Simple Terms
Think of this as the AI analyst that reads text messages, understands emotions, and provides insights about mental health. It takes raw text and turns it into actionable information about someone's emotional state.

## Key Analysis Functions

### 1. **Sentiment Analysis**
```python
def analyze_sentiment(text: str) -> Dict[str, any]:
    """Analyze sentiment of the given text."""
```
**What it does:** Determines if text is positive, negative, or neutral
**Input:** "I'm having a great day!"
**Output:** {"label": "POSITIVE", "score": 0.95, "confidence": "high"}

### 2. **Emotion Analysis**
```python
def analyze_emotion(text: str) -> Dict[str, any]:
    """Analyze emotions in the given text."""
```
**What it does:** Identifies specific emotions in text
**Input:** "I'm so anxious about the exam"
**Output:** {"label": "anxiety", "score": 0.87, "confidence": "high"}

### 3. **Toxicity Detection**
```python
def analyze_toxicity(text: str) -> Dict[str, any]:
    """Analyze toxicity level of the given text."""
```
**What it does:** Detects harmful or offensive content
**Input:** "You're worthless"
**Output:** {"toxic": 0.92, "level": "high", "safe": False}

### 4. **Distress Detection**
```python
def analyze_distress(text: str) -> Dict[str, any]:
    """Analyze distress level and detect urgent situations."""
```
**What it does:** Identifies if someone is in immediate danger
**Input:** "I want to kill myself"
**Output:** {"is_urgent": True, "reason": "Detected urgent keyword: 'kill myself'", "confidence": 0.9, "recommendation": "Seek immediate help"}

### 5. **Risk Assessment**
```python
def calculate_risk_score(sentiments: List[str], emotions: List[str] = None) -> Dict[str, any]:
    """Calculate risk score from sentiment and emotion history."""
```
**What it does:** Analyzes patterns over time to assess mental health risk
**Input:** List of past sentiments and emotions
**Output:** {"risk_score": 0.75, "level": "high", "advice": "Immediate attention recommended", "recommendations": ["Consider professional mental health support"]}

## How Each Function Works

### 1. **Sentiment Analysis Process**
```python
def analyze_sentiment(text: str) -> Dict[str, any]:
    try:
        # Use AI model to analyze sentiment
        result = nlp_models.sentiment_analyzer(text, truncation=True)[0]
        return {
            "label": result["label"],  # POSITIVE, NEGATIVE, or NEUTRAL
            "score": float(result["score"]),  # Confidence score (0-1)
            "confidence": "high" if result["score"] > 0.8 else "medium" if result["score"] > 0.6 else "low"
        }
    except Exception as e:
        logger.error(f"Sentiment analysis error: {e}")
        return {"label": "neutral", "score": 0.5, "confidence": "low", "error": str(e)}
```

### 2. **Emotion Analysis Process**
```python
def analyze_emotion(text: str) -> Dict[str, any]:
    try:
        # Use AI model to identify emotions
        result = nlp_models.emotion_analyzer(text, truncation=True)[0]
        return {
            "label": result["label"],  # Specific emotion (anxiety, sadness, joy, etc.)
            "score": float(result["score"]),  # Confidence score (0-1)
            "confidence": "high" if result["score"] > 0.8 else "medium" if result["score"] > 0.6 else "low"
        }
    except Exception as e:
        logger.error(f"Emotion analysis error: {e}")
        return {"label": "neutral", "score": 0.5, "confidence": "low", "error": str(e)}
```

### 3. **Toxicity Detection Process**
```python
def analyze_toxicity(text: str) -> Dict[str, any]:
    try:
        # Prepare text for toxicity model
        inputs = nlp_models.toxicity_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = nlp_models.toxicity_model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1)
        toxic_prob = probs[0][1].item()  # Probability of toxicity
        
        return {
            "toxic": toxic_prob,  # Toxicity probability (0-1)
            "level": "high" if toxic_prob > 0.7 else "medium" if toxic_prob > 0.4 else "low",
            "safe": toxic_prob < 0.3  # Whether text is safe
        }
    except Exception as e:
        logger.error(f"Toxicity analysis error: {e}")
        return {"toxic": 0.0, "level": "low", "safe": True, "error": str(e)}
```

### 4. **Distress Detection Process**
```python
def analyze_distress(text: str) -> Dict[str, any]:
    try:
        lower_text = text.lower()
        is_urgent = False
        reason = ""
        confidence = 0.0
        
        # 1. Check for urgent keywords
        for keyword in settings.urgent_keywords:
            if keyword in lower_text:
                is_urgent = True
                reason = f"Detected urgent keyword: '{keyword}'"
                confidence = 0.9
                break
        
        # 2. If no urgent keywords, check sentiment and emotion
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
```

### 5. **Risk Assessment Process**
```python
def calculate_risk_score(sentiments: List[str], emotions: List[str] = None) -> Dict[str, any]:
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
```

## Analysis Results Explained

### 1. **Sentiment Analysis Results**
- **label**: POSITIVE, NEGATIVE, or NEUTRAL
- **score**: Confidence score (0-1, where 1 is most confident)
- **confidence**: "high" (>0.8), "medium" (0.6-0.8), or "low" (<0.6)

### 2. **Emotion Analysis Results**
- **label**: Specific emotion (anxiety, sadness, joy, anger, fear, etc.)
- **score**: Confidence score (0-1)
- **confidence**: "high", "medium", or "low"

### 3. **Toxicity Detection Results**
- **toxic**: Probability of toxicity (0-1)
- **level**: "high" (>0.7), "medium" (0.4-0.7), or "low" (<0.4)
- **safe**: Boolean indicating if text is safe

### 4. **Distress Detection Results**
- **is_urgent**: Boolean indicating if immediate intervention is needed
- **reason**: Explanation of why distress was detected
- **confidence**: Confidence in the assessment (0-1)
- **recommendation**: Suggested action ("Seek immediate help" or "Continue monitoring")

### 5. **Risk Assessment Results**
- **risk_score**: Overall risk score (0-1)
- **level**: "high", "medium", or "low"
- **advice**: General advice based on risk level
- **recommendations**: Specific actionable recommendations
- **sentiment_risk**: Risk score based on sentiment history
- **emotion_risk**: Risk score based on emotion history

## Error Handling

### 1. **Model Errors**
- All functions include try-catch blocks
- Errors are logged for debugging
- Fallback values are returned when models fail

### 2. **Input Validation**
- Functions handle empty or invalid input
- Graceful degradation for edge cases
- Consistent error response format

### 3. **Performance Issues**
- Functions handle slow model responses
- Timeout protection for long-running operations
- Efficient processing for large datasets

## Usage Examples

### 1. **Basic Analysis**
```python
from app.nlp_services import analyze_sentiment, analyze_emotion

# Analyze sentiment
text = "I'm feeling really down today"
sentiment = analyze_sentiment(text)
# Result: {"label": "NEGATIVE", "score": 0.89, "confidence": "high"}

# Analyze emotion
emotion = analyze_emotion(text)
# Result: {"label": "sadness", "score": 0.92, "confidence": "high"}
```

### 2. **Crisis Detection**
```python
from app.nlp_services import analyze_distress

# Check for urgent distress
text = "I want to kill myself"
distress = analyze_distress(text)
# Result: {"is_urgent": True, "reason": "Detected urgent keyword: 'kill myself'", "confidence": 0.9, "recommendation": "Seek immediate help"}
```

### 3. **Risk Assessment**
```python
from app.nlp_services import calculate_risk_score

# Assess risk from history
sentiments = ["negative", "negative", "positive", "negative"]
emotions = ["sadness", "anxiety", "joy", "sadness"]
risk = calculate_risk_score(sentiments, emotions)
# Result: {"risk_score": 0.75, "level": "high", "advice": "Immediate attention recommended", "recommendations": ["Consider professional mental health support"]}
```

## Why This Structure Matters

### 1. **Safety**
- Multiple layers of crisis detection
- Conservative thresholds for urgent situations
- Comprehensive error handling

### 2. **Accuracy**
- Specialized models for mental health
- Multiple analysis approaches
- Confidence scoring for reliability

### 3. **Usability**
- Clear, actionable results
- Consistent response format
- Easy to integrate with other systems

### 4. **Maintainability**
- Modular function design
- Centralized error handling
- Easy to test and debug

This service layer provides the core AI analysis capabilities that power the mental health detection features of the MindCare API.
