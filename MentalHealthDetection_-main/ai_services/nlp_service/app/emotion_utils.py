import nltk
from nltk.corpus import wordnet

# Download WordNet data once when module loads
nltk.download('wordnet')

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower())
    return synonyms

# Base set of severe emotions
severe_base = {"anger", "sadness", "fear", "despair"}

# Expanded synonyms set for severe emotions (run once)
severe_emotions = set()
for emotion in severe_base:
    severe_emotions.update(get_synonyms(emotion))
