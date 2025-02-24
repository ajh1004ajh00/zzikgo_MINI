from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User, Platform
from app.schemas._global import ApiResponse
from app.schemas.user import UserResponse
from app.database.get_db import get_db


router = APIRouter()

@router.get("/", response_model=ApiResponse[List[UserResponse]])
def read_users(platform_id: str, db: Session = Depends(get_db)):
    # 플랫폼 존재 여부 확인
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Platform with id {platform_id} not found."
        )
    
    # 해당 플랫폼의 사용자 조회
    platform_users = db.query(User).filter(User.platform_id == platform.id).all()

    response_users = []
    for user in platform_users:
        # created_at의 타입과 값 출력 (디버깅용)
        print(f"User ID: {user.id}, created_at type: {type(user.created_at)}, value: {user.created_at}")
        
        # created_at이 datetime 객체인지 확인
        if isinstance(user.created_at, datetime):
            created_at_value = user.created_at
        else:
            # 만약 문자열이라면, datetime으로 변환 시도
            try:
                created_at_value = datetime.strptime(user.created_at, "%Y%m%d_%H%M%S")
            except (ValueError, TypeError):
                # 다른 포맷이거나 변환할 수 없는 경우 처리
                print(f"Error: Unable to parse created_at for user {user.id}")
                created_at_value = None  # 또는 적절한 기본값 설정
                
        # UserResponse 객체 생성
        user_response = UserResponse(
            id=user.id,
            platform_id=user.platform_id,
            platform_user_id=user.platform_user_id,
            created_at=created_at_value,  # Optional[datetime]으로 설정 시 None 허용
            max_storage_mb=user.max_storage_mb
        )
        response_users.append(user_response)

    response_model = ApiResponse(
        status_code=200,
        message="성공",
        result=response_users
    )
    
    return response_model 