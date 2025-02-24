# app/routes/__init__.py

from fastapi import APIRouter

from app.routes.user import router as user_router


router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
