import feedparser
from datetime import datetime, timezone

RSS_FEEDS = {
    "CNN": "http://rss.cnn.com/rss/cnn_topstories.rss",
    "BBC": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "NPR": "https://feeds.npr.org/1001/rss.xml"
}

def fetch_articles(limit=5):
    articles = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries[:limit]:
            articles.append({
                "title": entry.get("title"),
                "summary": entry.get("summary", ""),
                "link": entry.get("link"),
                "published": entry.get("published", ""),
                "source": source,
                "fetched_at": datetime.now(timezone.utc)
            })

    random.shuffle(articles)

    return articles


if __name__ == "__main__":
    data = fetch_articles()
    print(f"Fetched {len(data)} articles")
    print(data[0])
