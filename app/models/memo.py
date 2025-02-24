import shortuuid

from sqlalchemy             import Column, String, Boolean, ForeignKey
from sqlalchemy.orm         import relationship

from app.database.engine    import Base


class Memo(Base):
    __tablename__ = 'memos'

    id = Column(String, primary_key=True, unique=True)
    image_id = Column(String, ForeignKey('images.uuid'), index=True)
    message = Column(String)
    is_client = Column(Boolean, nullable=False)
    created_at = Column(String)
    updated_at = Column(String)

    image = relationship("MyImage", back_populates="memos")
    
    def __init__(self, image_id, message, is_client, created_at, updated_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.image_id = image_id
        self.message = message
        self.is_client = is_client
        self.created_at = created_at
        self.updated_at = updated_at