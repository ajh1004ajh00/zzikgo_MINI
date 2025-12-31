from fastapi import HTTPException
from typing import Optional

class CustomErrorException(HTTPException):
    def __init__(self, status_code: int, message: str, error_code: Optional[str] = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.error_code = error_code
