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
    "SPORTS": ["sports", "football", "basketball", "soccer", "nba", "nfl", "game", "player", "championship", "team"]
}

# Create TF-IDF vectorizer (initialized once)
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)

# Create topic profiles by combining keywords
topic_profiles = {topic: " ".join(keywords) for topic, keywords in TOPIC_KEYWORDS.items()}

# Fit vectorizer on topic profiles
vectorizer.fit(list(topic_profiles.values()))

def classify_topic(text):
    """
    Classify topic using TF-IDF and cosine similarity (actual NLP/ML)
    """
    if not text or not text.strip():
        return "GENERAL"
    
    try:
        # Vectorize the input text
        text_vector = vectorizer.transform([text.lower()])
        
        # Vectorize all topic profiles
        topic_vectors = vectorizer.transform(list(topic_profiles.values()))
        
        # Calculate cosine similarity between text and each topic
        similarities = cosine_similarity(text_vector, topic_vectors)[0]
        
        # Get topic with highest similarity
        max_idx = np.argmax(similarities)
        max_similarity = similarities[max_idx]
        
        # If similarity is too low, return GENERAL
        if max_similarity < 0.1:
            return "GENERAL"
        
        topic_names = list(topic_profiles.keys())
        return topic_names[max_idx]
    
    except:
        return "GENERAL"