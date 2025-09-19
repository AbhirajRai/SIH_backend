import nltk
from nltk.corpus import wordnet
from app.emotion_utils import severe_emotions
from app.models import nlp_models
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Ensure NLTK wordnet is downloaded once externally:
# nltk.download('wordnet')

# Load Hugging Face toxicity model once
toxicity_model_name = "unitary/toxic-bert"
toxicity_tokenizer = AutoTokenizer.from_pretrained(toxicity_model_name)
toxicity_model = AutoModelForSequenceClassification.from_pretrained(toxicity_model_name)

def get_synonyms(word: str) -> set:
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

def is_synonym_in_set(label: str, ref_set: set) -> bool:
    label_lower = label.lower()
    if label_lower in ref_set:
        return True
    syns = get_synonyms(label_lower)
    return not syns.isdisjoint(ref_set)

def analyze_sentiment(text: str) -> dict:
    result = nlp_models.sentiment_analyzer(text, truncation=True)[0]
    return {"label": result["label"], "score": float(result["score"])}

def analyze_emotion(text: str) -> dict:
    result = nlp_models.emotion_analyzer(text, truncation=True)[0]
    return {"label": result["label"], "score": float(result["score"])}

def analyze_toxicity(text: str) -> dict:
    # Use Hugging Face toxicity model to produce probability
    inputs = toxicity_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = toxicity_model(**inputs)
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)
    toxic_prob = probs[0][1].item()
    return {"toxic": toxic_prob}

def analyze_distress(text: str) -> dict:
    urgent_phrases = [
        "suicide", "kill myself", "ending it all", "can't go on", "don't want to live",
        "hopeless", "no way out", "hurting myself", "want to die"
    ]
    lower_text = text.lower()
    is_urgent = False
    reason = ""

    # 1. Rule-based keyword detection
    for phrase in urgent_phrases:
        if phrase in lower_text:
            is_urgent = True
            reason = f"Detected urgent keyword: '{phrase}'"
            break

    # 2. NLP-based sentiment and emotion detection for subtle cases
    if not is_urgent:
        sentiment = nlp_models.sentiment_analyzer(text, truncation=True)[0]
        emotion = nlp_models.emotion_analyzer(text, truncation=True)[0]
        if sentiment["label"].lower() == "negative" and sentiment["score"] > 0.90:
            is_urgent = True
            reason = f"Very negative sentiment detected (score: {sentiment['score']:.2f})"
        elif emotion["label"].lower() in severe_emotions and emotion["score"] > 0.85:
            is_urgent = True
            reason = f"Strong negative emotion detected: {emotion['label']} (score: {emotion['score']:.2f})"

    if not is_urgent:
        reason = "No urgent distress detected."
    return {"is_urgent": is_urgent, "reason": reason}

def risk_from_sentiments(sentiments: list) -> dict:
    total = len(sentiments)
    if total == 0:
        return {"risk_score": 0.0, "advice": "No history to analyze."}

    negative_ref = {"negative", "bad", "sad", "angry", "upset", "unhappy"}

    negative_count = sum(1 for s in sentiments if is_synonym_in_set(s, negative_ref))
    risk = negative_count / total
    advice = "Monitor closely." if risk > 0.5 else "No elevated risk detected."
    return {"risk_score": round(risk, 2), "advice": advice}

def risk_from_emotions(emotions: list) -> dict:
    total = len(emotions)
    if total == 0:
        return {"risk_score": 0.0, "advice": "No history to analyze."}

    risky_ref = set(severe_emotions)  # Use your predefined set/list from emotion_utils

    risky_count = sum(1 for e in emotions if is_synonym_in_set(e, risky_ref))
    risk = risky_count / total
    advice = "Consider early intervention." if risk > 0.5 else "Low immediate risk."
    return {"risk_score": round(risk, 2), "advice": advice}
