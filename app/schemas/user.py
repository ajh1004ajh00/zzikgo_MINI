from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    platform_id: str
    platform_user_id: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델과의 호환성을 위해 설정
