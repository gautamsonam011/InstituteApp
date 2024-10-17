from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from core.config import XpertsTax_config
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.ext.declarative import declarative_base



SQLALCHEMY_DATABASE_URL = XpertsTax_config.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

sessionmaker = FastAPISessionMaker(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_cron_db():
    with sessionmaker.context_session() as db:
        return db