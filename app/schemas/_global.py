from pydantic   import BaseModel
from typing     import List, Optional, TypeVar, Generic


T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status_code: int
    error_code: Optional[str] = None
    message: str
    result: T
