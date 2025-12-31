# app/routes/item.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.get_db import get_db
from app.functions.get_korea_timezone import get_korea_timezone
from app.functions.save_platform_to_db import save_platform_to_db
from app.functions.auth import generate_access_token, generate_refresh_token
from app.functions.parse_datetime import parse_datetime

from app.models import Platform as PlatformModel
from app.schemas._global import ApiResponse
from app.schemas.platform import PlatformTokenResponse

router = APIRouter()

@router.post("/", response_model=ApiResponse[PlatformTokenResponse])
def create_platform(
    token_payload: str,  # = platform name
    db: Session = Depends(get_db)
):
    perm = "platform"
    temp_id = None
    platform_name = token_payload

    existing = db.query(PlatformModel).filter(
        PlatformModel.platform == platform_name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Platform already exists."
        )

    now = datetime.now(get_korea_timezone())

    try:
        platform = save_platform_to_db(db, platform_name, now, now)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="플랫폼 생성 중 오류가 발생했습니다."
        )

    # platform의 created_at와 updated_at은 string => datatime 구조로 변환
    # created_at_dt = parse_datetime(platform.created_at)
    # updated_at_dt = parse_datetime(platform.updated_at)
    created_at_dt = platform.created_at
    updated_at_dt = platform.updated_at

    access_token = generate_access_token(
        temp_id, platform.id, created_at_dt, perm
    )
    refresh_token = generate_refresh_token(
        temp_id, platform.id, created_at_dt, perm
    )

    platform_data = PlatformTokenResponse(
        id=str(platform.id),
        platform=platform.platform,
        created_at=created_at_dt,
        updated_at=updated_at_dt,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

    return ApiResponse(
        status_code=status.HTTP_200_OK,
        message="성공",
        result=platform_data
    )
