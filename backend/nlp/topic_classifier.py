from functools import lru_cache
from transformers import pipeline

TOPICS = ["Politics", "Economy", "Technology", "Health", "Climate", "Conflict", "Sports"]

@lru_cache(maxsize=1)
def get_topic_classifier():
    return pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

def classify_topic(text):
    classifier = get_topic_classifier()
    result = classifier(text, candidate_labels=TOPICS)
    return result['labels'][0]
