from fastapi import FastAPI, HTTPException, Depends
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from backend.storage.database import SessionLocal, Article, init_db
from backend.app.scheduler import start_scheduler

from fastapi.responses import JSONResponse
# Initialize DB 
init_db()



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    yield

app = FastAPI(title="News Feed", lifespan=lifespan)

# Allow your React frontend to access
origins = [
    "http://localhost:3000",  # local React dev
    "https://kenwanyama.vercel.app"  # production portfolio
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

@app.get("/articles", response_class=JSONResponse)
def get_articles(limit: int = 50, db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.fetched_at.desc()).limit(limit).all()
    return [{
            "title": a.title,
            "summary": a.summary,
            "link": a.link,
            "source": a.source,
            "published": a.published,
            "fetched_at": str(a.fetched_at),
            "topic": a.topic,
            "sentiment": a.sentiment,
            "generated_summary": a.generated_summary
        } for a in articles
        ]

@app.get("/articles/topic/{topic_name}", response_class=JSONResponse)
def get_articles_by_topic(topic_name: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.topic==topic_name).all()
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this topic")
    return [{
            "title": a.title,
            "summary": a.summary,
            "link": a.link,
            "source": a.source,
            "published": a.published,
            "fetched_at": str(a.fetched_at),
            "topic": a.topic,
            "sentiment": a.sentiment,
            "generated_summary": a.generated_summary
        } for a in articles
        ]

@app.get("/articles/sentiment/{sentiment_label}", response_class=JSONResponse)
def get_articles_by_sentiment(sentiment_label: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.sentiment==sentiment_label).all()
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found for this sentiment")
    return [{
            "title": a.title,
            "summary": a.summary,
            "link": a.link,
            "source": a.source,
            "published": a.published,
            "fetched_at": str(a.fetched_at),
            "topic": a.topic,
            "sentiment": a.sentiment,
            "generated_summary": a.generated_summary
        } for a in articles
    ]

@app.get("/articles/trends", response_class=JSONResponse)
def get_trends(db: Session = Depends(get_db)):
    # Count articles per topic
    topics = db.query(Article.topic).all()
    sentiments = db.query(Article.sentiment).all()

    topic_counts = {}
    sentiment_counts = {}

    for t in topics:
        topic_counts[t[0]] = topic_counts.get(t[0], 0) + 1

    for s in sentiments:
        sentiment_counts[s[0]] = sentiment_counts.get(s[0], 0) + 1

    return {"topic_counts": topic_counts, "sentiment_counts": sentiment_counts}
