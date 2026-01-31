from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    link = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    published = Column(String, nullable=True)
    fetched_at = Column(DateTime, nullable=False)

    # to be loaded later 
    topic = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    generated_summary = Column(Text, nullable=True)

    # processing state
    processed = Column(Boolean, default=False, nullable=False)



