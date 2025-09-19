# ai_services/nlp_service/app/models.py
from transformers import pipeline
from app.config import settings

class NLPModels:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=settings.sentiment_model_name,
            truncation=True,
            max_length=settings.max_length
        )
        self.toxicity_analyzer = pipeline(
            "text-classification",
            model=settings.toxicity_model_name,
            truncation=True,
            max_length=settings.max_length
        )
        self.emotion_analyzer = pipeline(
            "text-classification",
            model="bhadresh-savani/distilbert-base-uncased-emotion",
            return_all_scores=False,
            truncation=True,
            max_length=settings.max_length
        )

nlp_models = NLPModels()
