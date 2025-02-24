import shortuuid

from sqlalchemy             import Column, ForeignKey, Integer, String, DateTime
from datetime               import datetime
from sqlalchemy.orm         import relationship

from app.database.engine    import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, unique=True)
    platform_id = Column(String, ForeignKey('platforms.id'), index=True)
    platform_user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    max_storage_mb = Column(Integer, default=10240)

    folders = relationship('Folder', back_populates='user')
    # images = relationship("MyImage", back_populates="user", cascade="all, delete-orphan")
    images = relationship("MyImage", back_populates="user")

    def __init__(self, platform_id, platform_user_id, created_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.platform_id = platform_id
        self.platform_user_id = platform_user_id
        self.created_at = created_at

