# app/routes/__init__.py

from fastapi import APIRouter

from app.routes.user import router as user_router
from app.routes.item import router as item_router
from app.schemas.error          import CustomErrorException
from app.routes.error.error     import custom_error_exception_handler
from app.routes.platform import router as platform_router


router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(item_router, prefix="/items", tags=["items"])
router.include_router(platform_router, prefix="/platforms", tags=["platforms"])