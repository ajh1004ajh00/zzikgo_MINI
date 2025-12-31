import shortuuid
from sqlalchemy import Column, Integer, String
from app.database.engine import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=False)
    located = Column(String)

    def __init__(self, name):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.name = name