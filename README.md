# 집찍고 MINI · 백엔드 실습

집찍고 도메인을 바탕으로 FastAPI·SQLAlchemy·PostgreSQL을 학습한 작은 실습 저장소입니다.
실제 운영 서비스 코드나 폴더 순환 참조 장애 수정본 전체를 공개한 저장소는 아닙니다.

## 살펴볼 내용

- 플랫폼·사용자 등록과 JWT 발급·해석 흐름
- 사용자·폴더·이미지 등 데이터 모델과 관계
- Item API, SQLAlchemy 조회 및 Alembic 마이그레이션 기록
- 별도 `tool_agent.py`와 `tools.yaml`의 DB 도구 연동 실습

## 로컬 실행

Docker Compose가 필요합니다.

1. `.env.example`을 `.env`로 복사합니다.
2. `.env`의 `DB_PASS`와 `JWT_SECRET_KEY`를 본인의 로컬용 값으로 바꿉니다.
3. `docker compose up --build`를 실행합니다.
4. `http://localhost:8000/docs`에서 API를 확인합니다.

빈 DB 볼륨으로 최초 실행할 때 `db-image/example.sql`의 스키마와 가상 데이터가 입력됩니다.
예제는 `example-platform`, `example-user`, `example-root` 등의 가상 식별자만 사용합니다.
기존 볼륨에는 초기화 SQL이 다시 실행되지 않습니다.

## 공개 데이터 구성

기존 PostgreSQL 데이터 디렉터리·SQL 덤프·SQLite DB를 제거하고 모델 정의로 만든 스키마와
가상 예제로 대체했습니다. 기존 접속값·서명 키·DB 파일은 공개 브랜치의 과거 커밋에서도 정리했습니다.
실행 중 생성되는 DB와 `.env`는 Git에 포함하지 않습니다.

## 실습 범위

이 코드는 학습 당시의 구현을 보존합니다. JWT 만료 검증이 꺼진 부분 등 운영 배포 전에
보완할 내용이 있으므로 로컬 실습용으로 사용합니다. Compose 포트도 로컬 호스트에만 바인딩합니다.
AI 도구 실습은 별도의 Google API 키와 ADK·Toolbox 실행 환경이 필요하며 기본 Compose에는 포함되지 않습니다.

## 예제 검증

`python scripts/build_example.py --check`로 모델 스키마와 예제 SQL의 일치 여부,
가상 데이터 입력과 외래키 관계를 메모리 SQLite에서 검사할 수 있습니다.
공개 준비 시 이 검사는 통과했으며, Docker·PostgreSQL 컨테이너 실행은 별도 검증이 필요합니다.
