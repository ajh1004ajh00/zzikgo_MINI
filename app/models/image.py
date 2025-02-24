import uuid

from sqlalchemy             import JSON, Column, ForeignKey, String, Float, Boolean, null
from sqlalchemy.orm         import relationship

from app.database.engine    import Base


class MyImage(Base):
    __tablename__ = 'images'

    uuid = Column(String, primary_key=True, unique=True)
    s3_info = Column(String)
    s3_filepath = Column(String)
    filename = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), index=True)
    folder_id = Column(String, ForeignKey('folders.id'), index=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    filesize = Column(Float)
    image_resource_type = Column(String)
    created_at = Column(String, index=True)
    updated_at = Column(String)
    delete_at = Column(String, nullable=True, index=True)
    address_road = Column(String)
    address_land = Column(String)
    address_land_number = Column(String, nullable=True)
    building_name = Column(String)
    address_det = Column(String)
    address_search = Column(String, index=True)
    address_sort = Column(String, index=True)
    is_signed = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    has_det = Column(Boolean, nullable=True)

    user = relationship("User", back_populates="images")    
    folder = relationship("Folder", back_populates="images")
    
    filedata_list = relationship("FileData", order_by="FileData.created_at", cascade="all, delete-orphan", back_populates="image")    
    memos = relationship("Memo", cascade="all, delete-orphan", back_populates="image")
    customs = relationship("Custom", cascade="all, delete-orphan", back_populates="image")    
    
    def __init__(self, s3_info, s3_filepath, filename, user_id, folder_id, lat, lng, filesize, image_resource_type, created_at, updated_at, address_road, address_land, address_land_number, building_name, address_det, address_search, address_sort, is_signed, is_shared, has_det):
        self.uuid = str(uuid.uuid4())
        self.s3_info = s3_info
        self.s3_filepath = s3_filepath
        self.filename = filename
        self.user_id = user_id
        self.folder_id = folder_id
        self.lat = lat
        self.lng = lng
        self.filesize = filesize
        self.image_resource_type = image_resource_type
        self.created_at = created_at
        self.updated_at = updated_at 
        self.delete_at = None
        self.address_road = address_road
        self.address_land = address_land
        self.address_land_number = address_land_number
        self.building_name = building_name
        self.address_det = address_det
        self.address_search = address_search
        self.address_sort = address_sort
        self.is_signed = is_signed
        self.is_shared = is_shared
        self.has_det = has_det