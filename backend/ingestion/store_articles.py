from sqlalchemy.exc import IntegrityError
from backend.storage.database import SessionLocal, Article
from backend.ingestion.rss_fetcher import fetch_articles
from backend.nlp.topic_classifier import classify_topic
from backend.nlp.sentiment import analyze_sentiment
from backend.nlp.summarizer import summarize_text
from datetime import datetime
import gc

def store_articles(batch_size=5):
    articles = fetch_articles()
    session = SessionLocal()
    count = 0
    added_count = 0

    for item in articles:
        # Skip duplicates
        if session.query(Article).filter_by(link=item.get("link")).first():
            continue

        # Ensure we have a text to process
        text = item.get("summary") or item.get("title") or ""

        # Ensure fetched_at is datetime
        fetched_at = item.get("fetched_at")
        if isinstance(fetched_at, str):
            try:
                fetched_at = datetime.fromisoformat(fetched_at)
            except:
                fetched_at = datetime.utcnow()
        elif not fetched_at:
            fetched_at = datetime.utcnow()

        try:
            # NLP with safe fallback
            topic = classify_topic(text) or "GENERAL"
            sentiment = analyze_sentiment(item, topic) or "LABEL_NEUTRAL"
            summary = summarize_text(text) or text[:130]

            article = Article(
                title=item.get("title") or "No Title",
                summary=item.get("summary") or "",
                link=item.get("link") or f"no-link-{count}",
                source=item.get("source") or "Unknown",
                published=item.get("published"),
                fetched_at=fetched_at,
                topic=topic,
                sentiment=sentiment,
                generated_summary=summary,
                processed=True
            )

            session.add(article)
            count += 1
            added_count += 1

            if count % batch_size == 0:
                try:
                    session.commit()
                except IntegrityError:
                    session.rollback()
                except Exception as e:
                    session.rollback()
                    print(f"Batch commit error: {e}")

        except Exception as e:
            print(f"Error processing article '{item.get('title', '')}': {e}")
            continue

    # Commit remaining articles
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Final commit error: {e}")

    session.close()
    gc.collect()
    print(f"Fetched {len(articles)} articles, added {added_count} new")
