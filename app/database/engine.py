import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = URL.create(
    'postgresql', username=os.getenv('DB_USER', 'example_user'),
    password=os.environ['DB_PASS'], host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '5433')), database=os.getenv('DB_NAME', 'example_db'),
)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
