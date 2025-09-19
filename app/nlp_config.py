"""
NLP Configuration for Mental Health Detection
"""

class NLPSettings:
    # Model configurations
    sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    toxicity_model_name = "unitary/toxic-bert"
    emotion_model_name = "bhadresh-savani/distilbert-base-uncased-emotion"
    
    # Processing settings
    max_length = 512
    truncation = True
    
    # Risk assessment thresholds
    sentiment_risk_threshold = 0.5
    emotion_risk_threshold = 0.5
    distress_confidence_threshold = 0.85
    
    # Urgent distress keywords
    urgent_keywords = [
        "suicide", "kill myself", "ending it all", "can't go on", 
        "don't want to live", "hopeless", "no way out", 
        "hurting myself", "want to die", "end it all"
    ]
    
    # Severe emotions for risk assessment
    severe_emotions = [
        "sadness", "anger", "fear", "disgust", "shame", 
        "guilt", "hopelessness", "despair", "rage"
    ]

settings = NLPSettings()
