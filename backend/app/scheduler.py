def start_scheduler():
    from backend.ingestion.store_articles import store_articles processing_articles

    # Run immediately on startup
    try:
        store_articles()
    except Exception as e:
        print("Startup fetch/store failed:", e)

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        store_articles,
        "interval",
        minutes=30,
        id="news_ingestion",
        replace_existing=True
    )
    scheduler.start()
