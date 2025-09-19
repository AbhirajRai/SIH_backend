from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Load the tokenizer and model once on import for efficiency
TOKENIZER = AutoTokenizer.from_pretrained("unitary/toxic-bert")
MODEL = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")

def analyze_toxicity(text: str) -> dict:
    """
    Analyze toxicity of the given text using the 'unitary/toxic-bert' model.

    Args:
        text (str): Input text to analyze.

    Returns:
        dict: Dictionary containing toxic probability score (0.0 to 1.0)
    """
    inputs = TOKENIZER(text, return_tensors="pt", truncation=True, padding=True)
    outputs = MODEL(**inputs)
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)
    toxic_prob = probs[0][1].item()  # Probability of "toxic" label
    return {"toxic": toxic_prob}
