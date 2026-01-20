from backend.storage.database import SessionLocal, Article, init_db
from backend.ingestion.rss_fetcher import fetch_articles
from backend.nlp.topic_classifier import classify_topic
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.summarizer import summarize_text


def store_articles():
    init_db()
    session = SessionLocal()

    articles = fetch_articles()

    for item in articles:
        exists = session.query(Article).filter_by(link=item["link"]).first()
        if exists:
            continue

        text = item["summary"] or item["title"]

        article = Article(
            title=item["title"],
            summary=item["summary"],
            link=item["link"],
            source=item["source"],
            published=item["published"],
            fetched_at=item["fetched_at"],
            topic=classify_topic(text),
            sentiment=analyze_sentiment(text),
            generated_summary=summarize_text(text)
        )
        session.add(article)

    session.commit()
    session.close()

if __name__ == "__main__":
    store_articles()
