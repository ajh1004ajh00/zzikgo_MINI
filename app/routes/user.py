import shortuuid
from fastapi.encoders   import jsonable_encoder
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.models import User, Platform
from app.schemas._global import ApiResponse
from app.schemas.user import UserResponse, UserTokenResponse
from app.database.get_db import get_db
from app.functions.auth import *
from app.functions.get_korea_timezone import get_korea_timezone
from app.functions.save_user_to_db import save_user_to_db

router = APIRouter()

@router.post("/", response_model=ApiResponse[UserTokenResponse]) 
def create_user(
    platform_id: str,
    Platform_user_id: str = Form(..., min_length=1),
    #Platform_user_id: str,
    token_payload: PlatformTokenPayload = Depends(decode_token_jwt),
    db: Session = Depends(get_db)
):
    try:
        sub = token_payload.sub
        if sub != platform_id:
            raise HTTPException(status_code=400, detail="Token does not match the platform_id.")

        platform = db.query(Platform).filter(Platform.id == platform_id).first()
        if not platform:
            raise HTTPException(status_code=404, detail="Platform not found")

        perm = "user"
        now = datetime.now(get_korea_timezone())
        # korea_timezone = get_korea_timezone()
        # created_at = datetime.now(korea_timezone)
               
        user = save_user_to_db(db, platform.id, Platform_user_id, now)

        access_token = generate_access_token(user.id, user.platform_id, user.created_at, perm)
        refresh_token = generate_refresh_token(user.id, user.platform_id, user.created_at, perm)
               
        token_response_model = UserTokenResponse(
            user_id=user.id,
            platform_id=platform.id,
            platform_user_id=Platform_user_id,
            created_at=now,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
        response_model = ApiResponse(
            status_code=200,
            message="성공",
            result=token_response_model   
        )
        return jsonable_encoder(response_model)
    except HTTPException as e:
        print(f"An error occurred: {e.detail}")
        response_model = ApiResponse(
            status_code=e.status_code,
            message=e.detail, 
            result=None
        )
        return response_model
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        response_model = ApiResponse(
            status_code=500,
            message="유저 생성 중 오류가 발생했습니다.", 
            result=None
        )
        return response_model

@router.get("/", response_model=ApiResponse[List[UserResponse]])
def read_users(
    platform_id: str,
    token_payload: PlatformTokenPayload = Depends(decode_token_jwt),
    db: Session = Depends(get_db)
):
    sub = token_payload.sub # sub는 user_id임 platform_id 아님
    if sub != platform_id:
        raise HTTPException(status_code=400, detail="Token does not match the platform_id.")    
    
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
        user_response = UserResponse.model_validate(user)
        response_users.append(user_response)

    response_model = ApiResponse(
        status_code=200,
        message="성공",
        result=response_users
    )
    
    return response_model 

@router.delete("/", response_model=ApiResponse[UserResponse])
def delete_user(
    user_id: str,
    token_payload: PlatformTokenPayload = Depends(decode_token_jwt),
    db: Session = Depends(get_db)
):
    perm = token_payload.perm
    if perm == "user":
        if user_id != token_payload.sub:
            raise HTTPException(status_code=400, detail="Token does not match the user_id.")
    
    # perm = token_payload.perm
    # if perm != "admin":
    #     raise HTTPException(status_code=403, detail="Token permissions are invalid.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID is not found {user_id}"
        )
    db.delete(user)
    db.commit()
    user_response = UserResponse.model_validate(user)
    return ApiResponse(
        status_code=200,
        message="삭제됨",
        result=user_response
    )

@router.put("/", response_model=ApiResponse[UserResponse])
def put_user(
    user_id: str,
    max_storage: int,
    token_payload: PlatformTokenPayload = Depends(decode_token_jwt),
    db: Session = Depends(get_db)):

    # sub = token_payload.sub
    # if sub != user_id:
    #     raise HTTPException(status_code=400, detail="Token does not match the platform_id.")    
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User ID is not found {user_id}"
        )
    user.max_storage_mb = max_storage
    db.commit()
    user_response = UserResponse.model_validate(user)
    
    return ApiResponse(
        status_code=200,
        message="수정됨",
        result=user_response
    )