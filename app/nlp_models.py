"""
NLP Models for Mental Health Detection
"""

import warnings
import logging
import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

# Suppress ALL warnings before importing transformers
warnings.filterwarnings("ignore")
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Redirect stderr to suppress transformers output
class SuppressOutput:
    def __enter__(self):
        self._original_stderr = sys.stderr
        self._original_stdout = sys.stdout
        sys.stderr = StringIO()
        sys.stdout = StringIO()
        return self
    
    def __exit__(self, *args):
        sys.stderr = self._original_stderr
        sys.stdout = self._original_stdout

# Set logging levels to suppress all transformers output
logging.getLogger("transformers").setLevel(logging.CRITICAL)
logging.getLogger("transformers.modeling_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.configuration_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.tokenization_utils").setLevel(logging.CRITICAL)
logging.getLogger("transformers.modeling_roberta").setLevel(logging.CRITICAL)

import nltk
from nltk.corpus import wordnet
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch.nn.functional as F
from app.nlp_config import settings
import logging

logger = logging.getLogger(__name__)

class NLPModels:
    def __init__(self):
        """Initialize NLP models for mental health detection."""
        try:
            # Download required NLTK data
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                nltk.download('wordnet', quiet=True)
            
            # Initialize models with output suppression
            with SuppressOutput():
                # Initialize sentiment analysis model
                self.sentiment_analyzer = pipeline(
                    "sentiment-analysis",
                    model=settings.sentiment_model_name,
                    truncation=settings.truncation,
                    max_length=settings.max_length
                )
                
                # Initialize emotion analysis model
                self.emotion_analyzer = pipeline(
                    "text-classification",
                    model=settings.emotion_model_name,
                    top_k=1,
                    truncation=settings.truncation,
                    max_length=settings.max_length
                )
                
                # Initialize toxicity detection model
                self.toxicity_tokenizer = AutoTokenizer.from_pretrained(settings.toxicity_model_name)
                self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(settings.toxicity_model_name)
            
            logger.info("✅ NLP models loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Error loading NLP models: {e}")
            # Fallback to basic models
            self._load_fallback_models()
    
    def _load_fallback_models(self):
        """Load fallback models if primary models fail."""
        try:
            with SuppressOutput():
                self.sentiment_analyzer = pipeline("sentiment-analysis")
                self.emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
            logger.info("✅ Fallback NLP models loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load fallback models: {e}")
            raise

# Global instance
nlp_models = NLPModels()

def get_synonyms(word: str) -> set:
    """Get synonyms for a word using WordNet."""
    synonyms = set()
    try:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().lower())
    except Exception as e:
        logger.warning(f"Error getting synonyms for {word}: {e}")
    return synonyms

def is_synonym_in_set(label: str, ref_set: set) -> bool:
    """Check if a label or its synonyms are in the reference set."""
    label_lower = label.lower()
    if label_lower in ref_set:
        return True
    syns = get_synonyms(label_lower)
    return not syns.isdisjoint(ref_set)
