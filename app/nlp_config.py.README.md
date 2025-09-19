# nlp_config.py - AI Model Configuration

## What This File Does
This file contains all the configuration settings for the AI models used in mental health detection. It's like the "control panel" that tells the AI models how to behave and what to look for.

## In Simple Terms
Think of this as the instruction manual for the AI models - it tells them which models to use, how confident they should be before making decisions, and what words or emotions to pay special attention to.

## Key Configuration Areas

### 1. **AI Model Settings**
- **sentiment_model_name**: Which AI model to use for analyzing positive/negative feelings
- **toxicity_model_name**: Which AI model to use for detecting harmful or toxic content
- **emotion_model_name**: Which AI model to use for identifying specific emotions

### 2. **Processing Settings**
- **max_length**: Maximum number of words the AI can analyze at once (512 words)
- **truncation**: Whether to cut off text that's too long (True)

### 3. **Risk Assessment Thresholds**
- **sentiment_risk_threshold**: How negative sentiment needs to be to trigger concern (0.5 = 50%)
- **emotion_risk_threshold**: How strong negative emotions need to be to trigger concern (0.5 = 50%)
- **distress_confidence_threshold**: How confident the AI needs to be before flagging urgent distress (0.85 = 85%)

### 4. **Crisis Detection Keywords**
- **urgent_keywords**: List of words that indicate someone might be in immediate danger
- **severe_emotions**: List of emotions that indicate serious mental health concerns

## AI Models Explained

### 1. **Sentiment Analysis Model**
```python
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
```
**What it does:** Analyzes text to determine if it's positive, negative, or neutral
**Example:** "I feel great today" → Positive sentiment
**Example:** "I'm having a terrible day" → Negative sentiment

### 2. **Toxicity Detection Model**
```python
toxicity_model_name = "unitary/toxic-bert"
```
**What it does:** Detects harmful, offensive, or toxic content
**Example:** "You're stupid" → Toxic content detected
**Example:** "I'm feeling sad" → Not toxic

### 3. **Emotion Analysis Model**
```python
emotion_model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
```
**What it does:** Identifies specific emotions in text
**Example:** "I'm so angry right now" → Anger emotion
**Example:** "I feel anxious about the test" → Anxiety emotion

## Risk Assessment Settings

### 1. **Sentiment Risk Threshold (0.5)**
- If negative sentiment score is above 50%, it's considered risky
- Helps identify when someone is consistently negative
- Used for long-term risk assessment

### 2. **Emotion Risk Threshold (0.5)**
- If negative emotion score is above 50%, it's considered risky
- Helps identify when someone is experiencing strong negative emotions
- Used for emotional risk assessment

### 3. **Distress Confidence Threshold (0.85)**
- AI must be 85% confident before flagging urgent distress
- Prevents false alarms from weak signals
- Ensures only serious concerns are escalated

## Crisis Detection Keywords

### 1. **Urgent Keywords**
```python
urgent_keywords = [
    "suicide", "kill myself", "ending it all", "can't go on", 
    "don't want to live", "hopeless", "no way out", 
    "hurting myself", "want to die", "end it all"
]
```
**Purpose:** Immediate crisis intervention
**Action:** Triggers urgent response and crisis resources
**Example:** "I want to kill myself" → Immediate crisis intervention

### 2. **Severe Emotions**
```python
severe_emotions = [
    "sadness", "anger", "fear", "disgust", "shame", 
    "guilt", "hopelessness", "despair", "rage"
]
```
**Purpose:** Identify serious emotional distress
**Action:** Triggers increased monitoring and support
**Example:** "I feel hopeless" → Increased support and monitoring

## How Configuration Works

### 1. **Model Selection**
```python
# The AI system loads these specific models
sentiment_analyzer = pipeline("sentiment-analysis", model=settings.sentiment_model_name)
emotion_analyzer = pipeline("text-classification", model=settings.emotion_model_name)
```

### 2. **Threshold Checking**
```python
# Risk assessment uses these thresholds
if sentiment_score > settings.sentiment_risk_threshold:
    # Flag as potentially risky
    risk_level = "high"
```

### 3. **Keyword Detection**
```python
# Crisis detection checks for urgent keywords
for keyword in settings.urgent_keywords:
    if keyword in text.lower():
        # Trigger immediate crisis intervention
        is_urgent = True
```

## Configuration Benefits

### 1. **Customization**
- Easy to adjust sensitivity levels
- Can modify which models to use
- Flexible threshold settings

### 2. **Safety**
- Conservative thresholds prevent false alarms
- High confidence requirements for crisis detection
- Multiple layers of risk assessment

### 3. **Performance**
- Optimized model selection for accuracy
- Reasonable text length limits
- Efficient processing settings

### 4. **Maintainability**
- Centralized configuration
- Easy to update models or thresholds
- Clear documentation of settings

## Usage Examples

### 1. **Loading Models**
```python
from app.nlp_config import settings

# Load sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model=settings.sentiment_model_name)

# Load emotion analysis model
emotion_analyzer = pipeline("text-classification", model=settings.emotion_model_name)
```

### 2. **Risk Assessment**
```python
# Check if sentiment is risky
if sentiment_score > settings.sentiment_risk_threshold:
    risk_level = "high"
else:
    risk_level = "low"
```

### 3. **Crisis Detection**
```python
# Check for urgent keywords
for keyword in settings.urgent_keywords:
    if keyword in text.lower():
        return {"is_urgent": True, "reason": f"Detected urgent keyword: {keyword}"}
```

## Why This Structure Matters

### 1. **Safety First**
- Conservative thresholds prevent false alarms
- High confidence requirements for serious concerns
- Multiple safety checks

### 2. **Flexibility**
- Easy to adjust sensitivity
- Can update models without code changes
- Configurable for different use cases

### 3. **Accuracy**
- Carefully selected models for mental health
- Optimized thresholds for real-world use
- Balanced sensitivity and specificity

### 4. **Maintainability**
- Centralized configuration
- Clear documentation
- Easy to update and modify

This configuration system ensures that the AI models are properly tuned for mental health detection while maintaining safety and accuracy standards.
