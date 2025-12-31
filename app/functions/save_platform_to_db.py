from fastapi            import HTTPException
from sqlalchemy.exc     import SQLAlchemyError

from app.models         import Platform

    
def save_platform_to_db(db, platform_name, created_at, updated_at):
    try:
        platform = Platform(
            platform=platform_name,
            created_at=created_at,
            updated_at=updated_at
        )
        db.add(platform)
        db.commit()
        return platform
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occurred while saving platform:", str(e))
        raise HTTPException(status_code=500, detail="Database error occurred while saving platform") from e
