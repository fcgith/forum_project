import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SISO_FORUM_DB_USER = os.getenv("SISO_FORUM_DB_USER")
SISO_FORUM_DB_PASSWORD = os.getenv("SISO_FORUM_DB_PASSWORD")
SISO_FORUM_DB_HOST = os.getenv("SISO_FORUM_DB_HOST")
SISO_FORUM_DB_PORT = os.getenv("SISO_FORUM_DB_PORT")
SISO_FORUM_DB_NAME = os.getenv("SISO_FORUM_DB_NAME")

SQLALCHEMY_DATABASE_URL =\
    f"postgresql+psycopg2://{SISO_FORUM_DB_USER}:{SISO_FORUM_DB_PASSWORD}@{SISO_FORUM_DB_HOST}:{SISO_FORUM_DB_PORT}/{SISO_FORUM_DB_NAME}"

engine = create_engine\
(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()