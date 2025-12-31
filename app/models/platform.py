import shortuuid

from sqlalchemy             import Column, String, DateTime

from app.database.engine    import Base


class Platform(Base):
    __tablename__ = 'platforms'

    id = Column(String, primary_key=True, unique=True)
    platform = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    # created_at = Column(DateTime(timezone=True), nullable=False)
    # updated_at = Column(DateTime(timezone=True), nullable=False)

    
    def __init__(self, platform, created_at, updated_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.platform = platform
        self.created_at = created_at
        self.updated_at = updated_at
