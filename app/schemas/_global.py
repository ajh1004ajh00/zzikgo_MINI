from pydantic   import BaseModel
from typing     import List, Optional, TypeVar, Generic


T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status_code: int
    error_code: Optional[str] = None
    message: str
    result: T

class TokenPayload(BaseModel):
    sub: str
    platform: str
    created_at: str
    perm: str

class UserTokenPayload(BaseModel):
    sub: str
    platform_id: str
    created_at: str
    perm: str

class PlatformTokenPayload(BaseModel):
    sub: str
    # created_at: str
    # perm: str
    created_at: Optional[str] = None
    perm: Optional[str] = None