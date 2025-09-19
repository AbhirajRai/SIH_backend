# nlp_models.py - AI Model Loading and Management

## What This File Does
This file handles loading and initializing all the AI models used for mental health analysis. It's like the "factory" that builds and prepares all the AI tools needed for text analysis.

## In Simple Terms
Think of this as the workshop where all the AI models are assembled and tested. It downloads the models, sets them up, and makes sure they're ready to analyze text for mental health insights.

## Key Responsibilities

### 1. **Model Loading**
- Downloads and loads pre-trained AI models
- Sets up model configurations and parameters
- Handles model initialization errors gracefully

### 2. **Fallback Systems**
- Provides backup models if primary models fail
- Ensures the system continues working even if some models fail
- Maintains service availability

### 3. **Model Management**
- Manages model instances and configurations
- Provides access to models throughout the application
- Handles model lifecycle and updates

## AI Models Explained

### 1. **Sentiment Analysis Model**
```python
self.sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model=settings.sentiment_model_name,  # "cardiffnlp/twitter-roberta-base-sentiment-latest"
    truncation=settings.truncation,
    max_length=settings.max_length
)
```
**What it does:** Analyzes text to determine if it's positive, negative, or neutral
**Input:** "I'm feeling great today!"
**Output:** {"label": "POSITIVE", "score": 0.95}

### 2. **Emotion Analysis Model**
```python
self.emotion_analyzer = pipeline(
    "text-classification",
    model=settings.emotion_model_name,  # "bhadresh-savani/distilbert-base-uncased-emotion"
    return_all_scores=False,
    truncation=settings.truncation,
    max_length=settings.max_length
)
```
**What it does:** Identifies specific emotions in text
**Input:** "I'm so anxious about the exam"
**Output:** {"label": "anxiety", "score": 0.87}

### 3. **Toxicity Detection Model**
```python
self.toxicity_tokenizer = AutoTokenizer.from_pretrained(settings.toxicity_model_name)
self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(settings.toxicity_model_name)
```
**What it does:** Detects harmful, offensive, or toxic content
**Input:** "You're worthless"
**Output:** {"toxic": 0.92, "level": "high", "safe": False}

## Model Loading Process

### 1. **Initialization**
```python
def __init__(self):
    try:
        # Download required NLTK data
        nltk.download('wordnet', quiet=True)
        
        # Load sentiment analysis model
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=settings.sentiment_model_name)
        
        # Load emotion analysis model
        self.emotion_analyzer = pipeline("text-classification", model=settings.emotion_model_name)
        
        # Load toxicity detection model
        self.toxicity_tokenizer = AutoTokenizer.from_pretrained(settings.toxicity_model_name)
        self.toxicity_model = AutoModelForSequenceClassification.from_pretrained(settings.toxicity_model_name)
        
        logger.info("✅ NLP models loaded successfully")
        
    except Exception as e:
        logger.error(f"❌ Error loading NLP models: {e}")
        self._load_fallback_models()
```

### 2. **Fallback System**
```python
def _load_fallback_models(self):
    """Load fallback models if primary models fail."""
    try:
        # Use default models if custom models fail
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        logger.info("✅ Fallback NLP models loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load fallback models: {e}")
        raise
```

## Helper Functions

### 1. **Synonym Detection**
```python
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
```
**Purpose:** Find related words to improve emotion detection
**Example:** "sad" → {"sad", "sorrowful", "melancholy", "depressed"}

### 2. **Synonym Matching**
```python
def is_synonym_in_set(label: str, ref_set: set) -> bool:
    """Check if a label or its synonyms are in the reference set."""
    label_lower = label.lower()
    if label_lower in ref_set:
        return True
    syns = get_synonyms(label_lower)
    return not syns.isdisjoint(ref_set)
```
**Purpose:** Check if an emotion matches any emotion in a reference set
**Example:** "sorrowful" matches "sad" because they're synonyms

## Model Configuration

### 1. **Text Processing Settings**
- **max_length**: 512 tokens (words) maximum
- **truncation**: True (cut off text that's too long)
- **return_all_scores**: False (only return the best match)

### 2. **Model Selection**
- **Primary models**: Specialized for mental health analysis
- **Fallback models**: General-purpose models if primary fails
- **NLTK integration**: For advanced text processing

## Error Handling

### 1. **Model Loading Errors**
```python
try:
    # Load primary models
    self.sentiment_analyzer = pipeline("sentiment-analysis", model=settings.sentiment_model_name)
except Exception as e:
    logger.error(f"❌ Error loading NLP models: {e}")
    # Load fallback models
    self._load_fallback_models()
```

### 2. **Fallback Model Errors**
```python
try:
    # Load fallback models
    self.sentiment_analyzer = pipeline("sentiment-analysis")
except Exception as e:
    logger.error(f"❌ Failed to load fallback models: {e}")
    raise  # This will cause the application to fail
```

### 3. **Runtime Errors**
- Models are wrapped in try-catch blocks
- Errors are logged for debugging
- Graceful degradation when possible

## Global Model Instance

### 1. **Singleton Pattern**
```python
# Global instance
nlp_models = NLPModels()
```
**Purpose:** Single instance shared across the application
**Benefits:** Efficient memory usage, consistent model state

### 2. **Model Access**
```python
from app.nlp_models import nlp_models

# Use the models
sentiment_result = nlp_models.sentiment_analyzer("I feel great!")
emotion_result = nlp_models.emotion_analyzer("I'm anxious about the test")
```

## Performance Considerations

### 1. **Model Size**
- **Transformers models**: Large (hundreds of MB to GB)
- **Loading time**: Can take 30-60 seconds on first startup
- **Memory usage**: High RAM requirements

### 2. **Optimization**
- **Model caching**: Models are loaded once and reused
- **Batch processing**: Can process multiple texts efficiently
- **GPU acceleration**: Models can use GPU if available

### 3. **Fallback Strategy**
- **Lightweight models**: Fallback models are smaller and faster
- **Reduced functionality**: Fallback models may be less accurate
- **Service continuity**: Ensures the API continues working

## Usage Examples

### 1. **Basic Model Usage**
```python
from app.nlp_models import nlp_models

# Analyze sentiment
text = "I'm feeling really down today"
result = nlp_models.sentiment_analyzer(text)
# Result: {"label": "NEGATIVE", "score": 0.89}

# Analyze emotion
result = nlp_models.emotion_analyzer(text)
# Result: {"label": "sadness", "score": 0.92}
```

### 2. **Synonym Usage**
```python
from app.nlp_models import get_synonyms, is_synonym_in_set

# Get synonyms
synonyms = get_synonyms("sad")
# Result: {"sad", "sorrowful", "melancholy", "depressed"}

# Check if emotion matches reference set
negative_emotions = {"sad", "angry", "fearful"}
is_negative = is_synonym_in_set("sorrowful", negative_emotions)
# Result: True (because "sorrowful" is a synonym of "sad")
```

## Why This Structure Matters

### 1. **Reliability**
- Fallback models ensure service continuity
- Error handling prevents crashes
- Graceful degradation when models fail

### 2. **Performance**
- Models are loaded once and reused
- Efficient memory usage with singleton pattern
- Optimized for mental health analysis

### 3. **Maintainability**
- Centralized model management
- Easy to update or replace models
- Clear separation of concerns

### 4. **Flexibility**
- Can easily add new models
- Configurable model selection
- Supports different model types

This model management system provides a robust foundation for AI-powered mental health analysis while ensuring reliability and performance.
