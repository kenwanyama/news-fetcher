from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis",
                              model="cardiffnlp/twitter-roberta-base-sentiment")

def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]['label']  # Positive / Neutral / Negative
