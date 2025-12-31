from fastapi            import HTTPException
from sqlalchemy.exc     import SQLAlchemyError

from app.models         import User

    
def save_user_to_db(db, platform_id, platform_user_id, created_at):
    try:
        user = User(
            platform_id=platform_id,
            platform_user_id=platform_user_id,
            created_at=created_at
        )
        db.add(user)
        db.commit()
        return user
    except SQLAlchemyError as e:
        db.rollback()
        print("Error occurred while saving user:", str(e))
        raise HTTPException(status_code=500, detail="Database error occurred while saving user") from e
