from transformers import pipeline

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

TOPICS = ["Politics", "Economy", "Technology", "Health", "Climate", "Conflict", "Sports"]

def classify_topic(text):
    result = classifier(text, candidate_labels=TOPICS)
    return result['labels'][0]  # top predicted topic
