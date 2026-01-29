from sqlalchemy.exc import IntegrityError
from backend.storage.database import SessionLocal, Article
from backend.ingestion.rss_fetcher import fetch_articles
from backend.nlp.topic_classifier import classify_topic
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.summarizer import summarize_text


def store_articles():
    articles = fetch_articles()
    session = SessionLocal()
    count = 0

    try:
        for item in articles:
            if session.query(Article).filter_by(link=item["link"]).first():
                continue

            text = item["summary"] or item["title"]
            topic = classify_topic(text)

            article = Article(
                title=item["title"],
                summary=item["summary"],
                link=item["link"],
                source=item["source"],
                published=item["published"],
                fetched_at=item["fetched_at"],
                topic=topic,
                sentiment=analyze_sentiment(item, topic),
                generated_summary=summarize_text(text),
            )

            session.add(article)
            count += 1

            if count % 5 == 0:
                session.commit()

        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    store_articles()
