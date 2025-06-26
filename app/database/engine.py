# app/database/engine.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./zzikgo_mini_sqlite.db") # "POSTGRE_DATABASE_URL", "postgresql://postgres:1234@localhost:5434/postgres"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False}) #POSTGRE_DATABASE_URL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
