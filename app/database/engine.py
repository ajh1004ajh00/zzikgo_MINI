# app/database/engine.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:///./zzikgo_mini_sqlite.db") # "POSTGRE_DATABASE_URL", "postgresql://postgres:1234@localhost:5434/postgres"
# DATABASE_URL = "postgresql://example_user:example_password@localhost:5432/postgres"
DB_USER = os.getenv("DB_USER", "example_user")
DB_PASS = os.getenv("DB_PASS", "example_password")
#DB_HOST = os.getenv("DB_HOST", "localhost")
DB_HOST = "localhost"
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL) #POSTGRE_DATABASE_URL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
