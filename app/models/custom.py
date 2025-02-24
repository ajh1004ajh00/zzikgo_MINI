import shortuuid

from sqlalchemy             import Column, String, ForeignKey
from sqlalchemy.orm         import relationship

from app.database.engine    import Base


class Custom(Base):
    __tablename__ = 'customs'

    id = Column(String, primary_key=True, unique=True)
    image_id = Column(String, ForeignKey('images.uuid'), index=True)
    key = Column(String)
    value = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    
    image = relationship("MyImage", back_populates="customs")
    
    def __init__(self, image_id, key, value, created_at, updated_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.image_id = image_id
        self.key = key
        self.value = value
        self.created_at = created_at
        self.updated_at = updated_at