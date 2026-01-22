from functools import lru_cache
from transformers import pipeline

TOPIC_BIAS = {
    "CONFLICT": -0.3,
    "ECONOMY": -0.1,
    "POLITICS": -0.05,
    "TECH": 0.0,
    "HEALTH": -0.1,
    "CLIMATE": -0.2,
    "SPORTS": 0.05
}

@lru_cache(maxsize=1)
def get_sentiment_analyzer():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

def analyze_sentiment(article, topic):
    text = article["title"] + " " + article["summary"]

    if not text.strip():
        return "NEUTRAL"

    sentiment_analyzer = get_sentiment_analyzer()
    result = sentiment_analyzer(text)[0]

    score = result["score"]
    if result["label"] == "NEGATIVE":
        score = -score

    adjusted_score = score + TOPIC_BIAS.get(topic, 0)

    if adjusted_score > 0.25:
        return "POSITIVE"
    elif adjusted_score < -0.25:
        return "NEGATIVE"
    else:
        return "NEUTRAL"
