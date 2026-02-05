from apscheduler.schedulers.background import BackgroundScheduler
from backend.ingestion.store_articles import store_articles

def start_scheduler():
    scheduler = BackgroundScheduler()

    # RSS ingestion 
    scheduler.add_job(
        store_articles,
        trigger="interval",
        minutes=15,
        id="rss_ingestion",
        replace_existing=True,
        
    )

    scheduler.start()


    try:
        store_articles()
    except Exception as e:
        print(f"Error during initial fetch: {e}")
