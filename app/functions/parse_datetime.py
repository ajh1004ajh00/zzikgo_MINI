from datetime import datetime

def parse_datetime(dt):
    if isinstance(dt, str):
        # 예: '2025-07-02 15:26:28.723342+09'
        try:
            return datetime.fromisoformat(dt)
        except Exception:
            # 필요시 다른 포맷도 시도
            return None
    return dt