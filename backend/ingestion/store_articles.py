from sqlalchemy.exc import IntegrityError

def store_articles():
    articles = fetch_articles()
    session = SessionLocal()
    count = 0

    for item in articles:
        # Skip if article already exists
        if session.query(Article).filter_by(link=item["link"]).first():
            continue

        text = item["summary"] or item["title"]

        try:
            # NLP processing
            topic = classify_topic(text)
            sentiment = analyze_sentiment(
                {"title": item["title"], "summary": item["summary"]}, 
                topic
            )
            summary = summarize_text(text)

            # Create article object
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

            # Add to session
            session.add(article)
            count += 1

        except Exception as e:
            
            print(f"Error processing article '{item.get('title', 'N/A')}': {e}")
            continue

    
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Duplicate article detected, rollback performed")
    except Exception as e:
        session.rollback()
        print(f"Error committing to database: {e}")
    finally:
        print(f"Fetched {len(articles)} articles, added {count} new")
        session.close()
