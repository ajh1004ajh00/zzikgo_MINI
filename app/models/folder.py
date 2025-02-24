import shortuuid

from sqlalchemy             import Column, String, ForeignKey
from sqlalchemy.orm         import relationship, backref

from app.database.engine    import Base


class Folder(Base):
    __tablename__ = 'folders'

    id = Column(String, primary_key=True, unique=True)
    title = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey('folders.id'), index=True)
    user_id = Column(String, ForeignKey('users.id'), index=True)
    created_at = Column(String)
    updated_at = Column(String)
    delete_at = Column(String, nullable=True, index=True) 

    user = relationship('User', back_populates='folders')  

    parent_folder = relationship('Folder', remote_side=[id], backref=backref('child_folders', cascade='all, delete-orphan'))
    images = relationship('MyImage', cascade='all, delete-orphan', back_populates='folder')
    
    def __init__(self, title, parent_id, user_id, created_at, updated_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.title = title
        self.parent_id = parent_id
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at