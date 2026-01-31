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
     

            article = Article(
                title=item["title"],
                summary=item["summary"],
                link=item["link"],
                source=item["source"],
                published=item["published"],
                fetched_at=item["fetched_at"]
            )

            session.add(article)
          
        session.commit()

    except Exception:
        session.rollback()
    finally:
        print(f"Fetched {len(articles)} articles")
        session.close()

def processing_articles(limit=3):
    session = SessionLocal()

    articles = (
        session.query(Article)
        .filter(Article.processed == False)
        .limit(limit)
        .all()
    )

    for article in articles:
        text = article.summary or article.title

        topic = classify_topic(text)
        sentiment = analyze_sentiment(
            {"title": article.title, "summary": article.summary}, topic
        )
        summary = summarize_text(text)

        article.topic = topic
        article.sentiment = sentiment
        article.generated_summary = summary
        article.processed = True

        session.commit()

    session.close()




if __name__ == "__main__":
    store_articles()
