from apscheduler.schedulers.background import BackgroundScheduler
from backend.ingestion.store_articles import store_articles

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        store_articles,
        "interval",
        minutes=30,
        id="news_ingestion",
        replace_existing=True
    )
    scheduler.start()
