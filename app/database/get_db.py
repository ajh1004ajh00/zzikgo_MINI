# app/database/get_db.py

from fastapi import HTTPException

from app.database.engine import SessionLocal


def get_db():
    try:
        db = SessionLocal()
    except Exception as e:
        print(f"Failed to create a database session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database.")
    
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            print(f"Failed to close the database session: {str(e)}")