# app/main.py

import logging
from fastapi import FastAPI
from app.database.engine import engine, Base
from app.routes import router as router  


# 모든 모델을 기반으로 데이터베이스 테이블을 생성.
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 포함
app.include_router(router, prefix="/api")