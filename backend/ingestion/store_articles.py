from sqlalchemy.exc import IntegrityError
from backend.storage.database import SessionLocal, Article
from backend.ingestion.rss_fetcher import fetch_articles
from backend.nlp.topic_classifier import classify_topic
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.summarizer import summarize_text
import gc

def store_articles(batch_size=5):
    articles = fetch_articles()
    session = SessionLocal()
    count = 0
    added_count = 0

    for item in articles:
        # Skip if article already exists
        if session.query(Article).filter_by(link=item["link"]).first():
            continue

        text = item["summary"] or item["title"]

        try:
            # NLP processing
            topic = classify_topic(text)
            sentiment = analyze_sentiment(item, topic)
            summary = summarize_text(text)

            # Create Article with NLP fields
            article = Article(
                title=item["title"],
                summary=item["summary"],
                link=item["link"],
                source=item["source"],
                published=item["published"],
                fetched_at=item["fetched_at"],
                topic=topic,
                sentiment=sentiment,
                generated_summary=summary,
                processed=True
            )

            session.add(article)
            count += 1
            added_count += 1

            # Commit every batch_size articles
            if count % batch_size == 0:
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    print(f"Error committing batch: {e}")

        except Exception as e:
            # Log errors 
            print(f"Error processing article '{item.get('title', '')}': {e}")
            continue

    # Final commit for remaining articles
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
    except Exception as e:
        session.rollback()
        print(f"Error committing final batch: {e}")

    session.close()
    gc.collect()
    print(f"Fetched {len(articles)} articles, added {added_count} new")


if __name__ == "__main__":
    store_articles()
