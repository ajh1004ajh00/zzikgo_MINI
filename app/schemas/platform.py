from pydantic import BaseModel
from datetime import datetime


class PlatformTokenResponse(BaseModel):
    id: str
    platform: str
    created_at: datetime
    updated_at: datetime
    access_token: str
    refresh_token: str
    token_type: str
    
    class Config:
        from_attributes = True

class Platform(BaseModel):
    id: str
    platform: str
    created_at: datetime
    updated_at: datetime

    class Config:
        #orm_mode = True  # SQLAlchemy 모델과의 호환성을 위해 설정
        from_attributes = True
