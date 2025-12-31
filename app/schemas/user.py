from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    platform_id: str
    platform_user_id: str
    created_at: datetime
    max_storage_mb: int | None = None

    class Config:
        #orm_mode = True  # SQLAlchemy 모델과의 호환성을 위해 설정
        from_attributes = True


class UserTokenResponse(BaseModel):
    user_id: str
    platform_id: str
    platform_user_id: str
    created_at: datetime
    max_storage_mb: int | None = None
    
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True