# app/auth.py
import time
import os

from fastapi    import HTTPException, Header, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.schemas.error import CustomErrorException
from app.schemas._global    import TokenPayload, UserTokenPayload, PlatformTokenPayload

SECRET_KEY = "example_only_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def generate_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": int(expire.timestamp())})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        print("토큰 생성 중 오류:", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT 생성 중 오류가 발생했습니다."
        ) from e

def generate_access_token(
    user_id: str,
    platform_id: str | None,
    created_at: datetime,
    perm: str
) -> str:
    # 만료 시간 계산
    access_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 반드시 ISO-8601 문자열로 변환
    created_at_iso = created_at.isoformat()

    if perm == "platform":
        data = {
            "sub": platform_id,
            "platform_id": None,
            "created_at": created_at_iso,
            "perm": "platform",
        }
    elif perm == "user":
        data = {
            "sub": user_id,
            "platform_id": platform_id,
            "created_at": created_at_iso,
            "perm": "user",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid perm value: {perm}"
        )

    return generate_token(data, access_expires)

def generate_refresh_token(
    user_id: str,
    platform_id: str | None,
    created_at: datetime,
    perm: str
) -> str:
    refresh_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    created_at_iso = created_at.isoformat()

    if perm == "platform":
        data = {
            "sub": platform_id,
            "platform_id": None,
            "created_at": created_at_iso,
            "perm": "platform",
        }
    elif perm == "user":
        data = {
            "sub": user_id,
            "platform_id": platform_id,
            "created_at": created_at_iso,
            "perm": "user",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid perm value: {perm}"
        )

    return generate_token(data, refresh_expires)

def decode_token_jwt(
    authorization: str = Header(...)
) -> TokenPayload | PlatformTokenPayload | UserTokenPayload:

    if not authorization or not authorization.strip():
        raise CustomErrorException(
            status_code=400,
            message="Authorization 헤더가 없습니다.",
            error_code="MISSING_AUTH_HEADER"
        )

    try:
        prifix, token = authorization.split(" ", 1)
    except ValueError:
        raise CustomErrorException(
            status_code=400,
            message="잘못된 Authorization 헤더 형식입니다.",
            error_code="INVALID_AUTH_HEADER"
        )

    # 3) Bearer만 허용
    if prifix.lower() != "bearer":
        raise CustomErrorException(
            status_code=400,
            message=f"허용되지 않는 토큰입니다: {prifix}",
            error_code="INVALID_TOKEN_PREFIX"
        )

    # 4) JWT 서명 및 페이로드 파싱
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False}  # exp 검증이 필요하면 True로 바꾸세요
        )
    except JWTError:
        raise CustomErrorException(
            status_code=401,
            message="유효하지 않은 토큰입니다.",
            error_code="INVALID_TOKEN"
        )

    # 5) perm 클레임에 따라 Pydantic 모델 선택
    perm = payload.get("perm")
    # if perm == "admin":
    #     return TokenPayload(**payload)
    if perm == "platform":
        return PlatformTokenPayload(**payload)
    elif perm == "user":
        return UserTokenPayload(**payload)
    else:
        raise CustomErrorException(
            status_code=400,
            message=f"알 수 없는 perm 값입니다: {perm}",
            error_code="INVALID_TOKEN_PAYLOAD"
        )