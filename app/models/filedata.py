import uuid

from sqlalchemy         import Column, String, Float, ForeignKey
from sqlalchemy.orm     import relationship

from app.database.engine        import Base


class FileData(Base):
    __tablename__ = 'filedata'

    uuid = Column(String, primary_key=True, unique=True)
    org_image_id = Column(String, ForeignKey('images.uuid'), index=True)
    s3_info = Column(String)
    s3_filepath = Column(String)
    filename = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), index=True)
    filesize = Column(Float)
    image_resource_type = Column(String)
    created_at = Column(String, index=True)
    updated_at = Column(String)
    hashdata = Column(String)
    resolution = Column(String)
    
    image = relationship("MyImage", back_populates="filedata_list")
    
    def __init__(self, org_image_id, s3_info, s3_filepath, filename, user_id, filesize, image_resource_type, created_at, updated_at, hashdata, resolution):
        self.uuid = str(uuid.uuid4())
        self.org_image_id = org_image_id
        self.s3_info = s3_info
        self.s3_filepath = s3_filepath
        self.filename = filename
        self.user_id = user_id
        self.filesize = filesize
        self.image_resource_type = image_resource_type
        self.created_at = created_at
        self.updated_at = updated_at 
        self.hashdata =hashdata
        self.resolution = resolution
    
