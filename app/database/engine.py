# app/database/engine.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

POSTGRE_DATABASE_URL = os.getenv("POSTGRE_DATABASE_URL", "postgresql://postgres:5501@192.168.45.145:5432/postgres")

engine = create_engine(POSTGRE_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
