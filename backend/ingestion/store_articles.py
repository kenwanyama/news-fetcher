from backend.storage.database import SessionLocal, Article, init_db
from backend.ingestion.rss_fetcher import fetch_articles

def store_articles():
    init_db()
    session = SessionLocal()

    articles = fetch_articles()

    for item in articles:
        exists = session.query(Article).filter_by(link=item["link"]).first()
        if exists:
            continue

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
    session.close()

if __name__ == "__main__":
    store_articles()
