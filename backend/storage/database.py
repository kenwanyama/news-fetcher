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
    id = Column(Integer, primary_key=True)
    title = Column(String)
    summary = Column(Text)
    link = Column(String, unique=True)
    source = Column(String)
    published = Column(String)
    fetched_at = Column(DateTime)
    topic = Column(String)
    sentiment = Column(String)
    generated_summary = Column(Text)

