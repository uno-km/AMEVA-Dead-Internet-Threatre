import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///./ameva_society.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from src.db.models import BotState
    Base.metadata.create_all(bind=engine)
    # Initialize bot states if empty
    db = SessionLocal()
    if db.query(BotState).count() == 0:
        bots = ["bot_1", "bot_2", "bot_3"]
        for b in bots:
            db.add(BotState(bot_name=b, anger_targets="{}"))
        db.commit()
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
