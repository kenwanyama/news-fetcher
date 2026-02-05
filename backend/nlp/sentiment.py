from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

TOPIC_BIAS = {
    "CONFLICT": -0.3,
    "ECONOMY": -0.1,
    "POLITICS": -0.05,
    "TECH": 0.0,
    "HEALTH": -0.1,
    "CLIMATE": -0.2,
    "SPORTS": 0.05
}


analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(article, topic):
    """
    Analyze sentiment using VADER (very lightweight)
    Returns: LABEL_POSITIVE, LABEL_NEGATIVE, or LABEL_NEUTRAL
    """
    text = article.get("title", "") + " " + article.get("summary", "")
    
    if not text.strip():
        return "LABEL_NEUTRAL"
    
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']  # -1 to 1
    
    # Apply topic bias
    adjusted_score = compound + TOPIC_BIAS.get(topic, 0)
    
    # Classify
    if adjusted_score > 0.05:
        return "LABEL_POSITIVE"
    elif adjusted_score < -0.05:
        return "LABEL_NEGATIVE"
    else:
        return "LABEL_NEUTRAL"
