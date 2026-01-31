from apscheduler.schedulers.background import BackgroundScheduler
from backend.services.ingest import fetch_and_store_articles
from backend.services.nlp_worker import process_unprocessed_articles

def start_scheduler():
    scheduler = BackgroundScheduler()

    # RSS ingestion 
    scheduler.add_job(
        fetch_and_store_articles,
        trigger="interval",
        minutes=15,
        id="rss_ingestion",
        replace_existing=True
    )

    # NLP processing 
    scheduler.add_job(
        process_unprocessed_articles,
        trigger="interval",
        minutes=10,
        id="nlp_processing",
        replace_existing=True
    )

    scheduler.start()
