# app/main.py
import logging
from fastapi import FastAPI
from app.database.engine import engine, Base
from app.routes import router as router  
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.routing import APIRoute

Base.metadata.create_all(bind=engine)

app = FastAPI()
# 라우터 포함
app.include_router(router, prefix="/api")