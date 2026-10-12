"""
PHISHGUARD//NEXUS - Database Session & Engine Configuration
"""

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.config import settings
from backend.app.db.models import Base

# Ensure SQLite parent directory exists
if settings.DATABASE_URL.startswith("sqlite"):
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    Path(db_path).resolve().parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
