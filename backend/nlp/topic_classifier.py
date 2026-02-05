from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

TOPIC_KEYWORDS = {
    "POLITICS": ["election", "government", "congress", "senate", "president", "vote", "law", "policy", "minister", "parliament"],
    "ECONOMY": ["economy", "market", "stock", "trade", "inflation", "gdp", "finance", "banking", "federal reserve", "dollar"],
    "TECHNOLOGY": ["tech", "ai", "software", "apple", "google", "microsoft", "startup", "app", "data", "cyber"],
    "HEALTH": ["health", "medical", "hospital", "doctor", "disease", "vaccine", "drug", "covid", "pandemic", "treatment"],
    "CLIMATE": ["climate", "environment", "carbon", "emissions", "renewable", "pollution", "global warming", "sustainability"],
    "CONFLICT": ["war", "military", "attack", "conflict", "violence", "terror", "weapon", "soldier", "bombing"],
    "SPORTS": ["sports", "football", "basketball", "soccer", "nba", "nfl", "game", "player", "championship", "team", "world cup", "cricket"]
}

vectorizer = TfidfVectorizer(stop_words='english', max_features=500)

# Create topic profiles
topic_profiles = {topic: " ".join(keywords) for topic, keywords in TOPIC_KEYWORDS.items()}
vectorizer.fit(list(topic_profiles.values()))

def classify_topic(text):
    if not text or not text.strip():
        return "GENERAL"
    
    text = text.lower()
    
    # Keyword-based boost
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                return topic

    # TF-IDF + cosine similarity fallback
    try:
        text_vector = vectorizer.transform([text])
        topic_vectors = vectorizer.transform(list(topic_profiles.values()))
        similarities = cosine_similarity(text_vector, topic_vectors)[0]
        max_idx = np.argmax(similarities)
        if similarities[max_idx] < 0.05:  # lower threshold
            return "GENERAL"
        topic_names = list(topic_profiles.keys())
        return topic_names[max_idx]
    except:
        return "GENERAL"
