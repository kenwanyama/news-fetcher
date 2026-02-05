from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from backend.storage.database import Article, SessionLocal
from backend.app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(title="News Feed", lifespan=lifespan)


# Allow React frontend to access
origins = [
    "http://localhost:3000",
    "https://brief-ly.vercel.app/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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


@app.get("/articles/trends", response_class=JSONResponse)
def get_trends(db: Session = Depends(get_db)):
    # Count articles per topic
    topics = db.query(Article.topic).all()

    topic_counts = {}


    for t in topics:
        topic_counts[t[0]] = topic_counts.get(t[0], 0) + 1


    return {"topic_counts": topic_counts}
