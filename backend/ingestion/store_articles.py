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
            # Skip if article already exists
            if session.query(Article).filter_by(link=item["link"]).first():
                continue
            
            text = item["summary"] or item["title"]
            
            #NLP processing
            topic = classify_topic(text)
            sentiment = analyze_sentiment(
                {"title": item["title"], "summary": item["summary"]}, 
                topic
            )
            summary = summarize_text(text)
            
            # Create article with NLP data already included
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
          
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error storing/processing articles: {e}")
    finally:
        print(f"Fetched {len(articles)} articles, added {new_count} new")
        session.close()

