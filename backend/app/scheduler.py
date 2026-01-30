def start_scheduler():
    from backend.ingestion.store_articles import store_articles

    store_articles()


    scheduler = BackgroundScheduler()
    scheduler.add_job(
        store_articles,
        "interval",
        minutes=30,
        id="news_ingestion",
        replace_existing=True
    )
    scheduler.start()
