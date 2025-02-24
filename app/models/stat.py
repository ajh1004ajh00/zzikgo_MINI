import shortuuid

from sqlalchemy             import Column, Integer, String, Float, DateTime, Boolean, ForeignKey

from app.database.engine    import Base


class Stat(Base):
    __tablename__ = 'stats'

    id = Column(String, primary_key=True, index=True)
    platform_id = Column(String, ForeignKey('platforms.id'), index=True)
    upload_camera = Column(Integer, default=0)
    upload_gallery = Column(Integer, default=0)
    upload_request = Column(Integer, default=0)
    total_upload = Column(Integer, default=0)
    edit_count = Column(Integer, default=0)
    delete_count = Column(Integer, default=0)
    total_images = Column(Integer, default=0)
    org_filesize = Column(Float, default=0)
    org_latest_filesize = Column(Float, default=0)
    total_filesize = Column(Float, default=0)
    calculated_at = Column(String, nullable=False)
    
    def __init__(self, platform_id, upload_camera, upload_gallery, upload_request, total_upload, edit_count, delete_count, total_images, org_filesize, org_latest_filesize, total_filesize, calculated_at):
        self.id = shortuuid.ShortUUID().random(length=10)
        self.platform_id = platform_id
        self.upload_camera = upload_camera
        self.upload_gallery = upload_gallery
        self.upload_request = upload_request
        self.total_upload = total_upload
        self.edit_count = edit_count
        self.delete_count = delete_count
        self.total_images = total_images
        self.org_filesize = org_filesize
        self.org_latest_filesize = org_latest_filesize
        self.total_filesize = total_filesize
        self.calculated_at = calculated_at
