from fastapi            import Request
from fastapi.responses  import JSONResponse

from app.schemas.error  import CustomErrorException


async def custom_error_exception_handler(request: Request, exc: CustomErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status_code": exc.status_code,
            "error_code": exc.error_code,
            "message": exc.message,
            "result": None
        },
    )
