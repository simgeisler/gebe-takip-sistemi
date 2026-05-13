from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    if SessionLocal is None:
        raise ValueError("DATABASE_URL environment variable is not set")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
