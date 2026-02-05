from backend.nlp.sentiment import get_sentiment_analyzer
from backend.nlp.summarizer import get_summarizer
from backend.nlp.topic_classifier import get_topic_classifier

def nlp_loader():
    print("Warming up NLP models...")
    get_sentiment_analyzer()
    get_summarizer()
    get_topic_classifier()
    print("NLP models loaded.")
